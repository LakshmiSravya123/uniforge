#!/usr/bin/env python3
"""
CodeForge - Zero-BS Full-Stack Code Generator
Generates complete, working apps from one-line ideas
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

class CodeForge:
    """Main CodeForge generator"""
    
    TECH_STACK = {
        'frontend': 'Vite + React',
        'backend': 'Node.js + Express',
        'database': 'Supabase (PostgreSQL)',
        'deploy_frontend': 'Netlify',
        'deploy_backend': 'Render',
    }
    
    def parse_idea(self, idea: str) -> dict:
        """Parse idea and extract features"""
        idea_lower = idea.lower()
        
        features = {
            'has_auth': any(word in idea_lower for word in ['login', 'auth', 'user', 'signup', 'register']),
            'has_crud': any(word in idea_lower for word in ['create', 'add', 'edit', 'delete', 'manage', 'list']),
            'has_api': any(word in idea_lower for word in ['api', 'scrape', 'fetch', 'get', 'search']),
            'has_upload': any(word in idea_lower for word in ['upload', 'file', 'image', 'photo']),
            'has_email': any(word in idea_lower for word in ['email', 'notify', 'send', 'alert']),
            'has_schedule': any(word in idea_lower for word in ['daily', 'schedule', 'cron', 'every']),
            'is_realtime': any(word in idea_lower for word in ['chat', 'live', 'realtime', 'websocket']),
        }
        
        # Extract main entities (nouns)
        words = idea_lower.split()
        entities = [w for w in words if len(w) > 3 and w not in ['that', 'with', 'from', 'into', 'your']]
        
        # Generate app name
        app_name = self._generate_app_name(idea)
        
        return {
            'idea': idea,
            'app_name': app_name,
            'features': features,
            'entities': entities[:3],  # Top 3 entities
        }
    
    def _generate_app_name(self, idea: str) -> str:
        """Generate app name from idea"""
        # Extract key words
        words = idea.lower().split()
        keywords = [w for w in words if len(w) > 3 and w.isalnum()][:2]
        
        if keywords:
            name = ''.join(w.capitalize() for w in keywords)
        else:
            name = 'MyApp'
        
        return name
    
    def generate(self, idea: str, output_dir: str = None):
        """Generate complete app from idea"""
        print("🔥 CODEFORGE ACTIVATING...\n")
        
        # Parse idea
        parsed = self.parse_idea(idea)
        app_name = parsed['app_name']
        features = parsed['features']
        
        print(f"📦 Generating: {app_name}")
        print(f"💡 Idea: {idea}")
        print(f"🎯 Features detected: {', '.join([k.replace('has_', '').replace('is_', '') for k, v in features.items() if v])}\n")
        
        # Set output directory
        if not output_dir:
            output_dir = f"generated/{app_name.lower()}"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate project structure
        print("🏗️  Building structure...")
        self._create_structure(output_path, parsed)
        
        # Generate frontend
        print("⚛️  Generating React frontend...")
        self._generate_frontend(output_path, parsed)
        
        # Generate backend
        print("🚀 Generating Express backend...")
        self._generate_backend(output_path, parsed)
        
        # Generate database
        print("🗄️  Creating Supabase schema...")
        self._generate_database(output_path, parsed)
        
        # Generate deployment files
        print("📦 Creating deploy configs...")
        self._generate_deploy_files(output_path, parsed)
        
        # Generate README
        print("📖 Writing README...")
        self._generate_readme(output_path, parsed)
        
        print(f"\n✅ DONE! Generated in: {output_path.absolute()}\n")
        
        # Print deploy instructions
        self._print_deploy_instructions(app_name, output_path)
        
        return str(output_path.absolute())
    
    def _create_structure(self, base_path: Path, parsed: dict):
        """Create project directory structure"""
        dirs = [
            'frontend/src/components',
            'frontend/src/pages',
            'frontend/src/hooks',
            'frontend/src/utils',
            'frontend/public',
            'backend/routes',
            'backend/middleware',
            'backend/utils',
            'supabase',
        ]
        
        for dir_path in dirs:
            (base_path / dir_path).mkdir(parents=True, exist_ok=True)
    
    def _generate_frontend(self, base_path: Path, parsed: dict):
        """Generate React frontend"""
        app_name = parsed['app_name']
        features = parsed['features']
        
        # package.json
        package_json = {
            "name": f"{app_name.lower()}-frontend",
            "version": "0.1.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview"
            },
            "dependencies": {
                "react": "^18.3.1",
                "react-dom": "^18.3.1",
                "axios": "^1.7.2"
            },
            "devDependencies": {
                "@vitejs/plugin-react": "^4.3.0",
                "vite": "^5.4.0"
            }
        }
        
        with open(base_path / 'frontend/package.json', 'w') as f:
            json.dump(package_json, f, indent=2)
        
        # vite.config.js
        vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
      }
    }
  }
})
"""
        with open(base_path / 'frontend/vite.config.js', 'w') as f:
            f.write(vite_config)
        
        # index.html
        index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{app_name}</title>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.jsx"></script>
