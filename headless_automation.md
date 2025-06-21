# Headless Claude Automation Options

## 1. **Systemd Service**
Create a service that runs your automation:

```bash
# /etc/systemd/system/claude-project-builder.service
[Unit]
Description=Claude Project Builder
After=network.target

[Service]
Type=simple
User=kevin
Environment="ANTHROPIC_API_KEY=your-api-key"
WorkingDirectory=/opt/code
ExecStart=/opt/code/venv/bin/python /opt/code/project_automation_example.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

## 2. **Cron Jobs**
Schedule automated builds:

```bash
# Run daily at 2 AM
0 2 * * * cd /opt/code && source venv/bin/activate && python project_automation_example.py
```

## 3. **Web API Wrapper**
Create a Flask/FastAPI endpoint to trigger builds:

```python
from flask import Flask, request
import asyncio
import subprocess

app = Flask(__name__)

@app.route('/build', methods=['POST'])
def trigger_build():
    specs = request.json
    # Save specs and trigger build
    subprocess.Popen(['python', '/opt/code/project_automation_example.py'])
    return {"status": "build started"}
```

## Important Authentication Considerations:

1. **API Key Required**: Claude Code CLI needs your Anthropic API key
   - Set via environment variable: `ANTHROPIC_API_KEY`
   - Or in ~/.claude/config.json

2. **Permission Mode**: Use `bypassPermissions` for fully automated operation
   - No interactive prompts
   - All tools execute automatically

3. **Session Management**: The SDK handles session continuity automatically

## Example Automated Workflow:

```python
# automated_builder.py
import asyncio
from pathlib import Path
import schedule
import time

async def build_from_github():
    """Pull specs from GitHub and build project"""
    # 1. Clone/pull latest specs
    # 2. Run project builder
    # 3. Push results back to GitHub
    
async def monitor_and_build():
    """Monitor for changes and trigger builds"""
    while True:
        if check_for_new_specs():
            await build_from_github()
        await asyncio.sleep(300)  # Check every 5 minutes
```

## Security Notes:
- Store API keys securely (use environment variables or secrets management)
- Limit file system permissions for the automation user
- Consider using Docker containers for isolated builds
- Monitor costs as automated builds can accumulate charges