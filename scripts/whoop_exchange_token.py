#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Exchange Whoop OAuth code for access token
"""
import json
import requests
import urllib.parse

# Load credentials
with open('/home/wrenn/.secrets/whoop.json', 'r') as f:
    creds = json.load(f)

# The callback URL from Cooper
callback_url = 'http://localhost:8080/?code=Hp7HxQvgPAnt4SE2DCHXg5gYaBpClQSyrgjhLZ1SgIM.IfkccldvutLXONkSY2gs-wOmEC_-GitcoTlI9-xRb6I&scope=read%3Aprofile%20read%3Arecovery%20read%3Acycles%20read%3Asleep&state=5MSEjdDs2J6LxEGDtdvbCo0hy-yVcxSpuemoD1mFpSU'

# Parse the code
parsed = urllib.parse.urlparse(callback_url)
params = urllib.parse.parse_qs(parsed.query)
code = params['code'][0]

print(f"📝 Authorization code: {code[:20]}...")

# Exchange for access token
token_url = 'https://api.prod.whoop.com/oauth/oauth2/token'

data = {
    'grant_type': 'authorization_code',
    'code': code,
    'client_id': creds['client_id'],
    'client_secret': creds['client_secret'],
    'redirect_uri': creds['redirect_uri']
}

response = requests.post(token_url, data=data, timeout=30)

if response.status_code == 200:
    token_data = response.json()
    
    # Save the token
    creds['access_token'] = token_data['access_token']
    creds['refresh_token'] = token_data.get('refresh_token')
    creds['expires_in'] = token_data.get('expires_in')
    creds['token_type'] = token_data.get('token_type')
    
    with open('/home/wrenn/.secrets/whoop.json', 'w') as f:
        json.dump(creds, f, indent=2)
    
    import os
    os.chmod('/home/wrenn/.secrets/whoop.json', 0o600)
    
    print("✅ Access token saved to /home/wrenn/.secrets/whoop.json")
    print(f"   Token type: {token_data.get('token_type')}")
    print(f"   Expires in: {token_data.get('expires_in')} seconds")
    
    # Test API access
    headers = {'Authorization': f"Bearer {token_data['access_token']}"}
    test = requests.get('https://api.prod.whoop.com/developer/v1/user/profile/basic', headers=headers, timeout=10)
    
    if test.status_code == 200:
        profile = test.json()
        print(f"✅ Whoop API working! User: {profile.get('first_name')} {profile.get('last_name')}")
        print(f"   Email: {profile.get('email')}")
    else:
        print(f"⚠️  Profile API returned: {test.status_code}")
        print(test.text)
else:
    print(f"❌ Token exchange failed: {response.status_code}")
    print(response.text)
