# UniForge

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)
![Status](https://img.shields.io/badge/status-production-brightgreen.svg)

**🔥 Two Powerful Tools in One Repo:**

1. **UniForge Automation** - Smart desktop workflow automation with keyboard recording/replay
2. **CodeForge Generator** - Generate complete full-stack web apps from a single sentence

---

## 🔥 CodeForge - Full-Stack App Generator

**Build production-ready web apps in under 5 minutes.**

### What You Get

Every CodeForge project includes:
- ✅ **Complete Frontend** - Vite + React with modern UI
- ✅ **Complete Backend** - Express API with CRUD operations
- ✅ **Database Schema** - Supabase PostgreSQL ready to deploy
- ✅ **Deploy Configs** - Netlify + Render 1-click deploy
- ✅ **Documentation** - Full README with instructions
- ✅ **Local Dev** - Works immediately with quickstart script

### Quick Start

```bash
# Generate any app you can describe
python codeforge.py "Your app idea here"

# Examples:
python codeforge.py "A todo list with categories"
python codeforge.py "URL shortener with analytics"
python codeforge.py "Recipe manager with search"

# Run locally
cd generated/your-app-name
bash ../quickstart.sh
```

### What Gets Generated

```
your-app/
├── frontend/          # Vite + React
├── backend/           # Node.js + Express
├── supabase/          # PostgreSQL schema
├── netlify.toml       # Frontend deploy config
├── render.yaml        # Backend deploy config
└── README.md          # Full instructions
```

### Deploy in 5 Minutes

1. **Supabase** (2 min) - Create project, run schema.sql
2. **GitHub** (1 min) - Push your code
3. **Render** (1 min) - Connect repo, add env vars
4. **Netlify** (1 min) - Connect repo, set API URL

**→ Live at https://your-app.netlify.app** 🎉

**[📖 Full CodeForge Documentation](./CODEFORGE.md)**

---

## 🚀 UniForge Automation

Automate repetitive desktop workflows by capturing keyboard patterns and replaying them through a unified desktop experience.

---

## 🚀 Features

### Core Automation
1. **Smart Keystroke Recorder** - Capture keyboard patterns with configurable duration (1-30s)
2. **Instant Replay** - Replay patterns on-demand or via global hotkeys
3. **Server-Side Storage** - Patterns saved to backend (no localStorage limits)
4. **Global Hotkeys** - Trigger flows system-wide (e.g., `ctrl+shift+p`)
5. **Pattern Management** - Create, edit, delete, export/import flows

### Advanced Capabilities
6. **Todo Management** - Track tasks with drag-&-drop reordering
7. **Voice Control** - Hands-free replay via speech recognition
8. **AI Chat Assistant** - Get smart automation suggestions
9. **Command Palette** - Quick actions via Cmd+K (like VSCode/Cursor)
10. **Export/Import** - Backup and share your automation flows
11. **Health Monitoring** - Backend health checks and status API

### What Makes UniForge Better Than Cursor/Windsurf AI Agents?
- ✅ **Full System Control**: Record/replay ANY keyboard input (not just code)
- ✅ **Offline-First**: Works without internet after setup
- ✅ **Privacy**: All data stays local (patterns stored on your machine)
- ✅ **Customizable**: Open-source Python/JavaScript stack
- ✅ **Global Hotkeys**: Trigger automations from ANY app
- ✅ **Multi-Purpose**: Beyond coding - automate emails, data entry, gaming, etc.

---

## Quick Start

```bash
# Clone and setup
git clone https://github.com/LakshmiSravya123/uniforge.git
cd uniforge

# Install dependencies
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..

# Start the application
python run.py
```

Open **http://localhost:5174** in your browser!

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Server health check |
| `/data` | GET | Get todos |
| `/save` | POST | Save todos |
| `/patterns` | GET | Get all patterns |
| `/patterns` | POST | Save/update pattern |
| `/patterns/<name>` | DELETE | Delete pattern |
| `/record` | POST | Record 3-second keystroke pattern |
| `/replay` | POST | Replay pattern |
| `/replay/name/<name>` | GET/POST | Replay named pattern |
| `/hotkey/register` | POST | Register global hotkey |

---

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Detailed usage guide
- **[WORKING_STATUS.md](WORKING_STATUS.md)** - Current status & fixes
- **[setup_permissions.sh](setup_permissions.sh)** - macOS permissions helper

---

## License

MIT - See LICENSE file for details
