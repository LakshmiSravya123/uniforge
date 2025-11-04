# Paste this into run_all.sh (overwrite the old one)
#!/bin/bash
set -e

# Backend
cd backend
python app.py &
BACK_PID=$!
cd ..

# UniForge recorder bridge (fixed import)
cd uniforge
python -m uniforge.server &
FORGE_PID=$!
cd ..

# Frontend
cd frontend
npm run dev &
FRONT_PID=$!
cd ..

echo "All services running!"
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop"

wait $BACK_PID $FORGE_PID $FRONT_PID