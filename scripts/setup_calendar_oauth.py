#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Set up Google Calendar OAuth - generates token for calendar access
This script opens a browser for one-time authorization
"""
import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.readonly'
]

CREDENTIALS_FILE = '/home/wrenn/.secrets/google-oauth.json'
TOKEN_FILE = '/home/wrenn/.secrets/google-calendar.json'

def main():
    creds = None
    
    # Check if token already exists and is valid
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If no valid credentials, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Starting OAuth flow...")
            print("This will open a browser window for authorization.")
            print("Log in with: coopergrantwrenn@gmail.com")
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8765)
        
        # Save credentials
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        
        print(f"✅ Token saved to {TOKEN_FILE}")
    else:
        print("✅ Valid token already exists!")
    
    # Test calendar access
    from googleapiclient.discovery import build
    service = build('calendar', 'v3', credentials=creds)
    
    result = service.calendarList().list().execute()
    calendars = result.get('items', [])
    
    print(f"\n✅ Calendar access working! Found {len(calendars)} calendars")
    for cal in calendars[:3]:
        print(f"  - {cal['summary']}")

if __name__ == '__main__':
    main()
