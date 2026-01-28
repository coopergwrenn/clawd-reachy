#!/usr/bin/env python3
"""Reachy bridge - ONE connection for listening AND playback."""
import sys, time, base64, wave, io, requests, threading, json
sys.path.insert(0, '/venvs/apps_venv/lib/python3.12/site-packages')
from http.server import HTTPServer, BaseHTTPRequestHandler
from reachy_mini import ReachyMini
import numpy as np

robot = None
DGX_URL = "http://192.168.4.76:8777/transcribe"
CHUNK = 1

def listener_loop():
    """Continuous listening."""
    global robot
    print("🎧 Listener starting...", flush=True)
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
                continue
            
            mono = audio[:, 0] if len(audio.shape) > 1 else audio
            buf = io.BytesIO()
            with wave.open(buf, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes((mono * 32767).astype(np.int16).tobytes())
            
            b64 = base64.b64encode(buf.getvalue()).decode()
            resp = requests.post(DGX_URL, json={"audio": b64}, timeout=10)
            if resp.ok:
                text = resp.json().get("text", "")
                if text.strip():
                    print(f"🎤 {text}", flush=True)
        except Exception as e:
            print(f"E: {e}", flush=True)
            time.sleep(0.5)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/play/'):
            try:
                num = int(self.path.split('/')[-1])
                
                with wave.open(f"/tmp/response{num}.wav", 'rb') as wf:
                    frames = wf.readframes(wf.getnframes())
                    sr = wf.getframerate()
                    nc = wf.getnchannels()
                    audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
                    if nc == 1:
                        audio = np.column_stack([audio, audio])
                
                robot.media.start_playing()
                robot.media.push_audio_sample(audio)
                time.sleep(len(audio) / sr + 0.5)
                robot.media.stop_playing()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "played": num}).encode())
                print(f"Played response {num}", flush=True)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())

if __name__ == "__main__":
    print("Connecting to robot...", flush=True)
    robot = ReachyMini(media_backend="default")
    print("✅ Connected!", flush=True)
    
    # Start listener in background thread
    threading.Thread(target=listener_loop, daemon=True).start()
    
    # Run HTTP server
    print("Starting HTTP server on port 9000...", flush=True)
    HTTPServer(('0.0.0.0', 9000), Handler).serve_forever()
