# TodoList

> Todo list with categories and due dates

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 🚀 What It Does

Todo list with categories and due dates

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
todolist/
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
cd todolist

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
