#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Exchange OAuth code for access token - SECURE VERSION
"""
import os
import json
from google_auth_oauthlib.flow import Flow

# Allow http for localhost
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.readonly'
]

CREDENTIALS_FILE = '/home/wrenn/.secrets/google-oauth.json'
TOKEN_FILE = '/home/wrenn/.secrets/google-calendar.json'

# Create flow
flow = Flow.from_client_secrets_file(
    CREDENTIALS_FILE,
    scopes=SCOPES,
    redirect_uri='http://localhost:8080'
)

# The authorization URL you got
auth_response = 'http://localhost:8080/?state=5yfa2gVDe5ZHmXoh00CaDhvDKo1arV&code=4/0ASc3gC2AWpm_YfDbo2WoeCckgd3GC3eJ3dfnzhyXvrcbwfraxUR4QT1Qu-JTAtPBSqaiQw&scope=https://www.googleapis.com/auth/gmail.readonly%20https://www.googleapis.com/auth/calendar.readonly'

# Exchange code for token
flow.fetch_token(authorization_response=auth_response)

# Get credentials
creds = flow.credentials

# Save token
with open(TOKEN_FILE, 'w') as token:
    token.write(creds.to_json())

os.chmod(TOKEN_FILE, 0o600)

print(f"✅ Token saved to {TOKEN_FILE}")

# Test calendar access
from googleapiclient.discovery import build

service = build('calendar', 'v3', credentials=creds)
result = service.calendarList().list().execute()
calendars = result.get('items', [])

print(f"✅ Calendar access working! Found {len(calendars)} calendars")
for cal in calendars[:5]:
    print(f"  - {cal['summary']}")
