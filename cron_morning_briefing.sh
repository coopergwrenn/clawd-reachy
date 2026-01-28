#!/bin/bash
# Morning briefing using GLM-4.7 (local, free!)

PROMPT="Check Cooper's calendar for today and tomorrow. Summarize any important meetings or deadlines. Keep it brief - 2-3 sentences max."

# Run GLM locally
RESPONSE=$(curl -s http://localhost:11434/api/generate -d "{
  \"model\": \"glm4:latest\",
  \"prompt\": \"$PROMPT\",
  \"stream\": false
}" | python3 -c "import sys,json; print(json.load(sys.stdin)['response'])")

# Send via Telegram
curl -s -X POST "http://localhost:18789/api/message/send" \
  -H "Authorization: Bearer e79d78c7a15a94d96fdf5a16e8297ce819ad0790a0473a27" \
  -H "Content-Type: application/json" \
  -d "{\"channel\":\"telegram\",\"message\":\"🌅 Morning Briefing\\n\\n$RESPONSE\"}"

echo "Morning briefing sent"
