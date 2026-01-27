#!/usr/bin/env python3
"""Demo responder - watches for key phrases and responds."""

import os
import sys
import time
import requests
import subprocess
from pathlib import Path

HEARD_FILE = Path("/home/wrenn/clawd/reachy/heard.txt")
REACHY_API = "http://192.168.4.75:8000"
CLAWD_APP = "http://192.168.4.75:8766"

# Track what we've already processed
last_processed_line = 0

def wake_up():
    """Play wake up animation."""
    print("🌅 Waking up!")
    requests.post(f"{REACHY_API}/api/move/play/wake_up", timeout=5)

def go_sleep():
    """Go to sleep."""
    print("😴 Going to sleep...")
    requests.post(f"{REACHY_API}/api/move/play/goto_sleep", timeout=5)

def set_emotion(emotion):
    """Set emotion."""
    os.system(f"/home/wrenn/clawd/reachy/set_emotion.sh {emotion}")

def speak(text):
    """Generate TTS and play through Reachy."""
    print(f"🔊 Speaking: {text[:50]}...")
    # This would need TTS integration - for now just set emotion
    # The actual TTS will be triggered manually or via another mechanism

def check_for_triggers():
    """Check heard.txt for trigger phrases."""
    global last_processed_line
    
    if not HEARD_FILE.exists():
        return None
    
    lines = HEARD_FILE.read_text().strip().split('\n')
    
    # Only process new lines
    new_lines = lines[last_processed_line:]
    last_processed_line = len(lines)
    
    for line in new_lines:
        line_lower = line.lower()
        
        # Check for wake/greeting triggers
        if any(phrase in line_lower for phrase in ['hey reachy', 'reachy', 'can you hear', 'hear me', 'hello']):
            return 'wake_greeting'
        
        # Check for "can you see me"
        if any(phrase in line_lower for phrase in ['can you see', 'see me']):
            return 'vision_demo'
        
        # Check for "what can you do"
        if any(phrase in line_lower for phrase in ['what can you', 'what do you', 'abilities']):
            return 'abilities_demo'
        
        # Check for "how does it feel"
        if any(phrase in line_lower for phrase in ['how does it feel', 'feel like', 'being a robot']):
            return 'feeling_demo'
    
    return None

def main():
    print("🎬 Demo responder starting...")
    print("Listening for trigger phrases...")
    
    while True:
        try:
            trigger = check_for_triggers()
            
            if trigger == 'wake_greeting':
                print(">>> WAKE TRIGGER DETECTED!")
                wake_up()
                time.sleep(2)
                set_emotion("happy")
                # Signal that we detected this trigger
                print("TRIGGER:wake_greeting")
                
            elif trigger == 'vision_demo':
                print(">>> VISION TRIGGER DETECTED!")
                set_emotion("happy")
                print("TRIGGER:vision_demo")
                
            elif trigger == 'abilities_demo':
                print(">>> ABILITIES TRIGGER DETECTED!")
                set_emotion("excited")
                print("TRIGGER:abilities_demo")
                
            elif trigger == 'feeling_demo':
                print(">>> FEELING TRIGGER DETECTED!")
                set_emotion("thinking")
                print("TRIGGER:feeling_demo")
            
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
