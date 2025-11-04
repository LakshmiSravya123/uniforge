from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)                     # allow frontend on different port

# In-memory store – disappears when you stop the server
todos = []

@app.route("/api/todos", methods=["GET", "POST"])
def handle_todos():
    if request.method == "POST":
        data = request.get_json()
        todos.append(data)
        return jsonify(todos)
    return jsonify(todos)

if __name__ == "__main__":
    app.run(port=5000, debug=True)