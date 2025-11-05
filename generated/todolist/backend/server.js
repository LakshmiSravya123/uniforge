import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'

dotenv.config()

const app = express()
const PORT = process.env.PORT || 5001

// In-memory storage (for demo - replace with Supabase when ready)
let items = []
let nextId = 1

// Middleware
app.use(cors())
app.use(express.json())

// Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() })
})

app.get('/api/items', async (req, res) => {
  try {
    // Return in-memory items
    res.json(items)
  } catch (error) {
    console.error('Error fetching items:', error)
    res.status(500).json({ error: error.message })
  }
})

app.post('/api/items', async (req, res) => {
  try {
    const { content } = req.body
    
    if (!content) {
      return res.status(400).json({ error: 'Content is required' })
    }
    
    const newItem = {
      id: String(nextId++),
      content,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    
    items.unshift(newItem)
    res.status(201).json(newItem)
  } catch (error) {
    console.error('Error creating item:', error)
    res.status(500).json({ error: error.message })
  }
})

app.delete('/api/items/:id', async (req, res) => {
  try {
    const { id } = req.params
    
    const initialLength = items.length
    items = items.filter(item => item.id !== id)
    
    if (items.length === initialLength) {
      return res.status(404).json({ error: 'Item not found' })
    }
    
    res.json({ message: 'Deleted successfully' })
  } catch (error) {
    console.error('Error deleting item:', error)
    res.status(500).json({ error: error.message })
  }
})

app.listen(PORT, () => {
  console.log(`🚀 TodoList API running on http://localhost:${PORT}`)
  console.log(`📊 Health check: http://localhost:${PORT}/api/health`)
  console.log(`💾 Using in-memory storage (add Supabase credentials to use database)`)
})
