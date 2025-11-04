from flask import Flask, request, jsonify
from .recorder import record_3sec
from .replayer import replay

app = Flask(__name__)

@app.route("/record", methods=["POST"])
def record():
    pattern = record_3sec()
    return jsonify({"pattern": pattern})

@app.route("/replay", methods=["POST"])
def do_replay():
    data = request.get_json()
    replay(data["pattern"])
    return jsonify({"status": "ok"})

def run():
    app.run(port=5001, debug=False)