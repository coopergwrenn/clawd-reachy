#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Get latest Whoop data - recovery, sleep, cycles
"""
import json
import requests
from datetime import datetime, timedelta

def load_credentials():
    with open('/home/wrenn/.secrets/whoop.json', 'r') as f:
        return json.load(f)

def get_latest_health_data():
    """Get most recent recovery and sleep data"""
    try:
        creds = load_credentials()
        headers = {'Authorization': f"Bearer {creds['access_token']}"}
        
        # Get last 7 days of data
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)
        
        # Get recovery data
        recovery_url = 'https://api.prod.whoop.com/developer/v1/recovery'
        recovery_params = {
            'limit': 7,
            'start': start_time.isoformat() + 'Z',
            'end': end_time.isoformat() + 'Z'
        }
        
        recovery_resp = requests.get(recovery_url, headers=headers, params=recovery_params, timeout=10)
        
        # Get sleep data
        sleep_url = 'https://api.prod.whoop.com/developer/v1/activity/sleep'
        sleep_params = {
            'limit': 7,
            'start': start_time.isoformat() + 'Z',
            'end': end_time.isoformat() + 'Z'
        }
        
        sleep_resp = requests.get(sleep_url, headers=headers, params=sleep_params, timeout=10)
        
        result = {
            'recovery': recovery_resp.json() if recovery_resp.status_code == 200 else {'error': recovery_resp.text},
            'sleep': sleep_resp.json() if sleep_resp.status_code == 200 else {'error': sleep_resp.text},
            'timestamp': datetime.now().isoformat()
        }
        
        # Extract latest if available
        if recovery_resp.status_code == 200 and recovery_resp.json().get('records'):
            latest_recovery = recovery_resp.json()['records'][0]
            result['latest_recovery'] = {
                'score': latest_recovery['score']['recovery_score'],
                'hrv': latest_recovery['score']['hrv_rmssd_milli'],
                'resting_hr': latest_recovery['score']['resting_heart_rate'],
                'created_at': latest_recovery['created_at']
            }
        
        if sleep_resp.status_code == 200 and sleep_resp.json().get('records'):
            latest_sleep = sleep_resp.json()['records'][0]
            result['latest_sleep'] = {
                'performance': latest_sleep['score']['sleep_performance_percentage'],
                'duration_hours': latest_sleep['score']['stage_summary']['total_in_bed_time_milli'] / 1000 / 60 / 60,
                'efficiency': latest_sleep['score']['sleep_efficiency_percentage'],
                'created_at': latest_sleep['created_at']
            }
        
        return result
        
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    data = get_latest_health_data()
    print(json.dumps(data, indent=2))
