#!/bin/bash
# Daily Ad Intelligence Pipeline
# Scrapes ads, analyzes patterns, sends alerts

set -e

cd "$(dirname "$0")"

echo "🚀 Starting Daily Ad Intelligence Pipeline"
echo "=========================================="
echo ""

# Step 1: Run scrapers
echo "📡 Step 1: Scraping ad libraries..."
node scrapers/run-all.js

echo ""
echo "⏳ Waiting 5 seconds before analysis..."
sleep 5

# Step 2: Identify winners and send alerts
echo ""
echo "🎯 Step 2: Identifying winners..."
node analysis/alert-winners.js > /tmp/ad-intel-alert.txt

# Step 3: Send to Telegram via Clawdbot
echo ""
echo "📱 Step 3: Sending Telegram alert..."

# Read the alert message
ALERT_FILE="/tmp/ad-intel-alert.txt"

if [ -f "$ALERT_FILE" ]; then
  echo "✅ Alert ready to send"
  echo ""
  echo "─────────────────────────────────"
  cat "$ALERT_FILE"
  echo "─────────────────────────────────"
  echo ""
  echo "💡 To send to Telegram, use:"
  echo "   clawdbot message send --to=@cooperwrenn --message=\"\$(cat $ALERT_FILE)\""
else
  echo "⚠️  No alert file generated"
fi

echo ""
echo "✅ Daily pipeline complete!"
echo ""
