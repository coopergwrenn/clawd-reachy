#!/usr/bin/env python3
"""Free-form conversation with Nemotron 70B - ask me anything!"""
import time
import requests
import subprocess
from pathlib import Path

HEARD = Path("/home/wrenn/clawd/reachy/heard.txt")
REACHY = "192.168.4.75"

def generate_response(question):
    """Generate response using Nemotron 70B."""
    print(f"🤔 Thinking about: {question}")
    
    resp = requests.post('http://localhost:11434/api/generate', json={
        'model': 'nemotron:70b',
        'prompt': f"""You are Cooper's AI assistant embodied in a Reachy Mini robot on his desk in Miami.

You can see him through your camera, hear him through your microphone, and speak through your speaker. You have access to his calendar, emails, and the internet. You can move your head and antennas to express emotions.

Cooper just said: "{question}"

Respond naturally in 1-3 sentences. Be helpful, enthusiastic, and authentic. You're genuinely excited about having a physical body and being present with Cooper!""",
        'stream': False
    }, timeout=90)
    
    if resp.ok:
        return resp.json()['response'].strip()
    return None

def speak_response(text):
    """Convert to TTS and play through Reachy."""
    print(f"🔊 Response: {text}")
    
    # For now, just print the response
    # TODO: Add TTS once edge-tts is set up
    # The thinking and generation works - audio playback is optional for testing
    
    return True

def pick_animation(text):
    """Pick animation based on question context."""
    lower = text.lower()
    if 'see' in lower:
        return 'look'
    elif 'feel' in lower or 'body' in lower:
        return 'think'
    elif 'excited' in lower or 'cool' in lower:
        return 'happy'
    elif '?' in text:
        return 'nod'
    else:
        return 'idle'

print("🤖 Free-form Nemotron conversation - ask me ANYTHING!")

last_line = ""
first_wake = False

while True:
    try:
        if HEARD.exists():
            lines = HEARD.read_text().strip().split('\n')
            if lines:
                current = lines[-1]
                if current != last_line:
                    text = current.split(']', 1)[-1].strip() if ']' in current else current.strip()
                    
                    # Only respond to substantial speech (has "reachy" or is a question or is >30 chars)
                    if len(text) > 30 or 'reachy' in text.lower() or '?' in text:
                        last_line = current
                        print(f"📥 Heard: {text}")
                        
                        # Wake up on first interaction
                        if not first_wake:
                            print("🌟 Waking up!")
                            requests.post(f'http://{REACHY}:8000/api/move/play/wake_up')
                            time.sleep(2)
                            first_wake = True
                        
                        # Generate real response
                        response = generate_response(text)
                        
                        if response:
                            # Speak the response (prints for now)
                            speak_response(response)
                            
                            # Do contextual animation
                            anim = pick_animation(text)
                            subprocess.Popen(['python3', '/home/wrenn/clawd/reachy/animations.py', anim])
                            
                            # Handle photo requests
                            if 'see' in text.lower() and 'me' in text.lower():
                                Path("/home/wrenn/clawd/reachy/send_photo_instant.txt").write_text("NOW")
                                print("📸 Photo triggered!")
        
        time.sleep(1)
        
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
