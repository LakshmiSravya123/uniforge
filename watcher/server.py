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
PATTERNS_FILE = "patterns.json"

def load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"[WARN] Failed to load {path}: {e}")
    return default

def save_json(path, data):
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"[WARN] Failed to save {path}: {e}")
        return False

# ==================== DATA ENDPOINTS ====================
@app.route('/data')
def get_data():
    try:
        data = load_json(DATA_FILE, [])
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': f'Failed to load data: {str(e)}'}), 500

@app.route('/save', methods=['POST'])
def save_data():
    try:
        if not request.json:
            return jsonify({'error': 'No data provided'}), 400
        ok = save_json(DATA_FILE, request.json)
        if ok:
            return jsonify({'status': 'saved'}), 200
        else:
            return jsonify({'error': 'Failed to save data'}), 500
    except Exception as e:
        return jsonify({'error': f'Save failed: {str(e)}'}), 500

# ==================== PATTERNS (Server storage) ====================
def load_patterns():
    return load_json(PATTERNS_FILE, [])

def save_patterns(patterns):
    return save_json(PATTERNS_FILE, patterns)

def register_hotkey_safely(name, hotkey, pattern):
    try:
        if not hotkey:
            return False
        def _cb():
            print(f"[Hotkey] Trigger '{name}' via {hotkey}")
            try:
                for key in pattern:
                    keyboard.press_and_release(key)
                    time.sleep(0.02)
            except Exception as e:
                print(f"[Hotkey] Replay error: {e}")
        keyboard.add_hotkey(hotkey, _cb)
        print(f"[Hotkey] Registered {name} -> {hotkey}")
        return True
    except Exception as e:
        print(f"[Hotkey] Could not register {hotkey}: {e}")
        return False

@app.route('/patterns', methods=['GET'])
def patterns_get():
    return jsonify(load_patterns())

@app.route('/patterns', methods=['POST'])
def patterns_post():
    body = request.get_json(force=True) or {}
    name = (body.get('name') or '').strip()
    pattern = body.get('pattern') or []
    hotkey = (body.get('hotkey') or '').strip()
    if not name or not isinstance(pattern, list):
        return jsonify({'error': 'Invalid name or pattern'}), 400
    patterns = load_patterns()
    # upsert by name
    found = False
    for p in patterns:
        if p.get('name') == name:
            p['pattern'] = pattern
            p['hotkey'] = hotkey
            found = True
            break
    if not found:
        patterns.append({'name': name, 'pattern': pattern, 'hotkey': hotkey})
    save_patterns(patterns)
    # Try hotkey registration (optional)
    if hotkey:
        register_hotkey_safely(name, hotkey, pattern)
    return jsonify({'status': 'ok', 'patterns': patterns})

@app.route('/patterns/<name>', methods=['DELETE'])
def patterns_delete(name):
    name = (name or '').strip()
    patterns = load_patterns()
    newp = [p for p in patterns if p.get('name') != name]
    save_patterns(newp)
    return jsonify({'status': 'ok', 'patterns': newp})

# ==================== RECORDER ENDPOINTS ====================
@app.route('/record', methods=['POST'])
def record():
    try:
        # Get duration from query param or request body, default to 3 seconds
        duration = request.args.get('duration', type=float)
        if duration is None:
            body = request.get_json(force=True, silent=True) or {}
            duration = body.get('duration', 3.0)
        
        # Validate duration (1-30 seconds)
        duration = max(1.0, min(30.0, duration))
        
        pattern = []
        recording_error = None
        
        def on_key(event):
            # Capture key name (e.g., 'ctrl', 'c', 'enter')
            if event.event_type == keyboard.KEY_DOWN:
                pattern.append(event.name)
        
        # Try to hook keyboard events
        try:
            hook = keyboard.hook(on_key)
            time.sleep(duration)
            keyboard.unhook(hook)  # Clean up
        except OSError as e:
            recording_error = str(e)
            if "administrator" in str(e).lower() or "permission" in str(e).lower():
                recording_error = "Accessibility permissions required. On macOS: System Settings → Privacy & Security → Accessibility → Add Terminal/Python"
        
        print(f"Recorded pattern ({duration}s): {pattern}")  # Console output for debugging
        
        if not pattern and recording_error:
            return jsonify({
                'pattern': [], 
                'duration': duration,
                'warning': recording_error,
                'help': 'Run: sudo python run.py OR grant accessibility permissions'
            }), 200
        
        return jsonify({'pattern': pattern, 'duration': duration}), 200
    except Exception as e:
        return jsonify({'error': f'Recording failed: {str(e)}'}), 500

@app.route('/replay', methods=['POST'])
def replay():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
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
        
        return jsonify({'status': 'replayed'}), 200
    except Exception as e:
        return jsonify({'error': f'Replay failed: {str(e)}'}), 500

@app.route('/replay/name/<name>', methods=['POST', 'GET'])
def replay_by_name(name):
    try:
        patterns = load_patterns()
        for p in patterns:
            if p.get('name') == name:
                return replay_pattern(p.get('pattern', []))
        return jsonify({'error': 'Pattern not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Replay by name failed: {str(e)}'}), 500

def replay_pattern(pattern):
    if not pattern:
        return jsonify({'error': 'No pattern provided'}), 400
    print(f"Replaying pattern: {pattern}")
    for key in pattern:
        try:
            keyboard.press_and_release(key)
            time.sleep(0.02)
        except Exception as e:
            print(f"Error replaying {key}: {e}")
    return jsonify({'status': 'replayed'})

@app.route('/hotkey/register', methods=['POST'])
def hotkey_register():
    body = request.get_json(force=True) or {}
    name = (body.get('name') or '').strip()
    hotkey = (body.get('hotkey') or '').strip()
    patterns = load_patterns()
    for p in patterns:
        if p.get('name') == name:
            p['hotkey'] = hotkey
            save_patterns(patterns)
            ok = register_hotkey_safely(name, hotkey, p.get('pattern', []))
            return jsonify({'status': 'ok' if ok else 'warn', 'patterns': patterns})
    return jsonify({'error': 'Pattern not found'}), 404

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5001))
    print(f"Starting UniForge Server on http://127.0.0.1:{port}")
    print(f"  - Data: /data, /save")
    print(f"  - Patterns: GET/POST /patterns, DELETE /patterns/<name>")
    print(f"  - Replay: POST /replay, GET/POST /replay/name/<name>")
    print(f"  - Hotkeys: POST /hotkey/register (optional)")
    print(f"  - Health: /health")
    # Try to preload hotkeys
    for item in load_patterns():
        if item.get('hotkey'):
            register_hotkey_safely(item.get('name'), item.get('hotkey'), item.get('pattern', []))
    app.run(host='127.0.0.1', port=port, debug=False)
