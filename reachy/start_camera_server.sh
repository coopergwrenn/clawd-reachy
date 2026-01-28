#!/bin/bash
# Start the camera server on Reachy Mini
# Run this to enable vision (port 8766)

echo "🎥 Starting Reachy camera server..."

# Kill any existing instance
ssh pollen@192.168.4.75 "pkill -f 'app.py'" 2>/dev/null || true

# Start the server
ssh pollen@192.168.4.75 "cd /home/pollen/clawd_app && /venvs/apps_venv/bin/python3 app.py > /tmp/clawd_app.log 2>&1 &"

# Wait for it to start
sleep 3

# Test
if curl -s http://192.168.4.75:8766/ | grep -q "Clawd App"; then
    echo "✅ Camera server is running on port 8766"
    echo "📷 Test snapshot: curl http://192.168.4.75:8766/snapshot -o photo.jpg"
else
    echo "❌ Camera server failed to start. Check logs:"
    echo "   ssh pollen@192.168.4.75 'cat /tmp/clawd_app.log'"
fi
