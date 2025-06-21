# Claude Web Interface

A modern web interface for Claude with project management capabilities.

## Features

- **Project Selection Modal**: Automatically shows on startup to select or create a project
- **Temporary Projects**: Quick sessions that are destroyed when the browser closes
- **Save to Permanent**: Convert temporary projects to permanent ones with a single click
- **Session Management**: Save and load conversation history
- **Clean UI**: Modern, responsive interface with a header showing current project and save button

## Quick Start

1. Run the start script:
   ```bash
   cd /opt/code/claude-web-interface
   ./start.sh
   ```

2. Open your browser to http://localhost:3001

3. The project selection modal will appear automatically:
   - Select an existing project
   - Create a new permanent project
   - Start a temporary session

## Architecture

- **Frontend**: React + TypeScript + Vite
- **Backend**: Flask API with session management
- **Storage**: Projects stored in ~/.claude_web

## Key Features

### Project Selection Modal (on startup)
- Lists all existing projects with metadata
- Shows session count and last accessed time
- Options to create new project or start temp session
- Temp projects marked with "TEMP" badge

### Header Save Button
- Always visible in the header
- Disabled when no changes to save
- For temp projects: prompts to convert to permanent
- For permanent projects: saves session directly

### Temporary Projects
- Created with one click
- Exist only in browser session
- Can be converted to permanent at any time
- Destroyed when session ends (unless saved)

## API Endpoints

- `GET /api/projects` - List all projects
- `POST /api/projects` - Create new project
- `POST /api/projects/:id/select` - Select a project
- `POST /api/projects/:id/convert` - Convert temp to permanent
- `POST /api/sessions` - Save current session
- `GET /api/sessions/:projectId` - Get project sessions