# Claude CLI Project Management Guide

## Overview
The enhanced Claude CLI now includes project management features that allow you to:
- Organize conversations by project
- Save and load session history
- Use temporary projects for one-off sessions
- Convert temporary projects to permanent ones

## Key Features

### 1. Auto-Selection on Startup
When you start the CLI:
- If projects exist, the first non-temporary project is auto-selected
- If no projects exist, a temporary project is automatically created
- You'll see the current project status immediately

### 2. Temporary Projects
- Created automatically if no projects exist
- Perfect for quick, one-off sessions
- Not saved to disk when you exit
- Can be converted to permanent projects during the session

### 3. Project Commands

```bash
# List all projects
/project list

# Create a new project
/project new myproject
/project new myproject /path/to/project

# Create a temporary project
/project temp
/project temp quick-test

# Select a project
/project select myproject

# Convert temp to permanent
/project convert temp-name
/project convert temp-name new-permanent-name

# View project sessions
/project sessions
```

### 4. Session Management

```bash
# Save current session
/session save

# Load a previous session
/session load 0  # Load first session
/session load 2  # Load third session
```

## Usage Examples

### Quick Start
```bash
# Run the CLI
python3 claude_cli_with_projects.py

# It will auto-create a temp project if none exist
# Start chatting immediately!
```

### Working on a Specific Project
```bash
# Create and use a project
/project new webapp /home/user/webapp
# Now all conversations are saved under this project

# Later, resume work
/project select webapp
/session load 0  # Load previous conversation
```

### Converting Temp to Permanent
```bash
# Start with a temp project (auto-created)
# ... do some work ...

# Decide to keep it
/project convert temp_20250621_143022 my-analysis
# Now it's saved permanently!
```

## File Storage

Projects and sessions are stored in:
- `~/.claude_cli/projects.json` - Project registry
- `<project_path>/.claude_project_<name>.json` - Individual project data

## Tips

1. **Use temp projects** for experiments and one-off tasks
2. **Create named projects** for ongoing work
3. **Save sessions** before exiting to preserve conversation history
4. **Load previous sessions** to continue where you left off
5. **Convert temp projects** when you realize the work is worth keeping