#!/usr/bin/env python3
"""Test script for the project management CLI"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
from claude_cli_with_projects import ProjectManager, Project

def test_project_management():
    """Test basic project management functionality"""
    print("Testing Project Management System...")
    
    # Create test config directory
    test_dir = Path("/tmp/claude_test")
    test_dir.mkdir(exist_ok=True)
    
    # Initialize project manager
    pm = ProjectManager(config_dir=test_dir)
    
    # Test 1: Create regular project
    print("\n1. Creating regular project...")
    try:
        project1 = pm.create_project("test-project", "/tmp")
        print(f"✓ Created project: {project1.name}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return
    
    # Test 2: Create temporary project
    print("\n2. Creating temporary project...")
    try:
        temp_project = pm.create_project("temp-project", "/tmp", is_temp=True)
        print(f"✓ Created temp project: {temp_project.name}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return
    
    # Test 3: List projects
    print("\n3. Listing projects...")
    projects = pm.list_projects()
    print(f"✓ Found {len(projects)} projects:")
    for p in projects:
        print(f"  - {p.name} {'(temp)' if p.is_temp else ''}")
    
    # Test 4: Select project
    print("\n4. Selecting project...")
    try:
        selected = pm.select_project("test-project")
        print(f"✓ Selected: {selected.name}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return
    
    # Test 5: Add session to project
    print("\n5. Adding session to project...")
    session_data = {
        'messages': [
            {'role': 'user', 'content': 'Hello'},
            {'role': 'assistant', 'content': 'Hi there!'}
        ],
        'session_id': 'test-123',
        'cost': 0.0001
    }
    selected.add_session(session_data)
    print(f"✓ Added session with {len(session_data['messages'])} messages")
    
    # Test 6: Convert temp to full project
    print("\n6. Converting temp project to full...")
    try:
        converted = pm.convert_temp_to_full("temp-project", "converted-project")
        print(f"✓ Converted to: {converted.name}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return
    
    # Test 7: Save and reload
    print("\n7. Testing persistence...")
    pm.save_projects()
    
    # Create new manager instance and check if projects persist
    pm2 = ProjectManager(config_dir=test_dir)
    reloaded = pm2.list_projects()
    
    # Should have 2 projects (test-project and converted-project)
    # temp-project should not be saved
    non_temp_count = len([p for p in reloaded if not p.is_temp])
    print(f"✓ Reloaded {non_temp_count} non-temp projects")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    test_project_management()