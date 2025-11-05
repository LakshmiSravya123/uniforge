#!/bin/bash
# CodeForge Quick Start - Auto-launch generated app

PROJECT_DIR="${1:-.}"
cd "$PROJECT_DIR" || exit 1

echo "🔥 CodeForge Quick Start"
echo "📍 Project: $PROJECT_DIR"
echo ""

# Check if backend and frontend exist
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
  echo "❌ Error: backend/ and frontend/ directories not found"
  echo "Run this script from a CodeForge-generated project directory"
  exit 1
fi

# Check if node_modules exist
if [ ! -d "backend/node_modules" ]; then
  echo "📦 Installing backend dependencies..."
  cd backend && npm install && cd ..
fi

if [ ! -d "frontend/node_modules" ]; then
  echo "📦 Installing frontend dependencies..."
  cd frontend && npm install && cd ..
fi

# Create .env if it doesn't exist
if [ ! -f "backend/.env" ]; then
  echo "⚠️  No .env file found"
  echo "📝 Creating backend/.env from .env.example..."
  cp backend/.env.example backend/.env
  echo ""
  echo "⚠️  IMPORTANT: Edit backend/.env with your Supabase credentials!"
  echo "   1. Go to supabase.com"
  echo "   2. Create project or use existing"
  echo "   3. Copy URL and anon key from Settings → API"
  echo "   4. Update backend/.env"
  echo ""
  read -p "Press Enter when ready to continue..."
fi

echo ""
echo "🚀 Starting servers..."
echo ""
echo "Backend will start on:  http://localhost:5001"
echo "Frontend will start on: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Kill any existing processes on ports
lsof -ti:5001 2>/dev/null | xargs kill -9 2>/dev/null || true
lsof -ti:5173 2>/dev/null | xargs kill -9 2>/dev/null || true

# Start backend in background
cd backend
npm run dev > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 2

# Start frontend in foreground
cd frontend
npm run dev

# Cleanup on exit
kill $BACKEND_PID 2>/dev/null || true