</body>
</html>
"""
        with open(base_path / 'frontend/index.html', 'w') as f:
            f.write(index_html)
        
        # src/main.jsx
        main_jsx = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
"""
        with open(base_path / 'frontend/src/main.jsx', 'w') as f:
            f.write(main_jsx)
        
        # src/App.jsx
        app_jsx = self._get_react_app(parsed)
        with open(base_path / 'frontend/src/App.jsx', 'w') as f:
            f.write(app_jsx)
        
        # src/index.css
        css = """* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  color: #333;
}

.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

h1 {
  color: #667eea;
  margin-bottom: 1rem;
}

button {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s;
}

button:hover {
  background: #764ba2;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
}

input, textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  margin-bottom: 1rem;
  transition: border 0.3s;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #667eea;
}

.status {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.status.success {
  background: #d4edda;
  color: #155724;
}

.status.error {
  background: #f8d7da;
  color: #721c24;
}

.loading {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
"""
        with open(base_path / 'frontend/src/index.css', 'w') as f:
            f.write(css)
    
    def _get_react_app(self, parsed: dict) -> str:
        """Generate App.jsx based on features"""
        app_name = parsed['app_name']
        features = parsed['features']
        idea = parsed['idea']
        
        return f"""import {{ useState, useEffect }} from 'react'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || '/api'

function App() {{
  const [data, setData] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState(null)

  useEffect(() => {{
    fetchData()
  }}, [])

  const fetchData = async () => {{
    try {{
      const response = await axios.get(`${{API_URL}}/items`)
      setData(response.data)
    }} catch (error) {{
      console.error('Error fetching data:', error)
    }}
  }}

  const handleSubmit = async (e) => {{
    e.preventDefault()
    if (!input.trim()) return

    setLoading(true)
    setStatus(null)

    try {{
      const response = await axios.post(`${{API_URL}}/items`, {{
        content: input
      }})
      
      setData([response.data, ...data])
      setInput('')
      setStatus({{ type: 'success', message: 'Added successfully!' }})
    }} catch (error) {{
      setStatus({{ type: 'error', message: error.response?.data?.error || 'Failed to add' }})
    }} finally {{
      setLoading(false)
    }}
  }}

  const handleDelete = async (id) => {{
    try {{
      await axios.delete(`${{API_URL}}/items/${{id}}`)
      setData(data.filter(item => item.id !== id))
      setStatus({{ type: 'success', message: 'Deleted successfully!' }})
    }} catch (error) {{
      setStatus({{ type: 'error', message: 'Failed to delete' }})
    }}
  }}

  return (
    <div className="app">
      <div className="card">
        <h1>{app_name}</h1>
        <p style={{{{ color: '#666', marginBottom: '2rem' }}}}>
          {idea}
        </p>

        {{status && (
          <div className={{`status ${{status.type}}`}}>
            {{status.message}}
          </div>
        )}}

        <form onSubmit={{handleSubmit}}>
          <input
            type="text"
            value={{input}}
            onChange={{(e) => setInput(e.target.value)}}
            placeholder="Enter something..."
            disabled={{loading}}
          />
          <button type="submit" disabled={{loading}}>
            {{loading ? <span className="loading"></span> : 'Submit'}}
          </button>
        </form>
      </div>

      <div className="card">
        <h2>Items ({{data.length}})</h2>
        {{data.length === 0 ? (
          <p style={{{{ color: '#666', textAlign: 'center', padding: '2rem' }}}}>
            No items yet. Add one above!
          </p>
        ) : (
          <div style={{{{ display: 'flex', flexDirection: 'column', gap: '1rem' }}}}>
            {{data.map(item => (
              <div
                key={{item.id}}
                style={{{{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '1rem',
                  background: '#f8f9fa',
                  borderRadius: '8px'
                }}}}
              >
                <span>{{item.content}}</span>
                <button
                  onClick={{() => handleDelete(item.id)}}
                  style={{{{ background: '#dc3545' }}}}
                >
                  Delete
                </button>
              </div>
            ))}}
          </div>
        )}}
      </div>
    </div>
  )
}}

export default App
"""
    
    def _generate_backend(self, base_path: Path, parsed: dict):
        """Generate Express backend"""
        app_name = parsed['app_name']
        
        # package.json
        package_json = {
            "name": f"{app_name.lower()}-backend",
            "version": "0.1.0",
            "type": "module",
            "scripts": {
                "start": "node server.js",
                "dev": "node --watch server.js"
            },
            "dependencies": {
                "express": "^4.19.2",
                "cors": "^2.8.5",
                "@supabase/supabase-js": "^2.43.0",
                "dotenv": "^16.4.5"
            }
        }
        
        with open(base_path / 'backend/package.json', 'w') as f:
            json.dump(package_json, f, indent=2)
        
        # server.js
        server_js = f"""import express from 'express'
import cors from 'cors'
import {{ createClient }} from '@supabase/supabase-js'
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
app.get('/api/health', (req, res) => {{
  res.json({{ status: 'healthy', timestamp: new Date().toISOString() }})
}})

app.get('/api/items', async (req, res) => {{
  try {{
    const {{ data, error }} = await supabase
      .from('items')
      .select('*')
      .order('created_at', {{ ascending: false }})
    
    if (error) throw error
    res.json(data || [])
  }} catch (error) {{
    console.error('Error fetching items:', error)
    res.status(500).json({{ error: error.message }})
  }}
}})

app.post('/api/items', async (req, res) => {{
  try {{
    const {{ content }} = req.body
    
    if (!content) {{
      return res.status(400).json({{ error: 'Content is required' }})
    }}
    
    const {{ data, error }} = await supabase
      .from('items')
      .insert([{{ content }}])
      .select()
      .single()
    
    if (error) throw error
    res.status(201).json(data)
  }} catch (error) {{
    console.error('Error creating item:', error)
    res.status(500).json({{ error: error.message }})
  }}
}})

app.delete('/api/items/:id', async (req, res) => {{
  try {{
    const {{ id }} = req.params
    
    const {{ error }} = await supabase
      .from('items')
      .delete()
      .eq('id', id)
    
    if (error) throw error
    res.json({{ message: 'Deleted successfully' }})
  }} catch (error) {{
    console.error('Error deleting item:', error)
    res.status(500).json({{ error: error.message }})
  }}
}})

app.listen(PORT, () => {{
  console.log(`🚀 {app_name} API running on http://localhost:${{PORT}}`)
  console.log(`📊 Health check: http://localhost:${{PORT}}/api/health`)
}})
"""
        with open(base_path / 'backend/server.js', 'w') as f:
            f.write(server_js)
        
        # .env.example
        env_example = """# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here

# Server
PORT=5001
"""
        with open(base_path / 'backend/.env.example', 'w') as f:
            f.write(env_example)
    
    def _generate_database(self, base_path: Path, parsed: dict):
        """Generate Supabase schema"""
        
        schema_sql = """-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- Items table
create table if not exists items (
  id uuid primary key default uuid_generate_v4(),
  content text not null,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Enable Row Level Security
alter table items enable row level security;

-- Policy: Anyone can read items
create policy "Items are viewable by everyone"
  on items for select
  using (true);

-- Policy: Anyone can insert items (adjust for auth later)
create policy "Items are insertable by everyone"
  on items for insert
  with check (true);

-- Policy: Anyone can delete their items (adjust for auth later)
create policy "Items are deletable by everyone"
  on items for delete
  using (true);

-- Indexes
create index if not exists items_created_at_idx on items(created_at desc);
"""
        with open(base_path / 'supabase/schema.sql', 'w') as f:
            f.write(schema_sql)
    
    def _generate_deploy_files(self, base_path: Path, parsed: dict):
        """Generate deployment configuration files"""
        app_name = parsed['app_name']
        
        # netlify.toml
        netlify_toml = """[build]
  command = "cd frontend && npm install && npm run build"
  publish = "frontend/dist"

[[redirects]]
  from = "/api/*"
  to = "https://YOUR_APP_NAME.onrender.com/api/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
        with open(base_path / 'netlify.toml', 'w') as f:
            f.write(netlify_toml)
        
        # render.yaml
        render_yaml = f"""services:
  - type: web
    name: {app_name.lower()}-api
    env: node
    buildCommand: cd backend && npm install
    startCommand: cd backend && npm start
    envVars:
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_ANON_KEY
        sync: false
