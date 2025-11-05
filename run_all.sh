#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# Detect Python interpreter
if [[ -d "$ROOT_DIR/.venv" ]]; then
  PYTHON="$ROOT_DIR/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON="python3"
else
  echo "ERROR: No Python 3 found. Install Python 3 or create .venv" >&2
  exit 1
fi

echo "=== UniForge Startup ==="
echo "Using: $PYTHON"

# Kill all existing processes on our ports
echo "Cleaning ports 5000, 5001, 5174, 8000..."
for port in 5000 5001 5174 8000; do
  if lsof -ti:"$port" >/dev/null 2>&1; then
    echo "  Killing process on port $port"
    lsof -ti:"$port" | xargs kill -9 2>/dev/null || true
    sleep 0.5
  fi
done

# Install dependencies if missing
if [[ ! -d "$ROOT_DIR/frontend/node_modules" ]]; then
  echo "Installing frontend dependencies..."
  (cd "$ROOT_DIR/frontend" && npm install)
fi

echo ""
echo "Starting services..."

# 1. Backend API (port 5000)
echo "[1/4] Starting Backend API on port 5000..."
cd "$ROOT_DIR/backend"
"$PYTHON" app.py > "$ROOT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
cd "$ROOT_DIR"
sleep 2

# 2. Recorder Bridge (port 5001)
echo "[2/4] Starting Recorder Bridge on port 5001..."
"$PYTHON" "$ROOT_DIR/watcher/server.py" > "$ROOT_DIR/bridge.log" 2>&1 &
BRIDGE_PID=$!
sleep 2

# 3. OAuth Server (port 8000) - only if no token exists
if [[ ! -f "$ROOT_DIR/.github_token" ]]; then
  echo "[3/4] Starting OAuth server on port 8000..."
  "$PYTHON" -c "import watcher.auth" > "$ROOT_DIR/oauth.log" 2>&1 &
  OAUTH_PID=$!
else
  echo "[3/4] GitHub token exists, skipping OAuth"
  OAUTH_PID=""
fi
sleep 1

# 4. Frontend (port 5174)
echo "[4/4] Starting Frontend on port 5174..."
cd "$ROOT_DIR/frontend"
npm run dev > "$ROOT_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
cd "$ROOT_DIR"

sleep 3

echo ""
echo "=== UniForge is LIVE ==="
echo "Frontend:  http://localhost:5174"
echo "Backend:   http://localhost:5000/api/todos"
echo "Recorder:  http://localhost:5001/record"
if [[ -n "$OAUTH_PID" ]]; then
  echo "OAuth:     http://localhost:8000"
fi
echo ""
echo "Logs:"
echo "  Backend:  tail -f backend.log"
echo "  Bridge:   tail -f bridge.log"
echo "  Frontend: tail -f frontend.log"
echo ""
echo "Press Ctrl+C to stop all services"

# Cleanup on exit
trap "echo 'Stopping...'; kill $BACKEND_PID $BRIDGE_PID $FRONTEND_PID $OAUTH_PID 2>/dev/null; exit" INT TERM

wait