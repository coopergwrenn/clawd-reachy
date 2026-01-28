#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Check Whoop health data - recovery, sleep, HRV
"""
import json
import requests
from datetime import datetime, timedelta

def load_credentials():
    with open('/home/wrenn/.secrets/whoop.json', 'r') as f:
        return json.load(f)

def get_recovery_data():
    """Get today's recovery data from Whoop"""
    try:
        creds = load_credentials()
        
        headers = {
            'Authorization': f"Bearer {creds['access_token']}"
        }
        
        # Get user profile first
        profile_url = 'https://api.prod.whoop.com/developer/v1/user/profile/basic'
        profile = requests.get(profile_url, headers=headers, timeout=10)
        
        if profile.status_code != 200:
            return {'error': f'Profile API failed: {profile.status_code} - {profile.text}'}
        
        user_id = profile.json()['user_id']
        
        # Get recovery data for today
        # Whoop API: Get cycles from last 24 hours
        end_time = datetime.now()
        start_time = end_time - timedelta(days=1)
        
        recovery_url = f'https://api.prod.whoop.com/developer/v1/recovery'
        params = {
            'start': start_time.isoformat() + 'Z',
            'end': end_time.isoformat() + 'Z'
        }
        
        recovery = requests.get(recovery_url, headers=headers, params=params, timeout=10)
        
        if recovery.status_code == 200:
            data = recovery.json()
            return {
                'user_id': user_id,
                'recovery_data': data,
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {'error': f'Recovery API failed: {recovery.status_code} - {recovery.text}'}
            
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    data = get_recovery_data()
    print(json.dumps(data, indent=2))
