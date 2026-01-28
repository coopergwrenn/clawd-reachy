#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Check Gmail for urgent/important emails from last 24 hours
"""
import json
import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def load_credentials():
    creds_path = '/home/wrenn/clawd/gmail-credentials.json'
    with open(creds_path, 'r') as f:
        creds_data = json.load(f)
    
    creds = Credentials(
        token=creds_data.get('token'),
        refresh_token=creds_data.get('refresh_token'),
        token_uri=creds_data.get('token_uri'),
        client_id=creds_data.get('client_id'),
        client_secret=creds_data.get('client_secret'),
        scopes=creds_data.get('scopes', ['https://www.googleapis.com/auth/gmail.readonly'])
    )
    return creds

def get_recent_emails(hours=24):
    try:
        creds = load_credentials()
        service = build('gmail', 'v1', credentials=creds)
        
        # Calculate time threshold
        after_date = datetime.now() - timedelta(hours=hours)
        after_timestamp = int(after_date.timestamp())
        
        # Search for unread emails from last 24h
        query = f'is:unread after:{after_timestamp}'
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=20
        ).execute()
        
        messages = results.get('messages', [])
        
        emails = []
        for msg in messages:
            message = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()
            
            headers = {h['name']: h['value'] for h in message['payload']['headers']}
            
            emails.append({
                'from': headers.get('From', 'Unknown'),
                'subject': headers.get('Subject', 'No subject'),
                'date': headers.get('Date', ''),
                'id': msg['id']
            })
        
        return emails
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    emails = get_recent_emails()
    print(json.dumps(emails, indent=2))
