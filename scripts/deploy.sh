#!/bin/bash
# Deploy Clawd scripts to Reachy Mini

REACHY_HOST="pollen@192.168.4.75"
REACHY_APP_DIR="~/clawd_app"

echo "🚀 Deploying to Reachy Mini..."

# Create app directory
ssh $REACHY_HOST "mkdir -p $REACHY_APP_DIR"

# Copy scripts
scp /home/wrenn/clawd/reachy/scripts/listener.py $REACHY_HOST:$REACHY_APP_DIR/
scp /home/wrenn/clawd/reachy/scripts/play_response.py $REACHY_HOST:/tmp/

echo "✅ Scripts deployed!"

# Generate and upload TTS responses
echo "🎤 Generating TTS responses..."

# These will be generated fresh each time or can use pre-existing
if [ -f /tmp/response1.mp3 ]; then
    echo "Using existing TTS files..."
else
    echo "TTS files need to be generated via Clawd TTS tool"
fi

echo "📦 Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Start Reachy backend: curl -X POST 'http://192.168.4.75:8000/api/daemon/start?wake_up=true'"
echo "2. Start listener: ssh $REACHY_HOST 'cd ~/clawd_app && python listener.py > /tmp/listener.log 2>&1 &'"
echo "3. Start demo monitor: bash /home/wrenn/clawd/reachy/demo_monitor.sh"
