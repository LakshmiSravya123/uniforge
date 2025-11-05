# run.py
import subprocess
import threading
import time
import os
import sys

PYTHON = sys.executable or "python"

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
        if name == "Watcher":
            print(f"[{name}] Watcher requires accessibility permissions on macOS.")
            print(f"[{name}] Skipping watcher - app will work without it.")
            break
        print(f"[{name}] Crashed! Restarting in 2s...")
        time.sleep(2)

# === 1. Start OAuth (optional) ===
print("[OAUTH] Initializing...")
try:
    import watcher.auth  # This starts the server if configured
except Exception as e:
    print(f"[OAUTH] Skipped: {e}")

# === 2. Start Flask on PORT 5001 ===
threading.Thread(
    target=run_command,
    args=([PYTHON, "watcher/server.py"], "Server", None, 5001),
    daemon=True
).start()
time.sleep(3)

# === 3. Start Watcher (optional - requires sudo on macOS) ===
print("[INFO] Watcher requires accessibility permissions and may need sudo.")
print("[INFO] Skipping watcher - you can enable it later for auto-deploy.")

# === 4. Start Vite ===
print(f"\n[FRONTEND] Starting on http://127.0.0.1:5174")
run_command(
    ["npm", "run", "dev"],
    "Vite",
    cwd="frontend"
)
