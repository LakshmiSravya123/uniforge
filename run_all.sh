#!/bin/bash
set -e

cd backend
python app.py &
BACK_PID=$!
cd ..

cd uniforge
python -m uniforge.server &
FORGE_PID=$!
cd ..

cd frontend
npm run dev &
FRONT_PID=$!
cd ..

echo "All services running!"
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop"

wait $BACK_PID $FORGE_PID $FRONT_PID