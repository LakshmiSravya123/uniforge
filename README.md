# UniForge

Automate repetitive desktop workflows by capturing keyboard patterns and replaying them through a unified desktop experience. UniForge ships as a three-service MVP: a Flask API for todo-like data, a keystroke recorder bridge, and a Vite/Electron frontend that orchestrates automation flows.

---

## Features
1. **Flask REST API** for storing lightweight task metadata (`/api/todos`).
2. **Keystroke recorder & replayer** (Python `keyboard` library) to capture 3-second input patterns and replay them on demand.
3. **Electron desktop shell** that wraps the frontend, starts the packaged Python backend, and loads the built UI.
4. **One-command dev script** (`run_all.sh`) to launch backend, recorder bridge, and frontend simultaneously.
5. **Packaged binaries** via PyInstaller (Python) and `electron-builder` (frontend) for distributing the desktop app.

---

## Architecture

| Layer | Location | Description |
| --- | --- | --- |
| Web API | `backend/app.py` | Flask service exposing `/api/todos` for GET/POST. Uses in-memory storage and enables CORS for local dev. Runs on port `5000`. |
| Recorder Bridge | `uniforge/server.py` | Flask microservice exposing `/record` and `/replay`. Relies on `keyboard` library to capture 3-second keystroke patterns and replay them. Runs on port `5001`. |
| Electron Shell & Frontend | `frontend/` | Vite-driven UI bundled into Electron for desktop delivery. `main.js` spawns the packaged backend binary so the desktop app works offline. |
| Packaging Utilities | `bundle_python.sh`, `frontend/package.json` | PyInstaller configuration to bundle the backend and Electron builder scripts (`npm run dist`, `npm run dist-mac`). |

```
uniforge/
├── backend/              # Flask API + PyInstaller spec
├── frontend/             # Vite/Electron desktop UI
├── uniforge/             # Recorder/replayer bridge package
├── bundle_python.sh      # Helper to bundle Python backend for Electron
├── run_all.sh            # Dev convenience script (starts all services)
└── README.md
```

---

## Prerequisites
- **Python** ≥ 3.10 (recommended) with `pip`
- **Node.js** ≥ 18 (for Vite + Electron 30)
- **npm** (ships with Node)
- macOS requires granting the Python recorder accessibility permissions for keystroke capture (`System Settings → Privacy & Security → Accessibility`).

---

## Setup

1. **Clone & enter the project**
   ```bash
   git clone https://github.com/LakshmiSravya123/uniforge.git
   cd uniforge
   ```

2. **Backend dependencies**
   ```bash
   cd backend
   python -m venv .venv            # optional but recommended
   source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
   pip install -r requirements.txt
   cd ..
   ```

3. **Frontend dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Recorder bridge dependencies**
   - The bridge shares the same environment as the backend. Ensure `keyboard` is available (installed via backend requirements).

---

## Development Workflow

### Option A: One-command startup
```bash
bash run_all.sh
```
This script will:
- start the Flask backend on port 5000,
- launch the recorder bridge on port 5001, and
- run `npm run dev` in the frontend (typically served on `http://localhost:5173`).

Press `Ctrl+C` to stop all services.

### Option B: Manual control
```bash
# Terminal 1 – backend API
cd backend
python app.py

# Terminal 2 – recorder bridge
cd uniforge
python -m uniforge.server

# Terminal 3 – frontend UI
cd frontend
npm run dev
```

Open the frontend URL printed by Vite (default `http://localhost:5173`).

---

## Building the Desktop App

1. **Bundle the Python backend**
   ```bash
   bash bundle_python.sh
   ```
   This runs PyInstaller, placing the binary at `backend/dist/uniforge-backend` and copying it into `frontend/` for Electron.

2. **Package the desktop app**
   ```bash
   cd frontend
   npm run build       # optional: produce production web assets
   npm run dist        # cross-platform build (see electron-builder config)
   npm run dist-mac    # macOS-specific DMG
   ```
   Artifacts appear in `frontend/dist/`. Large binaries (Electron frameworks, DMG) are ignored from Git by default—publish releases through GitHub Releases or another artifact store instead of committing them.

---

## API Reference

### Backend (`backend/app.py`)
- `GET /api/todos` → returns the in-memory list of todo objects.
- `POST /api/todos` → accepts JSON payload, appends to memory, and returns the updated list.
  - Example payload: `{ "title": "Automate billing run", "status": "pending" }`

> The in-memory list resets whenever the server restarts. Persist to a database if you need durability.

### Recorder Bridge (`uniforge/server.py`)
- `POST /record` → captures keyboard events for 3 seconds and returns `{ "pattern": ["ctrl", "c", ...] }`.
- `POST /replay` → accepts `{ "pattern": [...] }` and replays each key with a 20ms delay.

Both endpoints require local execution because they interact with OS-level keyboard hooks.

---

## Troubleshooting
- **Push failures due to large binaries**: remove `frontend/dist` or `frontend/node_modules` from commits (`git rm -r --cached frontend/dist frontend/node_modules`) and rely on `.gitignore` to keep them out of history.
- **Keyboard recording blocked on macOS**: grant accessibility permissions to the Python interpreter (`System Settings → Privacy & Security → Accessibility`).
- **Port conflicts**: adjust ports in `backend/app.py` or `uniforge/server.py`, then update the frontend configuration accordingly.
- **Electron backend not starting**: ensure `bundle_python.sh` ran successfully so `frontend/uniforge-backend` exists.

---

## Contributing
1. Create a feature branch.
2. Keep commits focused.
3. Ensure `frontend/dist` and `frontend/node_modules` remain untracked.
4. Open a pull request against `main` with a summary of changes and testing notes.

---

## License
Specify project licensing here (e.g., MIT). Update this section once a license is chosen.