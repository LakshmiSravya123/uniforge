import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || '/api'

function App() {
  const [data, setData] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState(null)
  const [activeView, setActiveView] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const response = await axios.get(`${API_URL}/items`)
      setData(response.data)
    } catch (error) {
      console.error('Error fetching data:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    setLoading(true)
    setStatus(null)

    try {
      const response = await axios.post(`${API_URL}/items`, {
        content: input
      })
      
      setData([response.data, ...data])
      setInput('')
      setStatus({ type: 'success', message: '✓ Task added' })
      setTimeout(() => setStatus(null), 3000)
    } catch (error) {
      setStatus({ type: 'error', message: error.response?.data?.error || 'Failed to add' })
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API_URL}/items/${id}`)
      setData(data.filter(item => item.id !== id))
      setStatus({ type: 'success', message: '✓ Task deleted' })
      setTimeout(() => setStatus(null), 3000)
    } catch (error) {
      setStatus({ type: 'error', message: 'Failed to delete' })
    }
  }

  const filteredData = data.filter(item => 
    item.content.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="logo">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="9 11 12 14 22 4"></polyline>
              <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
            </svg>
            <span>TodoList</span>
          </div>
        </div>

        <nav className="sidebar-nav">
          <button 
            className={`nav-item ${activeView === 'all' ? 'active' : ''}`}
            onClick={() => setActiveView('all')}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            </svg>
            All Tasks
            <span className="count">{data.length}</span>
          </button>
          
          <button 
            className={`nav-item ${activeView === 'today' ? 'active' : ''}`}
            onClick={() => setActiveView('today')}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            Today
          </button>

          <button 
            className={`nav-item ${activeView === 'important' ? 'active' : ''}`}
            onClick={() => setActiveView('important')}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
            Important
          </button>
        </nav>

        <div className="sidebar-footer">
          <div className="user-info">
            <div className="avatar">U</div>
            <span>User</span>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {/* Header */}
        <header className="header">
          <h1 className="page-title">
            {activeView === 'all' ? 'All Tasks' : activeView === 'today' ? 'Today' : 'Important'}
          </h1>
          <div className="header-actions">
            <div className="search-box">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
              </svg>
              <input 
                type="text" 
                placeholder="Search tasks..." 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>
        </header>

        {/* Status Messages */}
        {status && (
          <div className={`status-toast ${status.type}`}>
            {status.message}
          </div>
        )}

        {/* Add Task Form */}
        <div className="add-task-section">
          <form onSubmit={handleSubmit} className="add-task-form">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Add a new task..."
              disabled={loading}
              className="task-input"
            />
            <button type="submit" disabled={loading} className="add-btn">
              {loading ? (
                <span className="spinner"></span>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
              )}
            </button>
          </form>
        </div>

        {/* Tasks List */}
        <div className="tasks-container">
          {filteredData.length === 0 ? (
            <div className="empty-state">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1">
                <polyline points="9 11 12 14 22 4"></polyline>
                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
              </svg>
              <h3>No tasks yet</h3>
              <p>{searchQuery ? 'No tasks match your search' : 'Add your first task to get started'}</p>
            </div>
          ) : (
            <div className="tasks-list">
              {filteredData.map(item => (
                <div key={item.id} className="task-item">
                  <div className="task-checkbox">
                    <input type="checkbox" id={`task-${item.id}`} />
                    <label htmlFor={`task-${item.id}`}></label>
                  </div>
                  <div className="task-content">
                    <span className="task-text">{item.content}</span>
                    <span className="task-meta">Created {new Date(item.created_at).toLocaleDateString()}</span>
                  </div>
                  <button
                    onClick={() => handleDelete(item.id)}
                    className="delete-btn"
                    title="Delete task"
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default App
