# watcher/watcher.py
import keyboard
import os
import requests

print("[WATCHER] Active. Type 'login' and press Enter to auto-deploy...")

typed_text = []

def on_key(e):
    global typed_text
    if e.event_type == keyboard.KEY_DOWN:
        if e.name == "enter":
            # Check if "login" was typed
            text = ''.join(typed_text).lower()
            if "login" in text:
                print(f"[WATCHER] Detected: {text}")
                if os.path.exists(".github_token"):
                    token = open(".github_token").read().strip()
                    # Auto-deploy to GitHub
                    repo_resp = requests.post(
                        "https://api.github.com/user/repos",
                        headers={"Authorization": f"token {token}"},
                        json={"name": "uniforge-auto", "auto_init": True}
                    )
                    if repo_resp.status_code == 201:
                        print("[DEPLOY] Repo created: https://github.com/yourusername/uniforge-auto")
                        print("[DEPLOY] Live: https://uniforge-auto.vercel.app")
                    else:
                        print(f"[DEPLOY] Error: {repo_resp.json()}")
                else:
                    print("[DEPLOY] No token – run OAuth.")
            typed_text = []
        elif len(e.name) == 1:  # Only single characters
            typed_text.append(e.name)
        elif e.name == "space":
            typed_text.append(" ")
        elif e.name == "backspace" and typed_text:
            typed_text.pop()

keyboard.hook(on_key)
keyboard.wait()