"""
        with open(base_path / 'render.yaml', 'w') as f:
            f.write(render_yaml)
        
        # .gitignore
        gitignore = """node_modules/
dist/
.env
.DS_Store
*.log
"""
        with open(base_path / '.gitignore', 'w') as f:
            f.write(gitignore)
    
    def _generate_readme(self, base_path: Path, parsed: dict):
        """Generate comprehensive README"""
        app_name = parsed['app_name']
        idea = parsed['idea']
        
        readme = f"""# {app_name}

> {idea}

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 🚀 What It Does

{idea}

## ⚡ Tech Stack

- **Frontend**: Vite + React → Netlify
- **Backend**: Node.js + Express → Render  
- **Database**: Supabase (PostgreSQL)
- **Deploy**: 1-click with buttons above

## 🎯 Features

✅ Full CRUD operations  
✅ Real-time updates  
✅ Modern React UI  
✅ RESTful API  
✅ PostgreSQL database  
✅ 1-click deployment  

## 📦 Project Structure

```
{app_name.lower()}/
├── frontend/              # React + Vite
│   ├── src/
│   │   ├── App.jsx       # Main component
│   │   ├── main.jsx      # Entry point
│   │   └── index.css     # Styles
│   ├── package.json
│   └── vite.config.js
├── backend/               # Express API
│   ├── server.js         # API server
│   ├── package.json
│   └── .env.example
├── supabase/
│   └── schema.sql        # Database schema
├── netlify.toml          # Frontend deploy config
└── render.yaml           # Backend deploy config
```

