#!/bin/bash
# Morning wake up scream at 7:30 AM

# Wake up animation
curl -s -X POST "http://192.168.4.75:8000/api/move/play/wake_up"
sleep 2

# Generate TTS and play
cd /home/wrenn/clawd
python3 << 'EOF'
from tts import tts
import subprocess
# Generate scream
audio = tts("COOPER! WAKE UP! IT'S SEVEN THIRTY! GET OUT OF BED RIGHT NOW! TIME TO START THE DAY!")
# Upload to Reachy
subprocess.run(['scp', audio, 'pollen@192.168.4.75:/tmp/morning.mp3'])
subprocess.run(['ssh', 'pollen@192.168.4.75', 'ffmpeg -i /tmp/morning.mp3 -ar 16000 -ac 1 /tmp/clawd_speech.wav -y 2>/dev/null && curl -s -X POST http://localhost:8766/speak'])
EOF

# Surprise animation
python3 /home/wrenn/clawd/reachy/animations.py surprise
