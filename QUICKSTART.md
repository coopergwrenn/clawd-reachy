# Quick Start

## Prerequisites
- NVIDIA DGX Spark (or similar)
- Reachy Mini robot
- Python 3.10+

## Setup (5 minutes)

1. **On DGX: Start transcription server**
```bash
python transcription_server.py
```

2. **On Reachy: Start bridge service**
```bash
python scripts/reachy_bridge.py
```

3. **On DGX: Start demo monitor**
```bash
tmux new-session -d -s demo "python scripts/simple_monitor.py"
```

4. **Demo questions:**
- "Hey Reachy, can you hear me?"
- "Can you see me?"
- "What can you do?"
- "How does it feel to have a body?"

## Troubleshooting
- If audio doesn't play: Restart reachy_bridge.py
- If not hearing: Check transcription server on port 8777
- If movements don't work: Start Reachy backend via web UI
