# UniForge

Automate repetitive desktop workflows by capturing keyboard patterns and replaying them through a unified desktop experience. UniForge is an intelligent automation tool that goes beyond simple macro recording - it offers server-side pattern storage, global hotkey triggers, AI-powered suggestions, and a beautiful modern UI.

---

## 🚀 Features

### Core Automation
1. **Smart Keystroke Recorder** - Capture 3-second keyboard patterns with precision
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
