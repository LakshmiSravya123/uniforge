# UniForge - Quick Start Guide

## ✅ Application is Now Running!

The application is successfully running at:
- **Frontend**: http://localhost:5174
- **Backend API**: http://127.0.0.1:5001

---

## 🎯 What's Working

### ✅ Core Features
1. **Todo Management** - Add, view, and drag-to-reorder todos
2. **Pattern Recording** - Record 3-second keyboard patterns
3. **Pattern Replay** - Replay saved patterns
4. **Pattern Storage** - Save patterns locally with names
5. **Export/Import** - Backup and restore your flows
6. **Voice Control** - Voice commands for replay (requires browser permissions)
7. **AI Chat** - Get automation suggestions
8. **Command Palette** - Use Cmd+K (or Ctrl+K) for quick actions

### ✅ Backend Services
- Flask server on port 5001 serving:
  - `/data` - Get saved todos
  - `/save` - Save todos
  - `/record` - Record keyboard patterns
  - `/replay` - Replay patterns

---

## 🚀 How to Use

### 1. Recording a Flow
1. Click "Record Flow" button
2. Wait for 3-second countdown
3. Type your keyboard pattern
4. Enter a name for your pattern
5. Click "Save Flow"

### 2. Replaying a Flow
1. Click on a saved pattern in the sidebar
2. Click "Replay Flow" or use the main "Replay" button

### 3. Managing Todos
1. Type a task in the input box
2. Click "Add"
3. Drag todos to reorder them
4. Todos are automatically saved to the backend

### 4. Using Voice Commands
1. Click "Start Listening"
2. Grant microphone permissions
3. Say "repeat flow" to replay the loaded pattern

### 5. Using Command Palette
1. Press `Cmd+K` (macOS) or `Ctrl+K` (Windows/Linux)
2. Type to filter commands
3. Use arrow keys to select
4. Press Enter to execute

---

## ⚠️ Important Notes

### macOS Accessibility Permissions
The keyboard recording feature **requires** accessibility permissions:

1. Go to **System Settings** → **Privacy & Security** → **Accessibility**
2. Add Python (or your terminal app) to the allowed applications
3. You may need to run with `sudo` for full keyboard access:
   ```bash
   sudo /Users/sravyalu/uniforge/.venv/bin/python run.py
   ```

**Note**: The app works without these permissions, but keyboard recording/replay won't function.

### Optional Features
- **GitHub OAuth** (for auto-deploy): Configure `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` in `.env`
- **Watcher** (auto-deploy trigger): Requires accessibility permissions and sudo

---

## 📁 Project Structure

```
uniforge/
├── run.py                    # Main launcher script
├── .env                      # Environment variables (optional)
├── backend/                  # Original Flask API (not used in current setup)
├── frontend/                 # Vite frontend
│   ├── index.html           # Main UI with all JavaScript
│   ├── package.json         # Frontend dependencies
│   └── vite.config.js       # Vite configuration
├── watcher/                  # Backend services
│   ├── server.py            # Main Flask server (port 5001)
│   ├── auth.py              # GitHub OAuth (optional)
│   ├── watcher.py           # Auto-deploy trigger (optional)
│   ├── recorder.py          # Recording utilities
│   └── replayer.py          # Replay utilities
└── .venv/                    # Python virtual environment
```

---

## 🛠️ How to Start/Stop

### Start the Application
```bash
cd /Users/sravyalu/uniforge
/Users/sravyalu/uniforge/.venv/bin/python run.py
```

Or use the convenience script:
```bash
bash run_all.sh
```

### Stop the Application
Press `Ctrl+C` in the terminal where it's running

Or kill the processes manually:
```bash
pkill -f "python run.py"
for port in 5001 5174 5175; do 
  lsof -ti:$port | xargs kill -9 2>/dev/null || true
done
```

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Kill processes on required ports
lsof -ti:5001 | xargs kill -9
lsof -ti:5174 | xargs kill -9
```

### Keyboard Recording Not Working
1. Check macOS System Settings → Privacy & Security → Accessibility
2. Add Python or Terminal to allowed apps
3. Try running with `sudo`

### Frontend Not Loading
1. Ensure frontend dependencies are installed:
   ```bash
   cd frontend && npm install
   ```
2. Check that Vite is running on port 5174 or 5175
3. Look for error messages in the terminal

### Python Dependencies Missing
```bash
cd /Users/sravyalu/uniforge
/Users/sravyalu/uniforge/.venv/bin/python -m pip install -r backend/requirements.txt
```

---

## 📦 What Was Fixed

1. ✅ Completed the frontend JavaScript implementation
2. ✅ Fixed `watcher/watcher.py` keyboard API usage
3. ✅ Made GitHub OAuth optional (no longer required)
4. ✅ Updated Vite config to proxy all API endpoints
5. ✅ Created unified server.py combining data and recorder endpoints
6. ✅ Made watcher optional (accessibility permissions not required)
7. ✅ Fixed run.py to use correct server and handle errors gracefully
8. ✅ Installed all Python dependencies in virtual environment
9. ✅ Created .env template for optional GitHub OAuth

---

## 🎨 Features Overview

- **Modern UI**: Windsurf-inspired design with teal accents and smooth animations
- **Drag & Drop**: Reorder todos intuitively
- **Keyboard Shortcuts**: Cmd+K command palette
- **Local Storage**: Patterns saved in browser localStorage
- **Backend Sync**: Todos synced to JSON file via Flask API
- **Voice Control**: Hands-free operation with speech recognition
- **AI Suggestions**: Context-aware automation tips
- **Export/Import**: Backup and share your automation flows

---

## 🎉 You're All Set!

Your UniForge application is fully functional and ready to use. Open http://localhost:5174 in your browser and start automating your workflows!

For questions or issues, check the terminal output for error messages.
