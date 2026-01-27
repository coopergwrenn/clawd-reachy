#!/usr/bin/env python3
import sys, wave, time
sys.path.insert(0, '/venvs/apps_venv/lib/python3.12/site-packages')
import numpy as np
from reachy_mini import ReachyMini

num = sys.argv[1] if len(sys.argv) > 1 else "1"
robot = ReachyMini(media_backend="default")

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
print(f"Played response {num}")
