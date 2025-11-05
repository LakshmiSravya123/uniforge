# 🔥 CodeForge - Zero-BS Full-Stack Generator

**Generate complete, deployable web apps from a single sentence.**

## What You Get

Every CodeForge project includes:
- ✅ **Complete Frontend** - Vite + React with modern UI
- ✅ **Complete Backend** - Express API with CRUD operations
- ✅ **Database Schema** - Supabase PostgreSQL ready to deploy
- ✅ **Deploy Configs** - Netlify + Render 1-click deploy
- ✅ **Documentation** - Full README with instructions
- ✅ **Local Dev** - Works immediately with `quickstart.sh`

## Quick Start

### Generate Your App

```bash
python codeforge.py "Your app idea here"
```

**Examples:**
```bash
# Todo app
python codeforge.py "A todo list with categories and due dates"

# URL shortener
python codeforge.py "URL shortener with click analytics"

# Recipe manager
python codeforge.py "Recipe manager with search and ratings"

# Habit tracker
python codeforge.py "Track daily habits with streaks"

# Note taking
python codeforge.py "Note taking app with markdown support"
```

### Run Locally (Instant)

```bash
cd generated/your-app-name
./quickstart.sh  # Auto-installs dependencies and starts everything
```

Or manually:
```bash
# Terminal 1 - Backend
cd backend && npm install && npm run dev

# Terminal 2 - Frontend
cd frontend && npm install && npm run dev
```

Open http://localhost:5173 🎉

## Deploy to Production (5 minutes)

### 1. Setup Supabase (2 min)

1. Go to [supabase.com](https://supabase.com)
2. Create new project (free tier)
3. Go to SQL Editor
4. Paste contents of `supabase/schema.sql`
5. Click "Run"
6. Go to Settings → API
7. Copy your `Project URL` and `anon public key`

### 2. Push to GitHub (1 min)

```bash
cd generated/your-app-name
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME
git push -u origin main
```

### 3. Deploy Backend to Render (1 min)

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Settings:
   - **Name**: your-app-backend
   - **Root Directory**: `backend`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
5. Add Environment Variables:
   - `SUPABASE_URL` = your-project-url
   - `SUPABASE_ANON_KEY` = your-anon-key
6. Click "Create Web Service"
7. Wait for deploy (~2 min)
8. Copy your backend URL: `https://your-app.onrender.com`

### 4. Deploy Frontend to Netlify (1 min)

1. Go to [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect to GitHub and select your repo
4. Build settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`
5. Add Environment Variable:
   - `VITE_API_URL` = `https://your-app.onrender.com`
6. Click "Deploy site"
7. Your app is live! 🎉

## Project Structure

```
your-app/
├── frontend/              # React + Vite
│   ├── src/
│   │   ├── App.jsx       # Main component
│   │   ├── main.jsx      # Entry point
│   │   └── index.css     # Styles
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── backend/               # Express API
│   ├── server.js         # API routes
│   ├── package.json
│   └── .env.example
├── supabase/
│   └── schema.sql        # Database schema
├── netlify.toml          # Frontend deploy config
├── render.yaml           # Backend deploy config
├── README.md             # Project-specific docs
└── .gitignore
```

## Customization

### Change Styling

Edit `frontend/src/index.css`:
```css
/* Change primary colors */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Add API Endpoints

Edit `backend/server.js`:
```javascript
app.post('/api/new-endpoint', async (req, res) => {
  // Your logic here
})
```

### Modify Database

Edit `supabase/schema.sql` and re-run in Supabase SQL Editor.

## Tech Stack

| Layer | Technology | Deploy |
|-------|-----------|--------|
| Frontend | Vite + React 18 | Netlify (free) |
| Backend | Node.js + Express | Render (free) |
| Database | Supabase PostgreSQL | Supabase (free) |
| Repo | Git + GitHub | GitHub (free) |

**All tools are 100% free for personal/hobby projects.**

## Features Included

Every generated app has:

✅ **CRUD Operations** - Create, Read, Update, Delete  
✅ **REST API** - Clean RESTful endpoints  
✅ **Modern UI** - Responsive, gradient design  
✅ **Error Handling** - Proper status codes and messages  
✅ **Loading States** - User feedback during operations  
✅ **Environment Variables** - Secure configuration  
✅ **CORS Enabled** - Cross-origin requests configured  
✅ **Row-Level Security** - Supabase RLS policies  
✅ **Auto-Deploy** - Push to deploy workflow  

## Advanced Usage

### Generate with Custom Output Directory

```bash
python codeforge.py "Your idea" --output ~/projects/my-app
```

### Generate Multiple Apps

```bash
python codeforge.py "Todo app"
python codeforge.py "Recipe manager"
python codeforge.py "URL shortener"
# Each gets its own directory in generated/
```

### Use as Template

1. Generate base app: `python codeforge.py "Base CRUD app"`
2. Customize frontend components
3. Add your specific features
4. Deploy!

## Troubleshooting

**Port already in use?**
```bash
# Kill processes on ports 5001 and 5173
lsof -ti:5001 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

**CORS errors?**
- Check `VITE_API_URL` is set in Netlify
- Verify `netlify.toml` has correct backend URL

**Database connection fails?**
- Verify Supabase credentials in `backend/.env`
- Check you ran the schema.sql in Supabase

**Build fails on Netlify?**
- Make sure `frontend/` is the base directory
- Check build command: `npm run build`
- Publish directory: `dist`

**API 502 errors on Render?**
- Check backend logs in Render dashboard
- Verify environment variables are set
- Make sure start command is `npm start`

## What Makes This Different?

| Feature | CodeForge | Other Generators |
|---------|-----------|-----------------|
| **Setup Time** | 0 seconds | 30+ min config |
| **Questions Asked** | 0 | 10-20 prompts |
| **Deploy Ready** | ✅ Yes | ❌ Manual setup |
| **Database Included** | ✅ Yes | ❌ DIY |
| **Works Locally** | ✅ Instant | ⚠️ Docker needed |
| **Free Hosting** | ✅ Included | ❌ Pay or DIY |
| **Full Code** | ✅ Readable | ⚠️ Generated mess |

## Roadmap

Coming soon:
- [ ] Python/FastAPI backend option
- [ ] Vue.js frontend option
- [ ] Authentication templates
- [ ] File upload support
- [ ] Email integration
- [ ] Payment processing (Stripe)
- [ ] Admin dashboard generation
- [ ] Mobile-responsive templates
- [ ] Dark mode toggle
- [ ] Multi-language support

## Examples

Check `examples/` directory for pre-generated apps:
- Todo List
- URL Shortener
- Recipe Manager
- Habit Tracker
- Note Taking App

## Contributing

Have ideas? Found bugs?
1. Open an issue
2. Submit a PR
3. Star the repo ⭐

## License

MIT - Do whatever you want!

---

**Made with ❤️ by CodeForge**  
*Generate → Deploy → Ship*  
*In under 5 minutes.*
