#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Google Calendar OAuth authentication
Run this once to get a token for calendar access
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
TOKEN_FILE = '/home/wrenn/clawd/google-oauth-token.json'

def authenticate():
    """Run OAuth flow and save token"""
    creds = None
    
    # Check if we already have a token
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)
        
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        
        print(f"✅ Token saved to {TOKEN_FILE}")
    else:
        print("✅ Valid token already exists!")
    
    return creds

if __name__ == '__main__':
    authenticate()
