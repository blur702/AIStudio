import React, { useState } from 'react';
import './Help.css';

const Help = () => {
  const [activeSection, setActiveSection] = useState('user-getting-started');

  const userDocs = {
    'user-getting-started': {
      title: 'Getting Started',
      content: `
        <h3>Welcome to Claude Web Interface</h3>
        <p>The Claude Web Interface is a powerful tool for interacting with Claude AI to help with coding, analysis, and various development tasks.</p>
        
        <h4>First Steps</h4>
        <ol>
          <li><strong>Create a Project:</strong> Click "New Project" to start a new conversation context</li>
          <li><strong>Ask Questions:</strong> Type your questions or requests in the chat input</li>
          <li><strong>Review Responses:</strong> Claude will provide detailed answers with code examples</li>
          <li><strong>Save Sessions:</strong> Your conversations are automatically saved within projects</li>
        </ol>

        <h4>Quick Tips</h4>
        <ul>
          <li>Use clear, specific prompts for better results</li>
          <li>You can ask follow-up questions to refine responses</li>
          <li>Projects help organize related conversations</li>
          <li>Sessions are saved automatically for future reference</li>
        </ul>
      `
    },
    'user-projects': {
      title: 'Managing Projects',
      content: `
        <h3>Project Management</h3>
        <p>Projects help you organize your work and maintain context across multiple sessions.</p>

        <h4>Creating Projects</h4>
        <ul>
          <li><strong>Named Projects:</strong> Click "New Project" and provide a descriptive name</li>
          <li><strong>Temporary Projects:</strong> Start chatting immediately - a temp project is created automatically</li>
          <li><strong>Project Path:</strong> Optionally specify a directory path for code-related projects</li>
        </ul>

        <h4>Project Features</h4>
        <ul>
          <li><strong>Session History:</strong> All conversations within a project are saved</li>
          <li><strong>Context Preservation:</strong> Claude maintains awareness of your project's context</li>
          <li><strong>Quick Switching:</strong> Easily switch between projects from the sidebar</li>
          <li><strong>Convert Temp Projects:</strong> Save temporary projects with a proper name when needed</li>
        </ul>

        <h4>Best Practices</h4>
        <ul>
          <li>Use descriptive project names for easy identification</li>
          <li>Create separate projects for different topics or codebases</li>
          <li>Review project sessions to track your progress</li>
          <li>Delete old projects to keep your workspace organized</li>
        </ul>
      `
    },
    'user-chat': {
      title: 'Chat Interface',
      content: `
        <h3>Using the Chat Interface</h3>
        <p>The chat interface is designed for natural conversation with Claude about your coding needs.</p>

        <h4>Effective Prompting</h4>
        <ul>
          <li><strong>Be Specific:</strong> "Help me create a React component for user authentication" vs "Help with React"</li>
          <li><strong>Provide Context:</strong> Include relevant code snippets or error messages</li>
          <li><strong>Ask for Explanations:</strong> Request explanations for complex concepts</li>
          <li><strong>Iterate:</strong> Ask follow-up questions to refine the solution</li>
        </ul>

        <h4>Supported Tasks</h4>
        <ul>
          <li>Code generation and refactoring</li>
          <li>Debugging and error analysis</li>
          <li>Architecture and design discussions</li>
          <li>Code review and optimization</li>
          <li>Learning new technologies</li>
          <li>Writing documentation</li>
        </ul>

        <h4>Chat Features</h4>
        <ul>
          <li><strong>Code Highlighting:</strong> Code blocks are automatically syntax highlighted</li>
          <li><strong>Copy Code:</strong> Click the copy button on code blocks</li>
          <li><strong>Markdown Support:</strong> Responses support full markdown formatting</li>
          <li><strong>Session Persistence:</strong> Your chat history is saved automatically</li>
        </ul>
      `
    },
    'user-tips': {
      title: 'Tips & Tricks',
      content: `
        <h3>Power User Tips</h3>
        
        <h4>Productivity Shortcuts</h4>
        <ul>
          <li><strong>Ctrl/Cmd + Enter:</strong> Send message quickly</li>
          <li><strong>Up Arrow:</strong> Access previous messages</li>
          <li><strong>Tab:</strong> Navigate between UI elements</li>
        </ul>

        <h4>Advanced Prompting Techniques</h4>
        <ul>
          <li><strong>Step-by-Step:</strong> Ask Claude to break down complex tasks</li>
          <li><strong>Examples:</strong> Provide examples of desired output format</li>
          <li><strong>Constraints:</strong> Specify requirements like "using TypeScript" or "following REST principles"</li>
          <li><strong>Review Mode:</strong> Ask Claude to review and improve existing code</li>
        </ul>

        <h4>Common Use Cases</h4>
        <ol>
          <li><strong>Debugging:</strong> "Here's my error: [error]. Here's my code: [code]. What's wrong?"</li>
          <li><strong>Learning:</strong> "Explain [concept] with simple examples"</li>
          <li><strong>Refactoring:</strong> "How can I improve this code for better performance?"</li>
          <li><strong>Implementation:</strong> "Create a [feature] that does [specification]"</li>
        </ol>

        <h4>Maximizing Claude's Capabilities</h4>
        <ul>
          <li>Break large tasks into smaller, manageable pieces</li>
          <li>Provide complete error messages and stack traces</li>
          <li>Share relevant file structures for context</li>
          <li>Ask for best practices and industry standards</li>
          <li>Request test cases along with implementations</li>
        </ul>
      `
    }
  };

  const developerDocs = {
    'dev-architecture': {
      title: 'Architecture Overview',
      content: `
        <h3>System Architecture</h3>
        <p>The Claude Web Interface is built with a modern, scalable architecture.</p>

        <h4>Technology Stack</h4>
        <ul>
          <li><strong>Frontend:</strong> React 18 with React Router for SPA functionality</li>
          <li><strong>Backend:</strong> Flask (Python) REST API</li>
          <li><strong>State Management:</strong> React hooks and context</li>
          <li><strong>Styling:</strong> CSS modules for component isolation</li>
          <li><strong>Build Tool:</strong> Create React App (Webpack)</li>
        </ul>

        <h4>Component Structure</h4>
        <pre><code>src/
├── components/
│   ├── App.js          # Main application component
│   ├── Header.js       # Navigation header
│   ├── ProjectList.js  # Project management sidebar
│   ├── ChatWindow.js   # Main chat interface
│   ├── ChatMessage.js  # Individual message component
│   └── Help.js         # This documentation
├── services/
│   └── api.js          # API client for backend communication
└── index.js            # Application entry point</code></pre>

        <h4>Backend Structure</h4>
        <pre><code>backend/
├── app.py              # Flask application and routes
├── requirements.txt    # Python dependencies
└── data/              # Persistent storage
    ├── projects.json  # Project metadata
    └── sessions/      # Chat session files</code></pre>

        <h4>Data Flow</h4>
        <ol>
          <li>User input → React component → API service</li>
          <li>API service → Flask backend → Process request</li>
          <li>Backend → Save to disk → Return response</li>
          <li>Response → Update React state → Re-render UI</li>
        </ol>
      `
    },
    'dev-setup': {
      title: 'Development Setup',
      content: `
        <h3>Setting Up Development Environment</h3>

        <h4>Prerequisites</h4>
        <ul>
          <li>Node.js 18+ and npm</li>
          <li>Python 3.10+</li>
          <li>Git</li>
          <li>Anthropic API key</li>
        </ul>

        <h4>Installation Steps</h4>
        <ol>
          <li><strong>Clone the repository:</strong>
            <pre><code>git clone git@github.com:blur702/AIStudio.git
cd AIStudio/claude-web-interface</code></pre>
          </li>
          <li><strong>Set up environment variables:</strong>
            <pre><code>cp .env.example .env
# Edit .env and add your API keys</code></pre>
          </li>
          <li><strong>Install backend dependencies:</strong>
            <pre><code>cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt</code></pre>
          </li>
          <li><strong>Install frontend dependencies:</strong>
            <pre><code>cd ../frontend
npm install</code></pre>
          </li>
        </ol>

        <h4>Running in Development</h4>
        <p>Start both servers in separate terminals:</p>
        <pre><code># Terminal 1 - Backend
cd backend
source venv/bin/activate
python app.py

# Terminal 2 - Frontend
cd frontend
npm start</code></pre>

        <h4>Development URLs</h4>
        <ul>
          <li>Frontend: http://localhost:3001</li>
          <li>Backend API: http://localhost:5001</li>
        </ul>

        <h4>Environment Variables</h4>
        <pre><code>ANTHROPIC_API_KEY=your-api-key
FLASK_SECRET_KEY=your-secret-key
REACT_APP_API_URL=http://localhost:5001</code></pre>
      `
    },
    'dev-api': {
      title: 'API Reference',
      content: `
        <h3>Backend API Reference</h3>

        <h4>Base URL</h4>
        <pre><code>http://localhost:5001/api</code></pre>

        <h4>Endpoints</h4>

        <h5>GET /api/projects</h5>
        <p>Get all projects including temporary ones</p>
        <pre><code>Response:
{
  "projects": [
    {
      "id": "uuid",
      "name": "Project Name",
      "path": "/path/to/project",
      "is_temp": false,
      "created_at": "2024-01-01T00:00:00",
      "last_accessed": "2024-01-01T00:00:00",
      "session_count": 5
    }
  ],
  "current_project_id": "uuid"
}</code></pre>

        <h5>POST /api/projects</h5>
        <p>Create a new project</p>
        <pre><code>Request:
{
  "name": "My Project",
  "path": "/optional/path",
  "is_temp": false
}

Response:
{
  "id": "uuid",
  "name": "My Project",
  ...
}</code></pre>

        <h5>POST /api/projects/:id/select</h5>
        <p>Select a project as current</p>
        <pre><code>Response:
{
  "success": true,
  "project_id": "uuid"
}</code></pre>

        <h5>POST /api/projects/:id/convert</h5>
        <p>Convert temporary project to permanent</p>
        <pre><code>Request:
{
  "name": "New Name"
}</code></pre>

        <h5>POST /api/sessions</h5>
        <p>Save current chat session</p>
        <pre><code>Request:
{
  "project_id": "uuid",
  "messages": [...],
  "metadata": {}
}</code></pre>

        <h5>GET /api/sessions/:project_id</h5>
        <p>Get all sessions for a project</p>

        <h5>POST /api/claude/query</h5>
        <p>Send query to Claude</p>
        <pre><code>Request:
{
  "prompt": "Your question here"
}</code></pre>

        <h4>Error Responses</h4>
        <pre><code>{
  "error": "Error message"
}</code></pre>
      `
    },
    'dev-frontend': {
      title: 'Frontend Development',
      content: `
        <h3>Frontend Development Guide</h3>

        <h4>Component Guidelines</h4>
        <ul>
          <li>Use functional components with hooks</li>
          <li>Keep components focused and single-purpose</li>
          <li>Extract reusable logic into custom hooks</li>
          <li>Use prop-types for type checking</li>
        </ul>

        <h4>State Management</h4>
        <pre><code>// Local state for UI
const [isLoading, setIsLoading] = useState(false);

// Shared state via props
&lt;ChatWindow 
  messages={messages}
  onSendMessage={handleSendMessage}
/&gt;

// API state management
useEffect(() => {
  fetchProjects().then(setProjects);
}, []);</code></pre>

        <h4>API Integration</h4>
        <pre><code>// services/api.js
export const api = {
  getProjects: async () => {
    const response = await fetch(\`\${API_BASE_URL}/projects\`);
    return response.json();
  },
  
  createProject: async (projectData) => {
    const response = await fetch(\`\${API_BASE_URL}/projects\`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(projectData)
    });
    return response.json();
  }
};</code></pre>

        <h4>Styling Best Practices</h4>
        <ul>
          <li>Use CSS modules for component styles</li>
          <li>Follow BEM naming convention</li>
          <li>Use CSS variables for theming</li>
          <li>Mobile-first responsive design</li>
        </ul>

        <h4>Testing</h4>
        <pre><code>// Run tests
npm test

// Test example
import { render, screen } from '@testing-library/react';
import Header from './Header';

test('renders header with title', () => {
  render(&lt;Header /&gt;);
  const title = screen.getByText(/Claude Web Interface/i);
  expect(title).toBeInTheDocument();
});</code></pre>
      `
    },
    'dev-deployment': {
      title: 'Deployment',
      content: `
        <h3>Deployment Guide</h3>

        <h4>Production Build</h4>
        <pre><code># Build frontend
cd frontend
npm run build

# The build folder contains optimized production files</code></pre>

        <h4>Server Configuration</h4>
        <h5>Nginx Configuration</h5>
        <pre><code>server {
  listen 80;
  server_name your-domain.com;

  # Frontend
  location / {
    root /opt/code/claude-web-interface/frontend/build;
    try_files $uri $uri/ /index.html;
  }

  # Backend API
  location /api {
    proxy_pass http://localhost:5001;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
  }
}</code></pre>

        <h4>Process Management</h4>
        <h5>Systemd Service (Backend)</h5>
        <pre><code>[Unit]
Description=Claude Web Interface Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/code/claude-web-interface/backend
Environment="PATH=/opt/code/claude-web-interface/backend/venv/bin"
Environment="FLASK_SECRET_KEY=your-production-secret"
ExecStart=/opt/code/claude-web-interface/backend/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target</code></pre>

        <h4>GitHub Actions CI/CD</h4>
        <p>The project includes GitHub Actions workflows for:</p>
        <ul>
          <li>Automated testing on push</li>
          <li>Building and deployment</li>
          <li>Security scanning</li>
        </ul>

        <h4>Environment Variables</h4>
        <p>Production environment variables:</p>
        <ul>
          <li><code>ANTHROPIC_API_KEY</code> - Store in GitHub Secrets</li>
          <li><code>FLASK_SECRET_KEY</code> - Generate secure random key</li>
          <li><code>FLASK_ENV=production</code></li>
          <li><code>REACT_APP_API_URL</code> - Production API URL</li>
        </ul>

        <h4>Security Checklist</h4>
        <ul>
          <li>✓ Use HTTPS in production</li>
          <li>✓ Set secure session cookies</li>
          <li>✓ Enable CORS for specific origins only</li>
          <li>✓ Store secrets in environment variables</li>
          <li>✓ Regular dependency updates</li>
          <li>✓ Input validation and sanitization</li>
        </ul>
      `
    },
    'dev-contributing': {
      title: 'Contributing',
      content: `
        <h3>Contributing Guidelines</h3>

        <h4>Getting Started</h4>
        <ol>
          <li>Fork the repository</li>
          <li>Create a feature branch: <code>git checkout -b feature/your-feature</code></li>
          <li>Make your changes</li>
          <li>Test thoroughly</li>
          <li>Commit with clear messages</li>
          <li>Push and create a pull request</li>
        </ol>

        <h4>Code Standards</h4>
        <ul>
          <li><strong>Python:</strong> Follow PEP 8, use type hints</li>
          <li><strong>JavaScript:</strong> ESLint configuration, modern ES6+</li>
          <li><strong>Commits:</strong> Use conventional commit format</li>
          <li><strong>Documentation:</strong> Update docs with new features</li>
        </ul>

        <h4>Testing Requirements</h4>
        <ul>
          <li>Write tests for new features</li>
          <li>Maintain test coverage above 80%</li>
          <li>All tests must pass before merge</li>
          <li>Include integration tests for API changes</li>
        </ul>

        <h4>Pull Request Process</h4>
        <ol>
          <li>Update documentation</li>
          <li>Add tests for new functionality</li>
          <li>Ensure all tests pass</li>
          <li>Update CHANGELOG.md</li>
          <li>Request review from maintainers</li>
        </ol>

        <h4>Development Workflow</h4>
        <pre><code># 1. Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# 2. Create feature branch
git checkout -b feature/new-feature

# 3. Make changes and test
npm test
python -m pytest

# 4. Commit changes
git add .
git commit -m "feat: add new feature"

# 5. Push and create PR
git push origin feature/new-feature</code></pre>

        <h4>Questions?</h4>
        <p>Open an issue on GitHub for questions or discussions about contributing.</p>
      `
    }
  };

  const renderContent = (content) => {
    return <div dangerouslySetInnerHTML={{ __html: content }} />;
  };

  return (
    <div className="help-container">
      <div className="help-sidebar">
        <div className="help-section">
          <h3>User Guide</h3>
          <ul>
            {Object.entries(userDocs).map(([key, doc]) => (
              <li key={key}>
                <button
                  className={activeSection === key ? 'active' : ''}
                  onClick={() => setActiveSection(key)}
                >
                  {doc.title}
                </button>
              </li>
            ))}
          </ul>
        </div>
        
        <div className="help-section">
          <h3>Developer Guide</h3>
          <ul>
            {Object.entries(developerDocs).map(([key, doc]) => (
              <li key={key}>
                <button
                  className={activeSection === key ? 'active' : ''}
                  onClick={() => setActiveSection(key)}
                >
                  {doc.title}
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
      
      <div className="help-content">
        <h1>Documentation</h1>
        {userDocs[activeSection] && (
          <div className="doc-section">
            <h2>{userDocs[activeSection].title}</h2>
            {renderContent(userDocs[activeSection].content)}
          </div>
        )}
        {developerDocs[activeSection] && (
          <div className="doc-section">
            <h2>{developerDocs[activeSection].title}</h2>
            {renderContent(developerDocs[activeSection].content)}
          </div>
        )}
      </div>
    </div>
  );
};

export default Help;