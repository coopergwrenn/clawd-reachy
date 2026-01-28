#!/usr/bin/env python3
"""Transcription server - receives audio, transcribes with Whisper, notifies Clawd."""

import os
import sys
import base64
import tempfile
import wave
from datetime import datetime

# Use the venv
sys.path.insert(0, '/home/wrenn/clawd/reachy-venv/lib/python3.12/site-packages')

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from faster_whisper import WhisperModel

app = FastAPI(title="Clawd Transcription Server")

# Load faster-whisper (4-5x faster than standard Whisper!)
print("Loading faster-whisper tiny model...")
model = WhisperModel("tiny", device="cpu", compute_type="int8")
print("✅ faster-whisper ready")

# File to write transcriptions (Clawd can monitor this)
TRANSCRIPT_FILE = "/home/wrenn/clawd/reachy/heard.txt"

@app.get("/")
async def root():
    return {"status": "ok", "service": "Clawd Transcription"}

@app.post("/transcribe")
async def transcribe(data: dict):
    """Receive base64 audio, transcribe, save to file."""
    audio_b64 = data.get("audio", "")
    if not audio_b64:
        return JSONResponse({"error": "No audio"}, status_code=400)
    
    try:
        # Decode audio
        audio_bytes = base64.b64decode(audio_b64)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_bytes)
            temp_path = f.name
        
        # Transcribe with faster-whisper
        segments, info = model.transcribe(temp_path, language="en", beam_size=1, vad_filter=True)
        text = " ".join([seg.text for seg in segments]).strip()
        
        # Clean up
        os.unlink(temp_path)
        
        # Save to file if there's actual speech
        if text and len(text) > 2:
            timestamp = datetime.now().strftime("%H:%M:%S")
            with open(TRANSCRIPT_FILE, "a") as f:
                f.write(f"[{timestamp}] {text}\n")
            print(f"🎤 Heard: {text}")
        
        return {"text": text}
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/latest")
async def latest():
    """Get latest transcription."""
    if os.path.exists(TRANSCRIPT_FILE):
        with open(TRANSCRIPT_FILE, "r") as f:
            lines = f.readlines()
            if lines:
                return {"latest": lines[-1].strip(), "all": [l.strip() for l in lines[-10:]]}
    return {"latest": None, "all": []}

@app.post("/clear")
async def clear():
    """Clear transcription history."""
    if os.path.exists(TRANSCRIPT_FILE):
        os.unlink(TRANSCRIPT_FILE)
    return {"status": "cleared"}

if __name__ == "__main__":
    # Clear old transcripts
    if os.path.exists(TRANSCRIPT_FILE):
        os.unlink(TRANSCRIPT_FILE)
    print("🎧 Transcription server starting on port 8777...")
    uvicorn.run(app, host="0.0.0.0", port=8777)
