from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from ollama import Client as OllamaClient
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

app = Flask(__name__)
CORS(app)

# In-memory store
todos = []

# LLM Setup
USE_GROQ = os.getenv('USE_GROQ', 'false').lower() == 'true'
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODEL = 'llama3.3'

llm_client = None
if USE_GROQ and GROQ_AVAILABLE and GROQ_API_KEY:
    llm_client = Groq(api_key=GROQ_API_KEY)
    print("Using Groq (cloud)")
else:
    llm_client = OllamaClient()
    print("Using Ollama (local)")

@app.route("/api/todos", methods=["GET", "POST"])
def handle_todos():
    if request.method == "POST":
        data = request.get_json()
        todos.append(data)
        return jsonify(todos)
    return jsonify(todos)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    if not message:
        return jsonify({'error': 'No message'}), 400
    
    try:
        if USE_GROQ and GROQ_AVAILABLE and GROQ_API_KEY:
            completion = llm_client.chat.completions.create(
                messages=[{"role": "user", "content": message}],
                model=MODEL,
                temperature=0.7
            )
            response = completion.choices[0].message.content
        else:
            response = llm_client.chat(model=MODEL, messages=[{'role': 'user', 'content': message}])['message']['content']
        
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)