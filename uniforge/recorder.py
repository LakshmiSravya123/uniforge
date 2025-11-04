import keyboard
import time
import threading

def record_3sec():
    print("Recording keystrokes for 3 seconds…")
    events = keyboard.record(timeout=3.0)
    # Convert to simple list of key names
    pattern = [e.name for e in events if e.event_type == keyboard.KEY_DOWN]
    print(f"Recorded {len(pattern)} keystrokes")
    return pattern