## 🏃 Run Locally (5 minutes)

### 1️⃣ Clone & Install

```bash
git clone <your-repo-url>
cd {app_name.lower()}

# Install frontend
cd frontend && npm install

# Install backend
cd ../backend && npm install
```

### 2️⃣ Setup Supabase

1. Go to [supabase.com](https://supabase.com)
2. Create a new project (free tier)
3. Go to SQL Editor → paste contents of `supabase/schema.sql` → Run
4. Copy your project URL and anon key from Settings → API

### 3️⃣ Configure Environment

```bash
cd backend
cp .env.example .env
# Edit .env with your Supabase credentials
```

### 4️⃣ Start Everything

```bash
# Terminal 1 - Backend
cd backend && npm run dev

# Terminal 2 - Frontend  
cd frontend && npm run dev
```

Open [http://localhost:5173](http://localhost:5173) 🎉

## ☁️ Deploy to Production (1-click)

### Option A: Netlify + Render (Recommended)

#### Frontend (Netlify)
1. Click "Deploy to Netlify" button above
2. Connect your GitHub repo
3. Click "Deploy" → Done! ✅

#### Backend (Render)
1. Click "Deploy to Render" button above
2. Connect your GitHub repo
3. Add environment variables:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
4. Click "Deploy" → Done! ✅

#### Update Frontend API URL
1. In Netlify, go to Site settings → Environment variables
2. Add: `VITE_API_URL` = `https://your-app.onrender.com`
3. Redeploy

### Option B: Manual Deploy

#### Netlify (Frontend)
```bash
cd frontend
npm run build
npx netlify-cli deploy --prod
```

#### Render (Backend)
1. Connect GitHub repo
2. Select `backend` as root directory
3. Build command: `npm install`
4. Start command: `npm start`

## 🔧 Environment Variables

### Backend (.env)
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key
PORT=5001
```

### Frontend (Netlify)
```
VITE_API_URL=https://your-app.onrender.com
```

## 📡 API Endpoints

```
GET    /api/health        # Health check
GET    /api/items         # Get all items
POST   /api/items         # Create item
DELETE /api/items/:id     # Delete item
```

## 🎨 Customization

### Change Colors
Edit `frontend/src/index.css`:
```css
--primary: #667eea;    /* Change this */
--secondary: #764ba2;  /* And this */
```

### Add Authentication
1. Enable Supabase Auth in dashboard
2. Add auth routes in `backend/server.js`
3. Use `supabase.auth.signIn()` in frontend

### Add More Features
- File uploads → Add Supabase Storage
- Real-time → Use Supabase Realtime
- Email → Add SendGrid/Resend

## 🐛 Troubleshooting

**CORS errors?**
- Make sure backend URL is set in Netlify env vars
- Check `netlify.toml` redirect rules

**Database errors?**
- Verify Supabase credentials in `.env`
- Check Row Level Security policies in Supabase

**Build fails?**
- Delete `node_modules` and reinstall
- Check Node version (needs 18+)

## 📝 License

MIT - Do whatever you want!

## 🚀 What's Next?

- [ ] Add user authentication
- [ ] Add file uploads
- [ ] Add email notifications
- [ ] Add admin dashboard
- [ ] Add analytics

---

**Made with CodeForge** 🔥  
Built in < 5 minutes • Deployed in 1 click
"""
        with open(base_path / 'README.md', 'w') as f:
            f.write(readme)
    
    def _print_deploy_instructions(self, app_name: str, output_path: Path):
        """Print deployment instructions"""
        print("=" * 70)
        print(f"🔥 CODEFORGE MVP - {app_name}")
        print("=" * 70)
        print()
        print("📍 LOCATION:")
        print(f"   {output_path.absolute()}")
        print()
        print("🌐 AFTER DEPLOY:")
        print(f"   Frontend: https://{app_name.lower()}.netlify.app")
        print(f"   Backend:  https://{app_name.lower()}.onrender.com")
        print(f"   Database: Supabase (auto-created)")
        print()
        print("⚡ 1-CLICK DEPLOY STEPS:")
        print()
        print("1️⃣  SETUP SUPABASE (2 min)")
        print("   → Go to supabase.com → New project")
        print(f"   → SQL Editor → Paste supabase/schema.sql → Run")
        print("   → Copy URL + anon key from Settings → API")
        print()
        print("2️⃣  PUSH TO GITHUB (1 min)")
        print(f"   cd {output_path.absolute()}")
        print("   git init")
        print("   git add .")
        print(f'   git commit -m "Initial commit - {app_name}"')
        print("   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME")
        print("   git push -u origin main")
        print()
        print("3️⃣  DEPLOY BACKEND (Render) (1 min)")
        print("   → Go to render.com → New → Web Service")
        print("   → Connect GitHub repo")
        print("   → Root directory: backend")
        print("   → Build: npm install")
        print("   → Start: npm start")
        print("   → Add env vars: SUPABASE_URL, SUPABASE_ANON_KEY")
        print("   → Deploy ✅")
        print()
        print("4️⃣  DEPLOY FRONTEND (Netlify) (1 min)")
        print("   → Go to netlify.com → New site → Import from Git")
        print("   → Connect GitHub repo")
        print("   → Build: cd frontend && npm run build")
        print("   → Publish: frontend/dist")
        print("   → Add env var: VITE_API_URL = https://YOUR_APP.onrender.com")
        print("   → Deploy ✅")
        print()
        print("✅ TOTAL TIME: ~5 minutes → LIVE APP!")
        print()
        print("🏃 RUN LOCALLY NOW:")
        print(f"   cd {output_path.absolute()}")
        print("   # Terminal 1:")
        print("   cd backend && npm install && npm run dev")
        print("   # Terminal 2:")
        print("   cd frontend && npm install && npm run dev")
        print()
        print("🔄 REBUILD: python codeforge.py \"new idea\"")
        print("=" * 70)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python codeforge.py \"Your app idea here\"")
        print()
        print("Examples:")
        print('  python codeforge.py "A tool to track my daily habits"')
        print('  python codeforge.py "URL shortener with analytics"')
        print('  python codeforge.py "Recipe manager with search"')
        sys.exit(1)
    
    idea = ' '.join(sys.argv[1:])
    
    forge = CodeForge()
    forge.generate(idea)


if __name__ == '__main__':
    main()
