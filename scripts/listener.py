#!/usr/bin/env python3
"""FAST listener - 2 second chunks."""
import sys, time, base64, wave, io, requests
sys.path.insert(0, '/venvs/apps_venv/lib/python3.12/site-packages')
from reachy_mini import ReachyMini
import numpy as np

DGX_URL = "http://192.168.4.76:8777/transcribe"
CHUNK = 2  # 2 seconds for faster response

def main():
    print("🎧 FAST listener starting...", flush=True)
    robot = ReachyMini(media_backend="default")
    print("✅ Ready!", flush=True)
    
    while True:
        try:
            samples = []
            robot.media.start_recording()
            start = time.time()
            while time.time() - start < CHUNK:
                s = robot.media.get_audio_sample()
                if s is not None and len(s) > 0:
                    samples.append(s)
                time.sleep(0.05)
            robot.media.stop_recording()
            
            if not samples:
                continue
            
            audio = np.concatenate(samples)
            if np.max(np.abs(audio)) < 0.02:
                continue  # Too quiet
            
            # Convert to mono WAV
            mono = audio[:, 0] if len(audio.shape) > 1 else audio
            buf = io.BytesIO()
            with wave.open(buf, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes((mono * 32767).astype(np.int16).tobytes())
            
            # Send for transcription
            b64 = base64.b64encode(buf.getvalue()).decode()
            resp = requests.post(DGX_URL, json={"audio": b64}, timeout=10)
            if resp.ok:
                text = resp.json().get("text", "")
                if text.strip():
                    print(f"🎤 {text}", flush=True)
        except Exception as e:
            print(f"E: {e}", flush=True)
            time.sleep(0.5)

if __name__ == "__main__":
    main()
