import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom'
import api from './lib/api'
import ProjectSelectionModal from './components/ProjectSelectionModal'
import ChatInterface from './components/ChatInterface'
import Help from './components/Help'

interface Project {
  id: string
  name: string
  path: string
  is_temp: boolean
  created_at: string
  last_accessed: string
  session_count: number
}

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

const App: React.FC = () => {
  const [showProjectModal, setShowProjectModal] = useState(true)
  const [currentProject, setCurrentProject] = useState<Project | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)

  useEffect(() => {
    // Check if there's a current project on load
    checkCurrentProject()
  }, [])

  const checkCurrentProject = async () => {
    try {
      const response = await api.get('/code/api/projects')
      if (response.data.current_project_id) {
        const project = response.data.projects.find(
          (p: Project) => p.id === response.data.current_project_id
        )
        if (project) {
          setCurrentProject(project)
          setShowProjectModal(false)
        }
      }
    } catch (error) {
      console.error('Error checking current project:', error)
    }
  }

  const handleProjectSelect = (project: Project) => {
    setCurrentProject(project)
    setShowProjectModal(false)
    setMessages([])
    setHasUnsavedChanges(false)
  }

  const handleSaveSession = async () => {
    if (!currentProject || !hasUnsavedChanges) return

    try {
      await api.post('/code/api/sessions', {
        project_id: currentProject.id,
        messages: messages,
        metadata: {
          saved_at: new Date().toISOString()
        }
      })

      // If it's a temp project, offer to convert
      if (currentProject.is_temp) {
        const shouldConvert = window.confirm(
          'Would you like to convert this temporary project to a permanent one?'
        )
        if (shouldConvert) {
          const newName = window.prompt('Enter a name for the project:', currentProject.name)
          if (newName) {
            const response = await api.post(`/code/api/projects/${currentProject.id}/convert`, {
              name: newName
            })
            setCurrentProject(response.data)
          }
        }
      }

      setHasUnsavedChanges(false)
      alert('Session saved successfully!')
    } catch (error) {
      console.error('Error saving session:', error)
      alert('Failed to save session')
    }
  }

  const handleNewMessage = (message: Message) => {
    setMessages([...messages, message])
    setHasUnsavedChanges(true)
  }

  const handleChangeProject = () => {
    if (hasUnsavedChanges) {
      const shouldSave = window.confirm(
        'You have unsaved changes. Would you like to save before switching projects?'
      )
      if (shouldSave) {
        handleSaveSession()
      }
    }
    setShowProjectModal(true)
  }

  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <div className="header-left">
            <Link to="/" className="header-title-link">
              <h1 className="header-title">Claude Web Interface</h1>
            </Link>
          </div>
          <div className="header-info">
            {currentProject && (
              <>
                <div className="project-info">
                  Current Project: <strong>{currentProject.name}</strong>
                  {currentProject.is_temp && <span className="temp-badge">TEMP</span>}
                </div>
                <button className="button button-outline" onClick={handleChangeProject}>
                  Change Project
                </button>
                <button
                  className="save-button"
                  onClick={handleSaveSession}
                  disabled={!hasUnsavedChanges}
                >
                  Save Session
                </button>
              </>
            )}
            <Link to="/help" className="help-link" title="Help & Documentation">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
            </Link>
          </div>
        </header>

        <main className="app-content">
          <Routes>
            <Route path="/" element={
              <>
                {showProjectModal && (
                  <ProjectSelectionModal
                    onSelectProject={handleProjectSelect}
                    onClose={() => setShowProjectModal(false)}
                  />
                )}

                {currentProject && !showProjectModal && (
                  <ChatInterface
                    project={currentProject}
                    messages={messages}
                    onNewMessage={handleNewMessage}
                  />
                )}
              </>
            } />
            <Route path="/help" element={<Help />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App