#!/usr/bin/env python3
"""Simple, reliable demo monitor."""
import time
import subprocess
import requests
import threading
from pathlib import Path

HEARD = Path("/home/wrenn/clawd/reachy/heard.txt")
REACHY = "192.168.4.75"

q1_done = False
q2_done = False
q3_done = False
q4_done = False

def play_response(num):
    """Play response via bridge (faster, no SSH overhead)."""
    requests.get(f'http://{REACHY}:9000/play/{num}', timeout=20)

def animate(anim):
    """Trigger animation."""
    subprocess.run(['python3', '/home/wrenn/clawd/reachy/animations.py', anim])

def take_and_send_photo():
    """Take photo and send to Telegram."""
    # Trigger me to send photo - I'll watch for this
    Path("/home/wrenn/clawd/reachy/send_photo_instant.txt").write_text("NOW")

def wake_up():
    """Wake up Reachy."""
    requests.post(f'http://{REACHY}:8000/api/move/play/wake_up')

print("🎧 Simple monitor starting...")
last_line = ""

while True:
    if HEARD.exists():
        lines = HEARD.read_text().strip().split('\n')
        if lines:
            current = lines[-1]
            if current != last_line:
                last_line = current
                text = current.split(']', 1)[-1].lower() if ']' in current else current.lower()
                
                # Q1
                if not q1_done and ('reachy' in text or 'hear' in text):
                    q1_done = True
                    print(f"Q1: {current}")
                    wake_up()
                    time.sleep(2)
                    threading.Thread(target=play_response, args=(1,), daemon=True).start()
                    threading.Thread(target=animate, args=('happy',), daemon=True).start()
                
                # Q2
                elif q1_done and not q2_done and ('see me' in text or 'see you' in text or 'see' in text):
                    q2_done = True
                    print(f"Q2: {current}")
                    threading.Thread(target=play_response, args=(2,), daemon=True).start()
                    threading.Thread(target=animate, args=('look',), daemon=True).start()
                    threading.Thread(target=take_and_send_photo, daemon=True).start()
                    print("PHOTO_SENDING")
                
                # Q3
                elif q2_done and not q3_done and ('what can' in text or 'what do' in text):
                    q3_done = True
                    print(f"Q3: {current}")
                    threading.Thread(target=play_response, args=(3,), daemon=True).start()
                    threading.Thread(target=animate, args=('wiggle',), daemon=True).start()
                
                # Q4
                elif q3_done and not q4_done and ('feel' in text or 'body' in text):
                    q4_done = True
                    print(f"Q4: {current}")
                    threading.Thread(target=play_response, args=(4,), daemon=True).start()
                    threading.Thread(target=animate, args=('think',), daemon=True).start()
                    print("DEMO_COMPLETE")
                    time.sleep(20)  # Wait for response to finish
                    break
    
    time.sleep(0.1)  # Check faster!

print("Demo finished!")
