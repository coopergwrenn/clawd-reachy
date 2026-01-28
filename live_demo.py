#!/usr/bin/env python3
"""Live demo - I respond in real-time to Cooper's questions."""
import time
import subprocess
import requests
from pathlib import Path

HEARD_FILE = Path("/home/wrenn/clawd/reachy/heard.txt")
LAST_PROCESSED = Path("/home/wrenn/clawd/reachy/last_processed.txt")

def play_tts(text):
    """Generate TTS and play through Reachy."""
    # Generate TTS on DGX
    resp = requests.get(f"http://localhost:5000/tts", params={"text": text})
    if resp.ok:
        # Save audio
        audio_file = "/tmp/live_response.mp3"
        Path(audio_file).write_bytes(resp.content)
        
        # Convert and upload to Reachy
        subprocess.run(['ffmpeg', '-i', audio_file, '-ar', '16000', '-ac', '1', '/tmp/live.wav', '-y'], 
                      capture_output=True)
        subprocess.run(['scp', '/tmp/live.wav', 'pollen@192.168.4.75:/tmp/live_response.wav'])
        
        # Play on Reachy
        subprocess.run(['ssh', 'pollen@192.168.4.75', 
                       'cd /tmp && python3 -c "import sys; sys.path.insert(0,\\\"/venvs/apps_venv/lib/python3.12/site-packages\\\"); from reachy_mini import ReachyMini; import wave, numpy as np, time; r=ReachyMini(media_backend=\\\"default\\\"); wf=wave.open(\\\"live_response.wav\\\",\\\"rb\\\"); frames=wf.readframes(wf.getnframes()); sr=wf.getframerate(); nc=wf.getnchannels(); audio=np.frombuffer(frames,dtype=np.int16).astype(np.float32)/32768.0; audio=np.column_stack([audio,audio]) if nc==1 else audio; r.media.start_playing(); r.media.push_audio_sample(audio); time.sleep(len(audio)/sr+0.5); r.media.stop_playing()"'])
        
        print(f"🔊 Played: {text}")
        return True
    return False

# This script will be called when I want to speak through Reachy
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        play_tts(text)
