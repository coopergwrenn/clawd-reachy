#!/usr/bin/env python3
import json
import webbrowser
import http.server
import socketserver
import urllib.parse
from pathlib import Path

# Load credentials
with open('/home/wrenn/clawd/google-oauth-credentials.json') as f:
    creds = json.load(f)['installed']

client_id = creds['client_id']
client_secret = creds['client_secret']
redirect_uri = 'http://localhost:8888'

# Step 1: Generate auth URL
auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=https://www.googleapis.com/auth/gmail.modify&access_type=offline"

print(f"Opening browser for Gmail authentication...")
print(f"Auth URL: {auth_url}\n")

# Step 2: Start local server to catch redirect
auth_code = None

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed_url = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_url.query)
        
        if 'code' in params:
            auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Success!</h1><p>You can close this window and return to the terminal.</p></body></html>')
        else:
            self.send_response(400)
            self.end_headers()

with socketserver.TCPServer(('', 8888), Handler) as httpd:
    webbrowser.open(auth_url)
    print("Waiting for authentication...")
    
    # Wait for redirect
    while auth_code is None:
        httpd.handle_request()

print(f"Got auth code: {auth_code}\n")

# Step 3: Exchange code for token
import urllib.request
token_data = urllib.parse.urlencode({
    'code': auth_code,
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri,
    'grant_type': 'authorization_code'
}).encode()

token_req = urllib.request.Request(
    'https://oauth2.googleapis.com/token',
    data=token_data,
    method='POST'
)

with urllib.request.urlopen(token_req) as response:
    token_response = json.loads(response.read())

# Save token
token_file = Path('/home/wrenn/clawd/gmail_token.json')
token_file.write_text(json.dumps(token_response, indent=2))

print(f"✓ Gmail token saved to {token_file}")
print(f"Access token: {token_response['access_token'][:50]}...")
