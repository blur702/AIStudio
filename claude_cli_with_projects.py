#!/usr/bin/env python3
"""
Enhanced Claude CLI interface with project management.
Features:
- Automatic project selection/listing on startup
- Temporary projects for single sessions
- Convert temp projects to full projects
- Save/load session history
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from claude_code_sdk import query, ClaudeCodeOptions, ResultMessage, AssistantMessage, SystemMessage
from ui_theme import Colors, Icons, Theme


class Project:
    """Represents a project with sessions"""
    def __init__(self, name: str, path: Path, is_temp: bool = False):
        self.name = name
        self.path = path
        self.is_temp = is_temp
        self.created_at = datetime.now().isoformat()
        self.sessions: List[Dict] = []
        self.current_session = None
        
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'path': str(self.path),
            'is_temp': self.is_temp,
            'created_at': self.created_at,
            'sessions': self.sessions
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Project':
        project = cls(data['name'], Path(data['path']), data.get('is_temp', False))
        project.created_at = data.get('created_at', datetime.now().isoformat())
        project.sessions = data.get('sessions', [])
        return project
    
    def add_session(self, session_data: Dict):
        """Add a session to the project"""
        self.sessions.append({
            'timestamp': datetime.now().isoformat(),
            'messages': session_data.get('messages', []),
            'session_id': session_data.get('session_id'),
            'cost': session_data.get('cost', 0)
        })
    
    def save(self):
        """Save project to disk (only for non-temp projects)"""
        if not self.is_temp:
            project_file = self.path / f".claude_project_{self.name}.json"
            with open(project_file, 'w') as f:
                json.dump(self.to_dict(), f, indent=2)


class ProjectManager:
    """Manages projects and their persistence"""
    def __init__(self, config_dir: Path = None):
        self.config_dir = config_dir or Path.home() / '.claude_cli'
        self.config_dir.mkdir(exist_ok=True)
        self.projects_file = self.config_dir / 'projects.json'
        self.projects: Dict[str, Project] = {}
        self.current_project: Optional[Project] = None
        self.load_projects()
    
    def load_projects(self):
        """Load projects from disk"""
        if self.projects_file.exists():
            try:
                with open(self.projects_file, 'r') as f:
                    data = json.load(f)
                    for name, project_data in data.items():
                        if not project_data.get('is_temp', False):
                            self.projects[name] = Project.from_dict(project_data)
            except Exception as e:
                print(Theme.status(f"Error loading projects: {e}", 'error'))
    
    def save_projects(self):
        """Save all non-temp projects to disk"""
        data = {}
        for name, project in self.projects.items():
            if not project.is_temp:
                data[name] = project.to_dict()
        
        with open(self.projects_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_project(self, name: str, path: str = None, is_temp: bool = False) -> Project:
        """Create a new project"""
        if name in self.projects:
            raise ValueError(f"Project '{name}' already exists")
        
        project_path = Path(path) if path else Path.cwd()
        project = Project(name, project_path, is_temp)
        self.projects[name] = project
        
        if not is_temp:
            self.save_projects()
        
        return project
    
    def list_projects(self) -> List[Project]:
        """List all projects"""
        return list(self.projects.values())
    
    def select_project(self, name: str) -> Project:
        """Select a project as current"""
        if name not in self.projects:
            raise ValueError(f"Project '{name}' not found")
        
        self.current_project = self.projects[name]
        return self.current_project
    
    def convert_temp_to_full(self, temp_name: str, new_name: str = None) -> Project:
        """Convert a temporary project to a full project"""
        if temp_name not in self.projects:
            raise ValueError(f"Project '{temp_name}' not found")
        
        project = self.projects[temp_name]
        if not project.is_temp:
            raise ValueError(f"Project '{temp_name}' is not a temporary project")
        
        # Create new full project
        final_name = new_name or temp_name
        if final_name != temp_name and final_name in self.projects:
            raise ValueError(f"Project '{final_name}' already exists")
        
        # Convert the project
        project.is_temp = False
        project.name = final_name
        
        # Update in projects dict if name changed
        if final_name != temp_name:
            del self.projects[temp_name]
            self.projects[final_name] = project
        
        # Save to disk
        project.save()
        self.save_projects()
        
        return project


class EnhancedClaudeInterface:
    def __init__(self):
        self.project_manager = ProjectManager()
        self.session_messages = []
        self.session_cost = 0
        self.session_id = None
        self.options = ClaudeCodeOptions(
            permission_mode='default',
            cwd=os.getcwd(),
            continue_conversation=True
        )
        
    def show_welcome(self):
        """Display welcome message with project info"""
        print(Theme.header("Claude AI Assistant - Project Mode", 60))
        
        # Show current project or prompt to select
        if self.project_manager.current_project:
            project = self.project_manager.current_project
            status = f"Current Project: {project.name}"
            if project.is_temp:
                status += " (Temporary)"
            print(Theme.status(status, 'info'))
        else:
            print(Theme.status("No project selected", 'warning'))
            self.list_projects()
        
        print(f"\n{Colors.MUTED}Type 'exit' to end • '/help' for commands{Colors.RESET}\n")
    
    def list_projects(self):
        """List all available projects"""
        projects = self.project_manager.list_projects()
        
        if not projects:
            print(f"{Colors.MUTED}No projects found. Use '/project new <name>' to create one.{Colors.RESET}")
            return
        
        print(f"\n{Colors.PRIMARY}Available Projects:{Colors.RESET}")
        for project in projects:
            status = f"  • {project.name}"
            if project.is_temp:
                status += f" {Colors.MUTED}(temp){Colors.RESET}"
            status += f" - {len(project.sessions)} sessions"
            print(status)
        
        print(f"\n{Colors.MUTED}Use '/project select <name>' to choose a project{Colors.RESET}")
    
    def show_help(self):
        """Display help with project commands"""
        commands = [
            ('exit, quit', 'End the conversation'),
            ('/help', 'Show this help message'),
            ('/clear', 'Clear the screen'),
            ('/project list', 'List all projects'),
            ('/project new <name> [path]', 'Create new project'),
            ('/project temp [name]', 'Create temporary project'),
            ('/project select <name>', 'Select a project'),
            ('/project convert <name>', 'Convert temp to full project'),
            ('/project sessions', 'Show project sessions'),
            ('/session save', 'Save current session'),
            ('/session load <index>', 'Load a previous session'),
        ]
        
        print(Theme.help_section("Commands", commands))
    
    def handle_project_command(self, args: List[str]):
        """Handle project-related commands"""
        if not args or args[0] == 'list':
            self.list_projects()
            
        elif args[0] == 'new':
            if len(args) < 2:
                print(Theme.status("Usage: /project new <name> [path]", 'error'))
                return
            
            name = args[1]
            path = args[2] if len(args) > 2 else None
            
            try:
                project = self.project_manager.create_project(name, path)
                self.project_manager.current_project = project
                print(Theme.status(f"Created project '{name}'", 'success'))
            except Exception as e:
                print(Theme.status(str(e), 'error'))
                
        elif args[0] == 'temp':
            name = args[1] if len(args) > 1 else f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            try:
                project = self.project_manager.create_project(name, is_temp=True)
                self.project_manager.current_project = project
                print(Theme.status(f"Created temporary project '{name}'", 'success'))
            except Exception as e:
                print(Theme.status(str(e), 'error'))
                
        elif args[0] == 'select':
            if len(args) < 2:
                print(Theme.status("Usage: /project select <name>", 'error'))
                return
            
            try:
                project = self.project_manager.select_project(args[1])
                self.options.cwd = str(project.path)
                print(Theme.status(f"Selected project '{project.name}'", 'success'))
            except Exception as e:
                print(Theme.status(str(e), 'error'))
                
        elif args[0] == 'convert':
            if len(args) < 2:
                print(Theme.status("Usage: /project convert <temp-name> [new-name]", 'error'))
                return
            
            temp_name = args[1]
            new_name = args[2] if len(args) > 2 else None
            
            try:
                project = self.project_manager.convert_temp_to_full(temp_name, new_name)
                print(Theme.status(f"Converted temporary project to '{project.name}'", 'success'))
            except Exception as e:
                print(Theme.status(str(e), 'error'))
                
        elif args[0] == 'sessions':
            if not self.project_manager.current_project:
                print(Theme.status("No project selected", 'error'))
                return
            
            project = self.project_manager.current_project
            if not project.sessions:
                print(f"{Colors.MUTED}No sessions found for this project{Colors.RESET}")
                return
            
            print(f"\n{Colors.PRIMARY}Sessions for {project.name}:{Colors.RESET}")
            for i, session in enumerate(project.sessions):
                timestamp = session.get('timestamp', 'Unknown')
                messages = len(session.get('messages', []))
                cost = session.get('cost', 0)
                print(f"  [{i}] {timestamp} - {messages} messages - ${cost:.4f}")
                
        else:
            print(Theme.status(f"Unknown project command: {args[0]}", 'error'))
    
    def handle_session_command(self, args: List[str]):
        """Handle session-related commands"""
        if not self.project_manager.current_project:
            print(Theme.status("No project selected", 'error'))
            return
        
        if not args or args[0] == 'save':
            # Save current session
            if self.session_messages:
                session_data = {
                    'messages': self.session_messages,
                    'session_id': self.session_id,
                    'cost': self.session_cost
                }
                self.project_manager.current_project.add_session(session_data)
                self.project_manager.current_project.save()
                print(Theme.status("Session saved", 'success'))
            else:
                print(Theme.status("No messages to save", 'warning'))
                
        elif args[0] == 'load':
            if len(args) < 2:
                print(Theme.status("Usage: /session load <index>", 'error'))
                return
            
            try:
                index = int(args[1])
                project = self.project_manager.current_project
                if 0 <= index < len(project.sessions):
                    session = project.sessions[index]
                    self.session_messages = session.get('messages', [])
                    print(Theme.status(f"Loaded session {index} with {len(self.session_messages)} messages", 'success'))
                else:
                    print(Theme.status(f"Invalid session index: {index}", 'error'))
            except ValueError:
                print(Theme.status("Session index must be a number", 'error'))
                
        else:
            print(Theme.status(f"Unknown session command: {args[0]}", 'error'))
    
    async def run_conversation(self, prompt: str):
        """Run conversation and track messages"""
        if not self.project_manager.current_project:
            print(Theme.status("Please select or create a project first", 'warning'))
            return
        
        # Add to session messages
        self.session_messages.append({'role': 'user', 'content': prompt})
        
        assistant_response = ""
        tool_uses = []
        
        try:
            print(f"\n{Colors.PRIMARY}Claude{Colors.RESET} {Colors.MUTED}is thinking...{Colors.RESET}", end='\r')
            
            async for message in query(prompt=prompt, options=self.options):
                if isinstance(message, AssistantMessage):
                    print(f"\r{' ' * 50}\r", end='')
                    print(f"{Colors.PRIMARY}Claude{Colors.RESET}: ", end="")
                    
                    for block in message.content:
                        if hasattr(block, 'text'):
                            print(block.text, end="", flush=True)
                            assistant_response += block.text
                        elif hasattr(block, 'name'):
                            tool_uses.append(block.name)
                            print(Theme.tool_use(block.name, block.input if hasattr(block, 'input') else {}))
                
                elif isinstance(message, ResultMessage):
                    self.session_id = message.session_id
                    if message.total_cost_usd:
                        self.session_cost += message.total_cost_usd
                        print(f" {Colors.MUTED}[${message.total_cost_usd:.4f}]{Colors.RESET}")
            
            # Add assistant response to session
            self.session_messages.append({'role': 'assistant', 'content': assistant_response})
            
        except Exception as e:
            print(f"\r{' ' * 50}\r", end='')
            print(Theme.status(f"Error: {e}", 'error'))
    
    async def run(self):
        """Main interaction loop"""
        # Auto-select or create temp project if none exists
        if not self.project_manager.current_project:
            projects = self.project_manager.list_projects()
            if projects:
                # Auto-select first non-temp project or create temp
                non_temp = [p for p in projects if not p.is_temp]
                if non_temp:
                    self.project_manager.select_project(non_temp[0].name)
                else:
                    # Create temp project
                    temp_name = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    self.project_manager.create_project(temp_name, is_temp=True)
                    self.project_manager.select_project(temp_name)
            else:
                # Create temp project
                temp_name = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                self.project_manager.create_project(temp_name, is_temp=True)
                self.project_manager.select_project(temp_name)
        
        self.show_welcome()
        
        while True:
            try:
                # Show project in prompt
                project_name = self.project_manager.current_project.name if self.project_manager.current_project else "no-project"
                prompt_str = input(f"\n{Theme.prompt(project_name, self.options.permission_mode)}").strip()
                
                if prompt_str.lower() in ['exit', 'quit']:
                    # Ask to save session if there are messages
                    if self.session_messages and self.project_manager.current_project and not self.project_manager.current_project.is_temp:
                        save = input(f"{Colors.WARNING}Save current session? (y/n): {Colors.RESET}").lower()
                        if save == 'y':
                            self.handle_session_command(['save'])
                    
                    print(Theme.status("Goodbye!", 'success'))
                    break
                
                if not prompt_str:
                    continue
                
                # Handle commands
                if prompt_str.startswith('/'):
                    parts = prompt_str.split()
                    command = parts[0]
                    
                    if command == '/help':
                        self.show_help()
                    elif command == '/clear':
                        os.system('clear' if os.name == 'posix' else 'cls')
                        self.show_welcome()
                    elif command == '/project':
                        self.handle_project_command(parts[1:])
                    elif command == '/session':
                        self.handle_session_command(parts[1:])
                    else:
                        print(Theme.status(f"Unknown command: {command}", 'error'))
                    continue
                
                # Run conversation
                await self.run_conversation(prompt_str)
                
            except KeyboardInterrupt:
                print(f"\n\n{Theme.status('Interrupted. Type exit to quit or continue chatting.', 'warning')}")
            except EOFError:
                print(f"\n{Theme.status('Goodbye!', 'success')}")
                break


async def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("Usage: python claude_cli_with_projects.py")
        print("Claude AI CLI with project management")
        return
    
    interface = EnhancedClaudeInterface()
    await interface.run()


if __name__ == "__main__":
    asyncio.run(main())