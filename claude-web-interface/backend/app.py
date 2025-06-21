#!/usr/bin/env python3
"""
Flask backend for Claude Web Interface with project management
"""

from flask import Flask, jsonify, request, session
from flask_cors import CORS
from datetime import datetime
import json
import os
from pathlib import Path
import uuid
import asyncio
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
CORS(app, origins=['http://localhost:3001', 'https://kevinalthaus.com', 'http://kevinalthaus.com'], supports_credentials=True)

# Storage paths
DATA_DIR = Path.home() / '.claude_web'
DATA_DIR.mkdir(exist_ok=True)
PROJECTS_FILE = DATA_DIR / 'projects.json'
SESSIONS_DIR = DATA_DIR / 'sessions'
SESSIONS_DIR.mkdir(exist_ok=True)


class ProjectManager:
    @staticmethod
    def load_projects():
        """Load all projects from disk"""
        if PROJECTS_FILE.exists():
            with open(PROJECTS_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    @staticmethod
    def save_projects(projects):
        """Save projects to disk (excluding temp projects)"""
        permanent_projects = {
            pid: proj for pid, proj in projects.items() 
            if not proj.get('is_temp', False)
        }
        with open(PROJECTS_FILE, 'w') as f:
            json.dump(permanent_projects, f, indent=2)
    
    @staticmethod
    def create_project(name, path=None, is_temp=False):
        """Create a new project"""
        projects = ProjectManager.load_projects()
        project_id = str(uuid.uuid4())
        
        project = {
            'id': project_id,
            'name': name,
            'path': path or os.getcwd(),
            'is_temp': is_temp,
            'created_at': datetime.now().isoformat(),
            'last_accessed': datetime.now().isoformat(),
            'session_count': 0
        }
        
        projects[project_id] = project
        
        if not is_temp:
            ProjectManager.save_projects(projects)
        
        return project
    
    @staticmethod
    def get_session_file(project_id, session_id):
        """Get path to session file"""
        return SESSIONS_DIR / f"{project_id}_{session_id}.json"
    
    @staticmethod
    def save_session(project_id, session_data):
        """Save a session"""
        session_id = str(uuid.uuid4())
        session_file = ProjectManager.get_session_file(project_id, session_id)
        
        with open(session_file, 'w') as f:
            json.dump({
                'id': session_id,
                'project_id': project_id,
                'created_at': datetime.now().isoformat(),
                'messages': session_data.get('messages', []),
                'metadata': session_data.get('metadata', {})
            }, f, indent=2)
        
        # Update project session count
        projects = ProjectManager.load_projects()
        if project_id in projects:
            projects[project_id]['session_count'] += 1
            projects[project_id]['last_accessed'] = datetime.now().isoformat()
            ProjectManager.save_projects(projects)
        
        return session_id
    
    @staticmethod
    def convert_temp_to_permanent(temp_project_id, new_name=None):
        """Convert a temporary project to permanent"""
        projects = ProjectManager.load_projects()
        
        # Get temp project from session
        temp_projects = session.get('temp_projects', {})
        if temp_project_id not in temp_projects:
            raise ValueError("Temporary project not found")
        
        project = temp_projects[temp_project_id]
        project['is_temp'] = False
        if new_name:
            project['name'] = new_name
        
        # Add to permanent projects
        projects[temp_project_id] = project
        ProjectManager.save_projects(projects)
        
        # Remove from temp projects
        del temp_projects[temp_project_id]
        session['temp_projects'] = temp_projects
        
        return project


# Routes

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects including temp ones from session"""
    projects = ProjectManager.load_projects()
    
    # Add temp projects from session
    temp_projects = session.get('temp_projects', {})
    all_projects = {**projects, **temp_projects}
    
    # Convert to list and sort by last accessed
    project_list = list(all_projects.values())
    project_list.sort(key=lambda x: x.get('last_accessed', ''), reverse=True)
    
    return jsonify({
        'projects': project_list,
        'current_project_id': session.get('current_project_id')
    })


@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    data = request.json
    name = data.get('name', f"Project {datetime.now().strftime('%Y%m%d_%H%M%S')}")
    path = data.get('path')
    is_temp = data.get('is_temp', False)
    
    project = ProjectManager.create_project(name, path, is_temp)
    
    # Store temp projects in session
    if is_temp:
        if 'temp_projects' not in session:
            session['temp_projects'] = {}
        session['temp_projects'][project['id']] = project
    
    # Set as current project
    session['current_project_id'] = project['id']
    
    return jsonify(project)


@app.route('/api/projects/<project_id>/select', methods=['POST'])
def select_project(project_id):
    """Select a project as current"""
    projects = ProjectManager.load_projects()
    temp_projects = session.get('temp_projects', {})
    
    if project_id not in projects and project_id not in temp_projects:
        return jsonify({'error': 'Project not found'}), 404
    
    session['current_project_id'] = project_id
    
    # Update last accessed
    if project_id in projects:
        projects[project_id]['last_accessed'] = datetime.now().isoformat()
        ProjectManager.save_projects(projects)
    
    return jsonify({'success': True, 'project_id': project_id})


@app.route('/api/projects/<project_id>/convert', methods=['POST'])
def convert_project(project_id):
    """Convert temp project to permanent"""
    data = request.json
    new_name = data.get('name')
    
    try:
        project = ProjectManager.convert_temp_to_permanent(project_id, new_name)
        return jsonify(project)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/sessions', methods=['POST'])
def save_session():
    """Save current session"""
    data = request.json
    project_id = data.get('project_id') or session.get('current_project_id')
    
    if not project_id:
        return jsonify({'error': 'No project selected'}), 400
    
    session_id = ProjectManager.save_session(project_id, data)
    
    return jsonify({
        'session_id': session_id,
        'project_id': project_id
    })


@app.route('/api/sessions/<project_id>', methods=['GET'])
def get_sessions(project_id):
    """Get all sessions for a project"""
    sessions = []
    
    for session_file in SESSIONS_DIR.glob(f"{project_id}_*.json"):
        with open(session_file, 'r') as f:
            sessions.append(json.load(f))
    
    sessions.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return jsonify({'sessions': sessions})


@app.route('/api/claude/query', methods=['POST'])
async def claude_query():
    """Proxy Claude queries through the backend"""
    data = request.json
    prompt = data.get('prompt')
    project_id = session.get('current_project_id')
    
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    # Here you would integrate with claude-code-sdk
    # For now, return a mock response
    response = {
        'response': f"Mock response to: {prompt}",
        'project_id': project_id,
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(response)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


if __name__ == '__main__':
    app.run(debug=True, port=5001)