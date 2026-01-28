#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Check X (Twitter) for mentions and important activity
"""
import json
import tweepy
from datetime import datetime, timedelta

def load_credentials():
    with open('/home/wrenn/clawd/x-credentials.json', 'r') as f:
        creds = json.load(f)
    return creds

def get_mentions(hours=24):
    try:
        creds = load_credentials()
        
        # Set up tweepy
        auth = tweepy.OAuthHandler(creds['apiKey'], creds['apiSecret'])
        auth.set_access_token(creds['accessToken'], creds['accessSecret'])
        api = tweepy.API(auth)
        
        # Get mentions timeline
        mentions = api.mentions_timeline(count=50)
        
        # Filter to last 24h
        cutoff = datetime.now() - timedelta(hours=hours)
        recent_mentions = []
        
        for mention in mentions:
            if mention.created_at.replace(tzinfo=None) > cutoff:
                recent_mentions.append({
                    'user': mention.user.screen_name,
                    'text': mention.text,
                    'created_at': mention.created_at.isoformat(),
                    'id': mention.id
                })
        
        return recent_mentions
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    mentions = get_mentions()
    print(json.dumps(mentions, indent=2))
