#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Check Gmail for urgent/important emails using IMAP
"""
import imaplib
import email
from email.header import decode_header
import json
from datetime import datetime, timedelta

def load_credentials():
    import json
    with open('/home/wrenn/clawd/gmail-credentials.json', 'r') as f:
        creds = json.load(f)
    return creds['email'], creds['app_password']

def get_recent_emails(hours=24):
    try:
        email_addr, password = load_credentials()
        
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_addr, password)
        mail.select('inbox')
        
        # Search for unread emails
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()
        
        emails = []
        # Get last 20 unread emails
        for email_id in email_ids[-20:]:
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    subject = decode_header(msg['Subject'])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    
                    from_header = msg.get('From', 'Unknown')
                    date_header = msg.get('Date', '')
                    
                    emails.append({
                        'from': from_header,
                        'subject': subject,
                        'date': date_header
                    })
        
        mail.close()
        mail.logout()
        
        return emails
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    emails = get_recent_emails()
    print(json.dumps(emails, indent=2))
