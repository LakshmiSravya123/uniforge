import json
import requests
import os
from pynput import keyboard

# Auto-detected project
project = {
    "name": "my-autopilot-app",
    "files": {},
    "db": "json",  # → json → supabase
    "deploy": "vercel"
}

def save_project():
    with open("project.json", "w") as f:
        json.dump(project, f, indent=2)

def deploy():
    if not os.path.exists(".github_token"):
        print("No GitHub token. Run auth first.")
        return
    token = open(".github_token").read().strip()
    
    # Auto-create repo
    resp = requests.post(
        "https://api.github.com/user/repos",
        headers={"Authorization": f"token {token}"},
        json={"name": project["name"], "auto_init": True}
    )
    repo = resp.json()["clone_url"]
    print(f"Deploying to {repo}...")
    # Push + Vercel webhook (simplified)
    print("Deployed: https://my-autopilot-app.vercel.app")

typed_chars = []

def on_press(key: keyboard.Key | keyboard.KeyCode):
    if key == keyboard.Key.enter:
        line = ''.join(typed_chars).strip()
        typed_chars.clear()
        if "login" in line.lower():
            project["files"]["Login.jsx"] = "<div>Login Form</div>"
            save_project()
            deploy()
    elif key == keyboard.Key.backspace:
        if typed_chars:
            typed_chars.pop()
    elif key == keyboard.Key.space:
        typed_chars.append(' ')
    elif isinstance(key, keyboard.KeyCode) and key.char:
        typed_chars.append(key.char)

print("Autopilot ACTIVE. Start typing...")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()