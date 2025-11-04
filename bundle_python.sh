#!/bin/bash
cd backend
pyinstaller --onefile --name uniforge-backend app.py
cd ..

# Now copy dist/uniforge-backend to frontend/ for Electron
cp backend/dist/uniforge-backend frontend/