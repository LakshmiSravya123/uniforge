import keyboard
import time

def replay(pattern):
    print("Replaying pattern…")
    for key in pattern:
        keyboard.press(key)
        time.sleep(0.02)
        keyboard.release(key)
    print("Replay finished")