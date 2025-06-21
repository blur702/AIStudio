import React, { useState, useEffect } from 'react'
import api from '../lib/api'

interface Project {
  id: string
  name: string
  path: string
  is_temp: boolean
  created_at: string
  last_accessed: string
  session_count: number
}

interface ProjectSelectionModalProps {
  onSelectProject: (project: Project) => void
  onClose: () => void
}

const ProjectSelectionModal: React.FC<ProjectSelectionModalProps> = ({
  onSelectProject,
  onClose: _onClose
}) => {
  const [projects, setProjects] = useState<Project[]>([])
  const [selectedProject, setSelectedProject] = useState<Project | null>(null)
  const [showNewProjectForm, setShowNewProjectForm] = useState(false)
  const [newProjectName, setNewProjectName] = useState('')
  const [newProjectPath, setNewProjectPath] = useState('')

  useEffect(() => {
    loadProjects()
  }, [])

  const loadProjects = async () => {
    try {
      const response = await api.get('/code/api/projects')
      setProjects(response.data.projects)
    } catch (error) {
      console.error('Error loading projects:', error)
    }
  }

  const handleCreateProject = async (isTemp: boolean = false) => {
    try {
      const projectData = {
        name: isTemp ? `Temp Session ${new Date().toLocaleString()}` : newProjectName,
        path: isTemp ? undefined : newProjectPath || undefined,
        is_temp: isTemp
      }

      const response = await api.post('/code/api/projects', projectData)
      const newProject = response.data

      // Select the project
      await api.post(`/code/api/projects/${newProject.id}/select`)
      
      onSelectProject(newProject)
    } catch (error) {
      console.error('Error creating project:', error)
      alert('Failed to create project')
    }
  }

  const handleSelectProject = async () => {
    if (!selectedProject) return

    try {
      await api.post(`/code/api/projects/${selectedProject.id}/select`)
      onSelectProject(selectedProject)
    } catch (error) {
      console.error('Error selecting project:', error)
      alert('Failed to select project')
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleString()
  }

  return (
    <div className="modal-overlay">
      <div className="modal">
        <div className="modal-header">
          <h2 className="modal-title">Select a Project</h2>
        </div>

        <div className="modal-body">
          {!showNewProjectForm ? (
            <>
              {/* Existing Projects */}
              {projects.length > 0 && (
                <>
                  <div className="project-list">
                    {projects.map((project) => (
                      <div
                        key={project.id}
                        className={`project-item ${
                          selectedProject?.id === project.id ? 'selected' : ''
                        }`}
                        onClick={() => setSelectedProject(project)}
                      >
                        <div className="project-name">
                          {project.name}
                          {project.is_temp && <span className="temp-badge">TEMP</span>}
                        </div>
                        <div className="project-meta">
                          Last accessed: {formatDate(project.last_accessed)} • {project.session_count} sessions
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="divider">
                    <span className="divider-text">or</span>
                  </div>
                </>
              )}

              {/* Action Buttons */}
              <div className="button-group">
                <button
                  className="button button-outline"
                  onClick={() => handleCreateProject(true)}
                >
                  Start Temporary Session
                </button>
                <button
                  className="button button-primary"
                  onClick={() => setShowNewProjectForm(true)}
                >
                  Create New Project
                </button>
              </div>

              {/* Select Button */}
              {selectedProject && (
                <div className="button-group" style={{ marginTop: '16px' }}>
                  <button
                    className="button button-primary"
                    onClick={handleSelectProject}
                  >
                    Open Selected Project
                  </button>
                </div>
              )}
            </>
          ) : (
            /* New Project Form */
            <div className="new-project-form">
              <div className="form-group">
                <label className="form-label">Project Name</label>
                <input
                  type="text"
                  className="form-input"
                  value={newProjectName}
                  onChange={(e) => setNewProjectName(e.target.value)}
                  placeholder="My Project"
                  autoFocus
                />
              </div>

              <div className="form-group">
                <label className="form-label">Project Path (optional)</label>
                <input
                  type="text"
                  className="form-input"
                  value={newProjectPath}
                  onChange={(e) => setNewProjectPath(e.target.value)}
                  placeholder="/path/to/project"
                />
              </div>

              <div className="button-group">
                <button
                  className="button button-secondary"
                  onClick={() => {
                    setShowNewProjectForm(false)
                    setNewProjectName('')
                    setNewProjectPath('')
                  }}
                >
                  Cancel
                </button>
                <button
                  className="button button-primary"
                  onClick={() => handleCreateProject(false)}
                  disabled={!newProjectName.trim()}
                >
                  Create Project
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ProjectSelectionModal