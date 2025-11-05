import express from 'express'
import cors from 'cors'
import { createClient } from '@supabase/supabase-js'
import dotenv from 'dotenv'

dotenv.config()

const app = express()
const PORT = process.env.PORT || 5001

// Supabase client
const supabase = createClient(
  process.env.SUPABASE_URL || 'https://your-project.supabase.co',
  process.env.SUPABASE_ANON_KEY || 'your-anon-key'
)

// Middleware
app.use(cors())
app.use(express.json())

// Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() })
})

app.get('/api/items', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('items')
      .select('*')
      .order('created_at', { ascending: false })
    
    if (error) throw error
    res.json(data || [])
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
    
    const { data, error } = await supabase
      .from('items')
      .insert([{ content }])
      .select()
      .single()
    
    if (error) throw error
    res.status(201).json(data)
  } catch (error) {
    console.error('Error creating item:', error)
    res.status(500).json({ error: error.message })
  }
})

app.delete('/api/items/:id', async (req, res) => {
  try {
    const { id } = req.params
    
    const { error } = await supabase
      .from('items')
      .delete()
      .eq('id', id)
    
    if (error) throw error
    res.json({ message: 'Deleted successfully' })
  } catch (error) {
    console.error('Error deleting item:', error)
    res.status(500).json({ error: error.message })
  }
})

app.listen(PORT, () => {
  console.log(`🚀 ShortenerWith API running on http://localhost:${PORT}`)
  console.log(`📊 Health check: http://localhost:${PORT}/api/health`)
})
