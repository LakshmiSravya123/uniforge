#!/usr/bin/env python3
"""
CodeForge Web UI - Generate apps from browser
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os
from pathlib import Path

app = Flask(__name__, static_folder='codeforge_ui')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('codeforge_ui', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Generate app from idea"""
    data = request.json
    idea = data.get('idea', '')
    
    if not idea:
        return jsonify({'error': 'Idea is required'}), 400
    
    try:
        # Run codeforge.py
        result = subprocess.run(
            ['/Users/sravyalu/uniforge/.venv/bin/python', 'codeforge.py', idea],
            cwd='/Users/sravyalu/uniforge',
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Parse output to get app name and location
        output = result.stdout
        
        # Extract app name from output
        app_name = None
        location = None
        for line in output.split('\n'):
            if line.startswith('📦 Generating:'):
                app_name = line.split(':')[1].strip()
            elif line.startswith('   /Users/'):
                location = line.strip()
        
        return jsonify({
            'success': True,
            'app_name': app_name,
            'location': location,
            'output': output
        })
    
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Generation timed out'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/apps', methods=['GET'])
def list_apps():
    """List generated apps"""
    generated_dir = Path('/Users/sravyalu/uniforge/generated')
    
    if not generated_dir.exists():
        return jsonify({'apps': []})
    
    apps = []
    for app_dir in generated_dir.iterdir():
        if app_dir.is_dir() and (app_dir / 'frontend').exists():
            apps.append({
                'name': app_dir.name,
                'path': str(app_dir),
                'has_backend': (app_dir / 'backend').exists(),
                'has_frontend': (app_dir / 'frontend').exists()
            })
    
    return jsonify({'apps': apps})

if __name__ == '__main__':
    print("🔥 CodeForge Web UI")
    print("📍 Open http://localhost:3000")
    print("")
    app.run(host='0.0.0.0', port=3000, debug=True)
