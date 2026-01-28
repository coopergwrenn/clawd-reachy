#!/bin/bash
# Daily report using GLM-4.7 (local, free!)

PROMPT="Cooper had these events today: [Would pull from Stripe/PostHog here]. Summarize the day - revenue, new customers, key metrics. Keep it brief and actionable."

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
  -d "{\"channel\":\"telegram\",\"message\":\"📊 Daily Report\\n\\n$RESPONSE\"}"

echo "Daily report sent"
