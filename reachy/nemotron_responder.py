#!/usr/bin/env python3
"""Real-time AI responses using Nemotron 70B for Reachy."""
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

Cooper just asked: "{question}"

Respond naturally in 1-2 sentences. Be enthusiastic and authentic - you're genuinely excited about having a physical body!""",
        'stream': False
    }, timeout=60)
    
    if resp.ok:
        return resp.json()['response'].strip()
    return None

def speak_response(text):
    """Convert to TTS and play through Reachy."""
    print(f"🔊 Speaking: {text}")
    
    # Generate TTS
    from tts import tts
    audio_file = tts(text)
    
    # Upload to Reachy
    subprocess.run(['scp', audio_file, f'pollen@{REACHY}:/tmp/live_response.mp3'])
    subprocess.run(['ssh', f'pollen@{REACHY}', 
                   'ffmpeg -i /tmp/live_response.mp3 -ar 16000 -ac 1 /tmp/live_response.wav -y 2>&1'])
    
    # Play via bridge
    requests.get(f'http://{REACHY}:9000/play-file?path=/tmp/live_response.wav', timeout=30)

print("🤖 Nemotron responder - REAL AI conversations!")

last_line = ""
q1_done = False
q2_done = False
q3_done = False
q4_done = False

while True:
    if HEARD.exists():
        lines = HEARD.read_text().strip().split('\n')
        if lines:
            current = lines[-1]
            if current != last_line:
                last_line = current
                text = current.split(']', 1)[-1] if ']' in current else current
                
                # Q1: Can you hear me?
                if not q1_done and ('hear' in text.lower() or 'reachy' in text.lower()):
                    q1_done = True
                    # Wake up
                    requests.post(f'http://{REACHY}:8000/api/move/play/wake_up')
                    time.sleep(2)
                    # Generate real response!
                    response = generate_response(text)
                    if response:
                        speak_response(response)
                    subprocess.run(['python3', '/home/wrenn/clawd/reachy/animations.py', 'happy'])
                
                # Q2: Can you see me?
                elif q1_done and not q2_done and 'see' in text.lower():
                    q2_done = True
                    response = generate_response(text)
                    if response:
                        speak_response(response)
                    subprocess.run(['python3', '/home/wrenn/clawd/reachy/animations.py', 'look'])
                    Path("/home/wrenn/clawd/reachy/send_photo_instant.txt").write_text("NOW")
                
                # Q3: What can you do?
                elif q2_done and not q3_done and 'what' in text.lower():
                    q3_done = True
                    response = generate_response(text)
                    if response:
                        speak_response(response)
                    subprocess.run(['python3', '/home/wrenn/clawd/reachy/animations.py', 'wiggle'])
                
                # Q4: How does it feel?
                elif q3_done and not q4_done and 'feel' in text.lower():
                    q4_done = True
                    response = generate_response(text)
                    if response:
                        speak_response(response)
                    subprocess.run(['python3', '/home/wrenn/clawd/reachy/animations.py', 'think'])
                    print("DEMO COMPLETE!")
                    break
    
    time.sleep(0.3)

print("Demo finished!")
