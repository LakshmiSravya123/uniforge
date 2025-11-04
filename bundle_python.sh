#!/bin/bash
cd backend
pyinstaller --onefile --name uniforge-backend app.py
cp dist/uniforge-backend ../frontend/
echo "Backend bundled to frontend/uniforge-backend"