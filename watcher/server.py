import time
import threading
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import keyboard  # For capturing/replaying keys

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

# ==================== DATA ENDPOINTS ====================
@app.route('/data')
def get_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route('/save', methods=['POST'])
def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(request.json, f, indent=2)
    return jsonify({'status': 'saved'})

# ==================== RECORDER ENDPOINTS ====================
@app.route('/record', methods=['POST'])
def record():
    pattern = []
    def on_key(event):
        # Capture key name (e.g., 'ctrl', 'c', 'enter')
        if event.event_type == keyboard.KEY_DOWN:
            pattern.append(event.name)
    
    # Hook keyboard events for 3 seconds
    hook = keyboard.hook(on_key)
    time.sleep(3)
    keyboard.unhook(hook)  # Clean up
    
    print(f"Recorded pattern: {pattern}")  # Console output for debugging
    return jsonify({'pattern': pattern})

@app.route('/replay', methods=['POST'])
def replay():
    data = request.get_json()
    pattern = data.get('pattern', [])
    if not pattern:
        return jsonify({'error': 'No pattern provided'}), 400
    
    print(f"Replaying pattern: {pattern}")  # Console output
    for key in pattern:
        try:
            keyboard.press_and_release(key)
            time.sleep(0.02)  # 20ms delay for natural feel
        except Exception as e:
            print(f"Error replaying {key}: {e}")
    
    return jsonify({'status': 'replayed'})

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5001))
    print(f"Starting UniForge Server on http://127.0.0.1:{port}")
    print(f"  - Data endpoints: /data, /save")
    print(f"  - Recorder endpoints: /record, /replay")
    app.run(host='127.0.0.1', port=port, debug=False)
