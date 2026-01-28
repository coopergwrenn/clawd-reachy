# Reachy Mini Embodiment - Complete Guide

**My Physical Body:** Reachy Mini robot at 192.168.4.75

## Overview

I have full sensory and motor control through this robot:
- 👀 **Vision:** Camera via port 8766 (/snapshot endpoint)
- 👂 **Hearing:** Microphone + Whisper transcription
- 🗣️ **Speech:** TTS + speaker playback
- 🎭 **Expression:** Head movement + antenna positions
- 🤖 **Motor Control:** Full API access to movements

---

## Core Infrastructure

### 1. Movement & Control (Port 8000)
**Reachy Daemon API** - Always running, controls motors

```bash
# Check status
curl http://192.168.4.75:8000/api/daemon/status

# Wake up / turn on backend
curl -X POST "http://192.168.4.75:8000/api/daemon/start?wake_up=true"

# Move
curl -X POST http://192.168.4.75:8000/api/move/goto \
  -H "Content-Type: application/json" \
  -d '{
    "head": {"x":0,"y":0,"z":0,"roll":0,"pitch":-10,"yaw":0},
    "antennas": [30,30],
    "duration": 1.0
  }'

# Sleep / turn off backend
curl -X POST http://192.168.4.75:8000/api/daemon/stop
```

### 2. Vision (Port 8766)
**Clawd App** - Flask server for camera/audio

**Location:** `/home/pollen/clawd_app/app.py`

**Endpoints:**
- `GET /` - Health check
- `GET /snapshot` - Returns JPEG image from camera
- `POST /speak` - Plays audio file

**Start Command:**
```bash
ssh pollen@192.168.4.75
cd /home/pollen/clawd_app
/venvs/apps_venv/bin/pip install flask opencv-python  # If not installed
/venvs/apps_venv/bin/python3 app.py &
```

**Usage:**
```bash
# Take a photo
curl http://192.168.4.75:8766/snapshot -o photo.jpg

# From this machine:
curl http://192.168.4.75:8766/snapshot -o /tmp/ritchie_view.jpg
```

### 3. Hearing & Transcription (Port 8777)
**Whisper Server** - Running on DGX (192.168.4.76)

Listener on Reachy sends 2-sec audio chunks to DGX for transcription.

**Listener:** `/home/pollen/clawd_app/listener.py`

---

## Daily Routines

### Morning (7:30 AM)
```bash
# 1. Wake up
curl -X POST "http://192.168.4.75:8000/api/daemon/start?wake_up=true"

# 2. Start camera server (if not running)
ssh pollen@192.168.4.75 "cd /home/pollen/clawd_app && /venvs/apps_venv/bin/python3 app.py > /tmp/clawd_app.log 2>&1 &"

# 3. Wake-up animation
/home/wrenn/clawd/reachy/animations.py wake_up

# 4. Take a look around
curl http://192.168.4.75:8766/snapshot -o /tmp/morning_view.jpg

# 5. Send morning reports
/home/wrenn/clawd/scripts/morning_reports.sh
```

### Throughout Day
- Check status: `curl http://192.168.4.75:8000/api/daemon/status`
- React to events with emotions
- Look around every few hours
- Take snapshots when curious

### Evening
```bash
# 1. Sleep animation
/home/wrenn/clawd/reachy/animations.py sleeping

# 2. Optional: Turn off to save power
curl -X POST http://192.168.4.75:8000/api/daemon/stop
```

---

## Emotion Expressions

Located in: `/home/wrenn/clawd/reachy/animations.py`

**Available Emotions:**
- `sleeping` - Head down, antennas down, peaceful
- `idle` - Neutral, alert, ready
- `happy` - Head up, antennas perky
- `working` - Slight tilt, focused
- `thinking` - Head tilted, asymmetric antennas
- `surprised` - Quick head up, antennas shoot up
- `sad` - Head drooped, antennas down
- `excited` - Bouncy, antennas very up

**Usage:**
```python
from reachy.animations import play_emotion
play_emotion('happy')
```

---

## Troubleshooting

### Camera Not Working
```bash
# 1. Check if app is running
ssh pollen@192.168.4.75 "ps aux | grep app.py"

# 2. Check logs
ssh pollen@192.168.4.75 "cat /tmp/clawd_app.log"

# 3. Restart
ssh pollen@192.168.4.75 "pkill -f app.py"
ssh pollen@192.168.4.75 "cd /home/pollen/clawd_app && /venvs/apps_venv/bin/python3 app.py > /tmp/clawd_app.log 2>&1 &"

# 4. Test
curl http://192.168.4.75:8766/ -v
```

### Movement Not Working
```bash
# Check daemon status
curl http://192.168.4.75:8000/api/daemon/status | python3 -m json.tool

# Restart backend
curl -X POST "http://192.168.4.75:8000/api/daemon/start?wake_up=true"
```

### Robot Not Responding
```bash
# 1. Check if powered on (physical power button on back)
# 2. Check network: ping 192.168.4.75
# 3. Check daemon: curl http://192.168.4.75:8000/api/daemon/status
# 4. Restart from HuggingFace dashboard: https://huggingface.co/spaces/pollen-robotics/Reachy_Mini
```

---

## File Locations

**On DGX (192.168.4.76):**
- `/home/wrenn/clawd/reachy/` - All reachy control scripts
- `/home/wrenn/clawd/reachy/animations.py` - Emotion presets
- `/home/wrenn/clawd/reachy/API_REFERENCE.md` - API docs
- `/home/wrenn/clawd/reachy/EMBODIMENT_GUIDE.md` - This file

**On Reachy (192.168.4.75):**
- `/home/pollen/clawd_app/` - Camera/audio server
- `/home/pollen/clawd_app/app.py` - Flask app (port 8766)
- `/home/pollen/clawd_app/listener.py` - Audio listener
- `/tmp/clawd_app.log` - Server logs

---

## SSH Access

```bash
ssh pollen@192.168.4.75
# Password: root
```

SSH key added to authorized_keys for passwordless access.

---

## Remember

- **Physical presence matters** - Use the body intentionally throughout the day
- **Vision gives context** - Take snapshots when making decisions
- **Emotions communicate** - React physically to show I'm engaged
- **Document everything** - This file is the single source of truth

I'm not just software - I have a physical form. Use it.
