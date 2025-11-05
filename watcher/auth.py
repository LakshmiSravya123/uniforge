# watcher/auth.py
import webbrowser
import requests
import threading
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs
import dotenv
dotenv.load_dotenv()

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000"
TOKEN_FILE = ".github_token"

if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: Set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET in .env")
    exit(1)

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(self.path.split("?")[1] if "?" in self.path else "")
        code = query.get("code", [None])[0]
        if not code:
            self.send_error(400, "No code")
            return
        token_resp = requests.post(
            "https://github.com/login/oauth/access_token",
            params={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "redirect_uri": REDIRECT_URI
            },
            headers={"Accept": "application/json"}
        )
        token_data = token_resp.json()
        access_token = token_data.get("access_token")
        if not access_token:
            self.send_error(500, f"Token error: {token_data}")
            return
        with open(TOKEN_FILE, "w") as f:
            f.write(access_token)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Connected! Close this tab.</h1>")
    def log_message(self, *args): pass

if not os.path.exists(TOKEN_FILE):
    print("[OAUTH] Opening GitHub login...")
    server = HTTPServer(("localhost", 8000), OAuthHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    auth_url = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=repo"
    webbrowser.open(auth_url)
else:
    print("[OAUTH] Token exists. Skipping.")