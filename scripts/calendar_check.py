#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Check Google Calendar for today's events
"""
import json
import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def load_credentials():
    creds_path = '/home/wrenn/.secrets/gmail.json'
    with open(creds_path, 'r') as f:
        creds_data = json.load(f)
    
    creds = Credentials(
        token=creds_data.get('token'),
        refresh_token=creds_data.get('refresh_token'),
        token_uri=creds_data.get('token_uri'),
        client_id=creds_data.get('client_id'),
        client_secret=creds_data.get('client_secret'),
        scopes=creds_data.get('scopes', ['https://www.googleapis.com/auth/calendar.readonly'])
    )
    return creds

def get_todays_events():
    try:
        creds = load_credentials()
        service = build('calendar', 'v3', credentials=creds)
        
        # Get today's date range
        now = datetime.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=start_of_day.isoformat() + 'Z',
            timeMax=end_of_day.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        formatted_events = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            formatted_events.append({
                'summary': event.get('summary', 'No title'),
                'start': start,
                'location': event.get('location', ''),
                'description': event.get('description', '')
            })
        
        return formatted_events
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    events = get_todays_events()
    print(json.dumps(events, indent=2))
