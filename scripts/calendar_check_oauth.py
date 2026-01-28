#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Check Google Calendar for today's events using OAuth token
"""
import json
import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_FILE = '/home/wrenn/clawd/google-calendar-token.json'
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.readonly'
]

def get_todays_events():
    try:
        if not os.path.exists(TOKEN_FILE):
            return {
                'note': 'Calendar OAuth not set up yet - run setup_calendar_oauth.py',
                'events': []
            }
        
        # Load credentials from token file
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
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
