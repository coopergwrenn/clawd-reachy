# Reachy Mini API Reference

**Base URL:** `http://192.168.4.75:8000`

## Core Endpoints

### Check Status
```bash
GET /api/daemon/status
```
Returns: robot state, backend_status (ready: true/false), version, IP

### Start Backend (Wake Up)
```bash
POST /api/daemon/start?wake_up=true
```
Returns: `{"job_id": "..."}`
This turns on the robot's motor control system

### Stop Backend (Sleep)
```bash
POST /api/daemon/stop
```
Turns off motor control (robot goes limp)

### Movement
```bash
POST /api/move/goto
Content-Type: application/json

{
  "head": {
    "x": 0,
    "y": 0,
    "z": 0,
    "roll": 0,    # -30 to 30
    "pitch": -15, # -30 to 10  (negative = looking down)
    "yaw": 0      # -45 to 45
  },
  "antennas": [25, 25],  # 0-100 (0=down, 100=up)
  "duration": 1.0        # seconds
}
```
Returns: `{"uuid": "..."}`

### WebSocket for Real-Time Updates
```
WebSocket: ws://192.168.4.75:8000/api/move/ws/updates
```

### Apps Management
```bash
GET /api/apps/list-available/installed
GET /api/apps/current-app-status
```

### Health Check
```bash
POST /health-check
```

## Emotion Presets (via animations.py)

- sleeping: head down, antennas down
- idle: neutral, alert
- happy: head up, antennas perky
- working: slight tilt, focused
- thinking: head tilted, asymmetric antennas
- surprised: quick head up, antennas shoot up
- sad: head drooped, antennas down
- excited: bouncy, antennas very up

## Autonomous Control Strategy

**Morning (7:30am):**
1. POST /api/daemon/start?wake_up=true
2. Execute wake_up animation
3. Send morning reports

**Throughout Day:**
- Check status periodically
- React to business events with emotions
- Look around every few hours

**Evening (before end of day):**
1. Execute sleeping animation
2. POST /api/daemon/stop (optional - saves power)

## Notes

- Backend "ready" status can be false even when movement works
- Camera requires separate app (conversation_app or greetings_app)
- Robot can be controlled even when backend_status.ready=false
- Physical power button on back is separate from API control
