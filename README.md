# Reachy Mini Integration

This directory contains all the code needed to run Clawd on the Reachy Mini robot.

## Architecture

```
DGX (192.168.4.76)                    Reachy Mini (192.168.4.75)
┌─────────────────────┐               ┌─────────────────────┐
│ transcription_server│◄──────────────│ listener.py         │
│ (port 8777)         │   audio       │ (captures mic)      │
│                     │               │                     │
│ demo_monitor.sh     │──────────────►│ play_response.py    │
│ (watches heard.txt) │   SSH cmd     │ (plays audio)       │
│                     │               │                     │
│ animations.py       │──────────────►│ Reachy Daemon       │
│                     │   HTTP API    │ (port 8000)         │
└─────────────────────┘               └─────────────────────┘
```

## Components

### On DGX (192.168.4.76)
- **transcription_server.py** - Whisper transcription server on port 8777
- **demo_monitor.sh** - Monitors heard.txt for triggers, runs responses
- **animations.py** - Sends emotion/animation commands to Reachy API
- **heard.txt** - File where transcriptions are written

### On Reachy (192.168.4.75)
- **listener.py** - Captures audio, sends to DGX for transcription
- **play_response.py** - Plays WAV files through Reachy's speaker
- **response1-4.wav** - Pre-generated TTS responses in /tmp/

## Setup

### 1. Start Reachy Backend
```bash
curl -X POST "http://192.168.4.75:8000/api/daemon/start?wake_up=true"
```

### 2. Start Transcription Server (on DGX)
```bash
cd /home/wrenn/clawd/reachy
python transcription_server.py
```

### 3. Deploy to Reachy
```bash
./scripts/deploy.sh
```

### 4. Start Listener (on Reachy)
```bash
ssh pollen@192.168.4.75 'cd ~/clawd_app && python listener.py &'
```

### 5. Start Demo Monitor (on DGX)
```bash
bash /home/wrenn/clawd/reachy/demo_monitor.sh
```

## Demo Flow

1. **Q1: "Hey Reachy, can you hear me?"**
   - Wake up animation
   - Play response1.wav
   - Happy animation

2. **Q2: "Can you see me?"**
   - Play response2.wav
   - Look animation
   - Take photo, send to Telegram

3. **Q3: "What can you do?"**
   - Play response3.wav
   - Wiggle animation

4. **Q4: "How does it feel to have a body?"**
   - Play response4.wav
   - Think animation

## Troubleshooting

### Audio not playing
- Check if backend is running: `curl http://192.168.4.75:8000/api/daemon/status`
- Start backend with: `curl -X POST "http://192.168.4.75:8000/api/daemon/start?wake_up=true"`

### Listener not hearing
- Check if listener is running: `ssh pollen@192.168.4.75 'ps aux | grep listener'`
- Check listener log: `ssh pollen@192.168.4.75 'tail /tmp/listener.log'`

### Transcriptions not appearing
- Check transcription server: `curl http://localhost:8777/`
- Check heard.txt: `tail /home/wrenn/clawd/reachy/heard.txt`

## Updated Architecture (v2 - Using Bridge)

**Key Improvement:** Single unified bridge service on Reachy eliminates connection conflicts!

### Reachy Bridge Service
The `reachy_bridge.py` runs on Reachy and provides:
- HTTP endpoint for audio playback (`/play/<num>`)
- Background listening thread (sends to DGX transcription)
- Single ReachyMini connection (no conflicts!)

### Setup v2
1. Start transcription server on DGX (in tmux)
2. Start reachy_bridge.py on Reachy
3. Start simple_monitor.py on DGX (in tmux)

### Speed Optimizations
- 1-second audio chunks (faster detection)
- faster-whisper (4-5x speed boost)
- HTTP bridge (no SSH overhead)
- Threading (non-blocking responses)
