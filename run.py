# run.py
import subprocess
import threading
import time
import os

def run_command(cmd, name, cwd=None, port=None):
    env = os.environ.copy()
    if port:
        env["FLASK_PORT"] = str(port)
    while True:
        print(f"\n[{name}] Starting...")
        proc = subprocess.Popen(
            cmd,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        for line in proc.stdout:
            print(f"[{name}] {line.rstrip()}")
        proc.wait()
        print(f"[{name}] Crashed! Restarting in 2s...")
        time.sleep(2)

# === 1. Start OAuth (runs on import in auth.py) ===
print("[OAUTH] Initializing...")
import watcher.auth  # This starts the server

# === 2. Start Flask on PORT 5001 (avoid AirPlay) ===
threading.Thread(
    target=run_command,
    args=(["python", "backend/main.py"], "Flask", None, 5001),
    daemon=True
).start()
time.sleep(3)

# === 3. Start Watcher ===
threading.Thread(
    target=run_command,
    args=(["python", "watcher/watcher.py"], "Watcher"),
    daemon=True
).start()
time.sleep(2)

# === 4. Start Vite ===
print(f"\n[FRONTEND] Starting on http://127.0.0.1:5174")
run_command(
    ["npm", "run", "dev"],
    "Vite",
    cwd="frontend"
)