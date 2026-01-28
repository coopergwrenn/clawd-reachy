#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Generate Whoop OAuth authorization URL
"""
import json
import urllib.parse

# Load credentials
with open('/home/wrenn/.secrets/whoop.json', 'r') as f:
    creds = json.load(f)

# Generate authorization URL
params = {
    'client_id': creds['client_id'],
    'redirect_uri': creds['redirect_uri'],
    'response_type': 'code',
    'scope': ' '.join(creds['scopes'])
}

auth_url = f"https://api.prod.whoop.com/oauth/oauth2/auth?{urllib.parse.urlencode(params)}"

print("\n" + "="*80)
print("WHOOP HEALTH DATA AUTHORIZATION")
print("="*80)
print("\n1. Click this URL:\n")
print(f"   {auth_url}\n")
print("2. Log in with your Whoop account")
print("3. Click 'Allow' to grant access to recovery, cycles, and sleep data")
print("4. You'll be redirected to localhost (will show error - that's OK)")
print("5. Copy the ENTIRE URL from your browser")
print("6. Send it to me via Telegram\n")
print("="*80 + "\n")
