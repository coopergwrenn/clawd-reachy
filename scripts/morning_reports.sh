#!/bin/bash
# Master morning report script
# Sends both daily briefing and competitor intel

set -e

SCRIPTS_DIR="/home/wrenn/clawd/scripts"
cd "$SCRIPTS_DIR"

echo "🌅 Starting morning reports..."
echo ""

# 1. Send daily briefing
echo "📊 Generating daily briefing..."
./send_morning_report.py

echo ""
echo "🔍 Generating competitor intel..."

# 2. Generate competitor intel
INTEL_BODY=$(./competitor_intel_enhanced.py)

# 3. Send competitor intel email
./venv/bin/python3 << EOF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Load credentials
with open('/home/wrenn/clawd/gmail_credentials.txt', 'r') as f:
    lines = f.readlines()
    email = lines[0].split('=')[1].strip()
    password = lines[1].split('=')[1].strip().replace(' ', '')

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = 'coopergrantwrenn@gmail.com'
msg['Subject'] = f"Competitor Intel - {datetime.now().strftime('%B %d, %Y')}"

body = '''$INTEL_BODY'''
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)
server.send_message(msg)
server.quit()

print("✅ Competitor intel email sent!")
EOF

echo ""
echo "✅ All morning reports sent!"

# Update heartbeat state
mkdir -p /home/wrenn/clawd/memory
cat > /home/wrenn/clawd/memory/heartbeat-state.json << EOF
{
  "lastChecks": {
    "morning_report": $(date +%s),
    "email": $(date +%s),
    "calendar": $(date +%s),
    "stripe": $(date +%s)
  }
}
EOF

echo "📝 Updated heartbeat state"
