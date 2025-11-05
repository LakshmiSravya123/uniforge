from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for local dev (allows frontend to call this API)

# In-memory storage for todos (simple list; resets on restart)
todos = []

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Missing "title" in request'}), 400
    todo = {
        'title': data['title'],
        'status': data.get('status', 'pending'),
        'id': len(todos) + 1
    }
    todos.append(todo)
    return jsonify(todos), 201

if __name__ == '__main__':
    print("Starting UniForge Backend API on http://localhost:5000")
    print("Test it: curl http://localhost:5000/api/todos")
    app.run(debug=True, port=5000)