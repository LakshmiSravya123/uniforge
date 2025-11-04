# backend/main.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import os, json

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

@app.route("/data")
def get_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route("/save", methods=["POST"])
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(request.json, f, indent=2)
    return jsonify({"status": "saved"})

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    print(f"[Flask] Listening on http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=False)