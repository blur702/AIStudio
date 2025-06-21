# AIStudio

A comprehensive Claude-powered development environment with automated GitHub integration.

## Features

- **Claude Web Interface**: Web-based UI for interacting with Claude
- **Automated GitHub Builder**: Monitors GitHub repos for specification changes and automatically builds projects
- **Project Management**: Built-in project and session management

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

### Environment Variables

Copy `.env.example` to `.env` and set the following:

```bash
# Required
ANTHROPIC_API_KEY=your-anthropic-api-key-here
FLASK_SECRET_KEY=your-secure-random-secret-key-here

# Optional
GITHUB_TOKEN=your-github-personal-access-token-here
CLAUDE_WEB_PORT=5001
CLAUDE_WEB_DEBUG=false
```

### GitHub Secrets

For GitHub Actions to work, add these secrets to your repository:

1. Go to Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `FLASK_SECRET_KEY`: A secure random string for Flask sessions
   - `GITHUB_TOKEN`: (Optional) For private repository access

### Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:blur702/AIStudio.git
   cd AIStudio
   ```

2. Install backend dependencies:
   ```bash
   cd claude-web-interface/backend
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd ../frontend
   npm install
   ```

## Usage

### Claude Web Interface

1. Start the backend:
   ```bash
   cd claude-web-interface/backend
   python app.py
   ```

2. Start the frontend:
   ```bash
   cd claude-web-interface/frontend
   npm start
   ```

3. Open http://localhost:3001 in your browser

### Automated GitHub Builder

1. Configure `builder_config.json`:
   ```json
   {
     "specs_repo": "https://github.com/yourusername/project-specs.git",
     "output_repo": "https://github.com/yourusername/generated-project.git",
     "work_directory": "/opt/code/automated_builds",
     "check_interval_minutes": 30
   }
   ```

2. Run the builder:
   ```bash
   python github_automated_builder.py
   ```

## Security Notes

- Never commit `.env` files or secrets to the repository
- Use GitHub Secrets for CI/CD workflows
- Rotate API keys regularly
- Use strong, random values for `FLASK_SECRET_KEY`

## Development

- Backend tests: `cd backend && pytest`
- Frontend tests: `cd frontend && npm test`
- Linting: `cd backend && ruff check .`

## License

[Your license here]