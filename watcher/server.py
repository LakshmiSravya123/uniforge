import time
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import keyboard  # For capturing/replaying keys

app = Flask(__name__)
CORS(app)

@app.route('/record', methods=['POST'])
def record():
    pattern = []
    def on_key(event):
        # Capture key name (e.g., 'ctrl', 'c', 'enter')
        pattern.append(event.name)
    
    # Hook keyboard events for 3 seconds
    hook = keyboard.hook(on_key)
    time.sleep(3)
    hook()
    keyboard.unhook(hook)  # Clean up
    
    print(f"Recorded pattern: {pattern}")  # Console output for debugging
    return jsonify({"pattern": pattern})

@app.route('/replay', methods=['POST'])
def replay():
    data = request.get_json()
    pattern = data.get("pattern", [])
    if not pattern:
        return jsonify({'error': 'No pattern provided'}), 400
    
    print(f"Replaying pattern: {pattern}")  # Console output
    for key in pattern:
        try:
            keyboard.press_and_release(key)
            time.sleep(0.02)  # 20ms delay for natural feel
        except Exception as e:
            print(f"Error replaying {key}: {e}")
    
    return jsonify({"status": "replayed"})

if __name__ == '__main__':
    print("Starting UniForge Recorder Bridge on http://localhost:5001")
    print("Test record: curl -X POST http://localhost:5001/record")
    print("Test replay: curl -X POST http://localhost:5001/replay -H 'Content-Type: application/json' -d '{\"pattern\": [\"ctrl\", \"c\"]}'")
    app.run(debug=True, port=5001)