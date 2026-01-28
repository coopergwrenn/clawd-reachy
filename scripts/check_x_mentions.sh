#!/bin/bash
# Quick X mention check using xAI Grok API

XAI_KEY="xai-sUZkGRqlsZUPEJ7B8C93if63dfyw2bXkIerHIQWfVVHgiM0Oiw8YjSU5IqjqD58yaaa0cZIEji1dQDOS"

curl -s --max-time 30 https://api.x.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_KEY" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Search X for any recent posts (last 24 hours) mentioning @coopwrenn or discussing \"Yours Truly\" (the handwritten card company). If you find any, list them with author and text. If none found, say \"No mentions found.\""
      }
    ],
    "model": "grok-4-latest",
    "stream": false,
    "temperature": 0
  }' | python3 -c "import sys,json; r=json.load(sys.stdin); print(r['choices'][0]['message']['content'])"
