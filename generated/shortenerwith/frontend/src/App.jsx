import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || '/api'

function App() {
  const [data, setData] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState(null)

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
      setStatus({ type: 'success', message: 'Added successfully!' })
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
      setStatus({ type: 'success', message: 'Deleted successfully!' })
    } catch (error) {
      setStatus({ type: 'error', message: 'Failed to delete' })
    }
  }

  return (
    <div className="app">
      <div className="card">
        <h1>ShortenerWith</h1>
        <p style={{ color: '#666', marginBottom: '2rem' }}>
          URL shortener with click analytics
        </p>

        {status && (
          <div className={`status ${status.type}`}>
            {status.message}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter something..."
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            {loading ? <span className="loading"></span> : 'Submit'}
          </button>
        </form>
      </div>

      <div className="card">
        <h2>Items ({data.length})</h2>
        {data.length === 0 ? (
          <p style={{ color: '#666', textAlign: 'center', padding: '2rem' }}>
            No items yet. Add one above!
          </p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {data.map(item => (
              <div
                key={item.id}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '1rem',
                  background: '#f8f9fa',
                  borderRadius: '8px'
                }}
              >
                <span>{item.content}</span>
                <button
                  onClick={() => handleDelete(item.id)}
                  style={{ background: '#dc3545' }}
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
