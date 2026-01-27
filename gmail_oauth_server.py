#!/usr/bin/env python3
import json
import http.server
import urllib.parse
import webbrowser
from pathlib import Path

# Load OAuth credentials
with open('/home/wrenn/clawd/google-oauth-credentials.json') as f:
    creds = json.load(f)['installed']

client_id = creds['client_id']
client_secret = creds['client_secret']
redirect_uri = 'http://localhost:8888/callback'

# Generate auth URL
auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=https://www.googleapis.com/auth/gmail.modify&access_type=offline&prompt=consent"

print(f"\n🔐 Gmail OAuth Setup")
print(f"=" * 60)
print(f"\n1. Open this URL in your browser:\n")
print(f"{auth_url}\n")
print(f"2. Log in with coopergwrenn@gmail.com")
print(f"3. Click 'Allow'")
print(f"4. You'll be redirected (the page may error, that's OK)")
print(f"5. Come back here and I'll have your token\n")
print(f"=" * 60)
print(f"\nWaiting for authorization...\n")

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
            html = b'<html><body style="font-family:Arial"><h1>Success!</h1><p>Authorization complete. Return to the terminal.</p></body></html>'
            self.wfile.write(html)
            print(f"✓ Authorization code received!\n")
        else:
            self.send_response(400)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logs

import socketserver
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(('', 8888), Handler) as httpd:
    print(f"Waiting on http://localhost:8888/callback...\n")
    
    while auth_code is None:
        httpd.handle_request()

print(f"Got auth code: {auth_code[:20]}...\n")

# Exchange for token
import urllib.request
token_data = urllib.parse.urlencode({
    'code': auth_code,
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri,
    'grant_type': 'authorization_code'
}).encode()

print(f"Exchanging code for access token...")

token_req = urllib.request.Request(
    'https://oauth2.googleapis.com/token',
    data=token_data,
    method='POST'
)

try:
    with urllib.request.urlopen(token_req) as response:
        token_response = json.loads(response.read())
    
    # Save token
    token_file = Path('/home/wrenn/clawd/gmail_token.json')
    token_file.write_text(json.dumps(token_response, indent=2))
    
    print(f"✓ Success!")
    print(f"✓ Gmail token saved to {token_file}")
    print(f"✓ You can now use Gmail from Mercury!\n")
    
except Exception as e:
    print(f"✗ Error exchanging token: {e}")
