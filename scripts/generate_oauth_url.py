#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Generate OAuth URL for manual authorization - SECURE VERSION
"""
import json
from google_auth_oauthlib.flow import Flow

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.readonly'
]

CREDENTIALS_FILE = '/home/wrenn/.secrets/google-oauth.json'

# Create flow with manual redirect
flow = Flow.from_client_secrets_file(
    CREDENTIALS_FILE,
    scopes=SCOPES,
    redirect_uri='http://localhost:8080'
)

auth_url, _ = flow.authorization_url(prompt='consent')

print("\n" + "="*80)
print("CALENDAR OAUTH AUTHORIZATION")
print("="*80)
print("\n1. Click this URL:\n")
print(f"   {auth_url}\n")
print("2. Log in with: coopergrantwrenn@gmail.com")
print("3. Click 'Allow'")
print("4. You'll be redirected to localhost (will show error - that's OK)")
print("5. Copy the ENTIRE URL from your browser")
print("6. Send it to me via Telegram\n")
print("="*80 + "\n")
