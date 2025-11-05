import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'

dotenv.config()

const app = express()
const PORT = process.env.PORT || 5001

// In-memory storage (for demo - replace with Supabase when ready)
let tasks = []
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
    res.json(tasks)
  } catch (error) {
    console.error('Error fetching tasks:', error)
    res.status(500).json({ error: error.message })
  }
})

app.post('/api/items', async (req, res) => {
  try {
    const { content } = req.body
    
    if (!content) {
      return res.status(400).json({ error: 'Content is required' })
    }
    
    const newTask = {
      id: String(nextId++),
      content,
      pomodoros: 0,
      completed: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
    
    tasks.unshift(newTask)
    res.status(201).json(newTask)
  } catch (error) {
    console.error('Error creating task:', error)
    res.status(500).json({ error: error.message })
  }
})

app.patch('/api/items/:id', async (req, res) => {
  try {
    const { id } = req.params
    const { pomodoros, completed } = req.body
    
    const task = tasks.find(t => t.id === id)
    if (!task) {
      return res.status(404).json({ error: 'Task not found' })
    }
    
    if (pomodoros !== undefined) task.pomodoros = pomodoros
    if (completed !== undefined) task.completed = completed
    task.updated_at = new Date().toISOString()
    
    res.json(task)
  } catch (error) {
    console.error('Error updating task:', error)
    res.status(500).json({ error: error.message })
  }
})

app.delete('/api/items/:id', async (req, res) => {
  try {
    const { id } = req.params
    
    const initialLength = tasks.length
    tasks = tasks.filter(task => task.id !== id)
    
    if (tasks.length === initialLength) {
      return res.status(404).json({ error: 'Task not found' })
    }
    
    res.json({ message: 'Deleted successfully' })
  } catch (error) {
    console.error('Error deleting task:', error)
    res.status(500).json({ error: error.message })
  }
})

app.listen(PORT, () => {
  console.log(`🍅 PomodoroTimer API running on http://localhost:${PORT}`)
  console.log(`📊 Health check: http://localhost:${PORT}/api/health`)
  console.log(`💾 Using in-memory storage (add Supabase credentials to use database)`)
})
