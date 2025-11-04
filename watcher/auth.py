# watcher/auth.py
import webbrowser
import requests
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs
import threading
import dotenv

# Load .env
dotenv.load_dotenv()

# === CONFIG ===
CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000"
TOKEN_FILE = ".github_token"

if not CLIENT_ID or not CLIENT_SECRET:
    raise EnvironmentError("Please set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET in .env")

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if "?" not in self.path:
            self.send_error(400, "No query string")
            return
        query = parse_qs(self.path.split("?")[1])
        code = query.get("code", [None])[0]
        if not code:
            self.send_error(400, "No code")
            return

        # Exchange code for token
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

        # Save token
        with open(TOKEN_FILE, "w") as f:
            f.write(access_token)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"""
        <h1 style="font-family: sans-serif; text-align: center; margin-top: 100px;">
          Connected! You can close this tab.
        </h1>
        """)

    def log_message(self, format, *args):
        return  # Silence server logs

def start_oauth_server():
    if os.path.exists(TOKEN_FILE):
        print("GitHub token already exists. Skipping login.")
        return

    print(f"Starting OAuth server on {REDIRECT_URI}")
    server = HTTPServer(("localhost", OAUTH_PORT), OAuthHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()

    # Open browser
    auth_url = "https://github.com/login/oauth/authorize?" + urlencode({
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "repo"
    })
    print(f"Opening: {auth_url}")
    webbrowser.open(auth_url)

# Run on import
start_oauth_server()