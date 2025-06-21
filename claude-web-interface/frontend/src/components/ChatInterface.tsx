import React, { useState, useRef, useEffect } from 'react'
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

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

interface ChatInterfaceProps {
  project: Project
  messages: Message[]
  onNewMessage: (message: Message) => void
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  project,
  messages,
  onNewMessage
}) => {
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return

    const userMessage: Message = {
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    }

    onNewMessage(userMessage)
    setInputValue('')
    setIsLoading(true)

    try {
      const response = await api.post('/code/api/claude/query', {
        prompt: inputValue,
        project_id: project.id
      })

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.response,
        timestamp: response.data.timestamp
      }

      onNewMessage(assistantMessage)
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      }
      onNewMessage(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="chat-container">
      <div className="messages-area">
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', color: '#666', padding: '40px' }}>
            <h3>Welcome to {project.name}!</h3>
            <p>Start a conversation by typing a message below.</p>
            {project.is_temp && (
              <p style={{ marginTop: '10px', fontSize: '14px' }}>
                This is a temporary session. Use the Save button in the header to keep your work.
              </p>
            )}
          </div>
        )}

        {messages.map((message, index) => (
          <div key={index} className={`message message-${message.role}`}>
            <div className="message-content">
              {message.content}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="message message-assistant">
            <div className="message-content">
              <em>Claude is thinking...</em>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <input
          type="text"
          className="message-input"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <button
          className="send-button"
          onClick={handleSendMessage}
          disabled={!inputValue.trim() || isLoading}
        >
          Send
        </button>
      </div>
    </div>
  )
}

export default ChatInterface