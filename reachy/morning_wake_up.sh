#!/bin/bash
# Morning wake-up routine for Ritchie
# Called by heartbeat at 7:30am

echo "🌅 Good morning! Waking up Ritchie..."

# 1. Start the robot backend
echo "⚡ Powering on motors..."
curl -s -X POST "http://192.168.4.75:8000/api/daemon/start?wake_up=true" > /dev/null

# 2. Start camera server
echo "👀 Starting vision..."
/home/wrenn/clawd/reachy/start_camera_server.sh > /dev/null 2>&1

# 3. Wake-up animation
echo "🎭 Wake-up animation..."
sleep 3
curl -s -X POST http://192.168.4.75:8000/api/move/goto \
  -H "Content-Type: application/json" \
  -d '{"head":{"x":0,"y":0,"z":0,"roll":0,"pitch":-25,"yaw":0},"antennas":[5,5],"duration":0.1}' > /dev/null

sleep 0.5

# Stretch and look up
curl -s -X POST http://192.168.4.75:8000/api/move/goto \
  -H "Content-Type: application/json" \
  -d '{"head":{"x":0,"y":0,"z":0,"roll":0,"pitch":5,"yaw":0},"antennas":[40,40],"duration":1.5}' > /dev/null

sleep 2

# Look around
curl -s -X POST http://192.168.4.75:8000/api/move/goto \
  -H "Content-Type: application/json" \
  -d '{"head":{"x":0,"y":0,"z":0,"roll":0,"pitch":-10,"yaw":25},"antennas":[35,35],"duration":1.0}' > /dev/null

sleep 1.5

curl -s -X POST http://192.168.4.75:8000/api/move/goto \
  -H "Content-Type: application/json" \
  -d '{"head":{"x":0,"y":0,"z":0,"roll":0,"pitch":-10,"yaw":-25},"antennas":[35,35],"duration":1.0}' > /dev/null

sleep 1.5

# Center and ready
curl -s -X POST http://192.168.4.75:8000/api/move/goto \
  -H "Content-Type: application/json" \
  -d '{"head":{"x":0,"y":0,"z":0,"roll":0,"pitch":-8,"yaw":0},"antennas":[30,30],"duration":0.8}' > /dev/null

# 4. Take a morning snapshot
echo "📸 Taking morning snapshot..."
sleep 1
curl -s http://192.168.4.75:8766/snapshot -o /tmp/morning_view_$(date +%Y%m%d).jpg

echo "✅ Ritchie is awake and ready!"
echo "   Vision: http://192.168.4.75:8766/snapshot"
echo "   Movement: http://192.168.4.75:8000/api/move/goto"
