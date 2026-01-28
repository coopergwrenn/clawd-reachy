#!/usr/bin/env python3
"""Live AI responder - generates responses on the fly."""
import time
import subprocess
import requests
from pathlib import Path

HEARD_FILE = Path("/home/wrenn/clawd/reachy/heard.txt")
REACHY_HOST = "192.168.4.75"
STATE_FILE = Path("/home/wrenn/clawd/reachy/responder_state.txt")

def get_last_line():
    """Get the last line from heard.txt."""
    if HEARD_FILE.exists():
        lines = HEARD_FILE.read_text().strip().split('\n')
        return lines[-1] if lines else ""
    return ""

def trigger_response(question):
    """Trigger me to respond to a question."""
    # Write question to a trigger file that I'll monitor
    trigger_file = Path("/home/wrenn/clawd/reachy/question_trigger.txt")
    trigger_file.write_text(question)
    print(f"Triggered response for: {question}")

last_processed = ""
print("🎧 Live responder starting...")

while True:
    line = get_last_line()
    
    if line and line != last_processed:
        # New text detected
        if "reachy" in line.lower() or "hear" in line.lower() or "see" in line.lower() or "what" in line.lower() or "feel" in line.lower():
            print(f"💬 Question: {line}")
            trigger_response(line)
            last_processed = line
    
    time.sleep(0.3)
