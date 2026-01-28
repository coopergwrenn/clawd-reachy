#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Check Gmail for IMPORTANT emails only - filter out noise
"""
import imaplib
import email
from email.header import decode_header
import json
from datetime import datetime, timedelta

# Domains/senders to SKIP (noise)
SKIP_SENDERS = [
    'uber.com',
    'venmo.com',
    'chime.com',
    'godaddy.com',
    'alibaba.com',
    'chrono24.com',
    'hiltongrandvacations.com',
    'touchofmodern.com',
    'redfin.com',
    'aloyoga.com',
    'jamesperse.com',
    'fandango.com',
    'coinbase.com',
    'nytimes.com',
    'bloomberg.com',
    'polymarket.com',
    'tiktok.com',
    'producthunt.com',
    'gemini.com',
    'webull.com',
    'salliemae.com',
    'substack.com',
    'mobbin.com',
    'bayareatimes.com',
    'skool.com',
    'luma-mail.com'
]

# Keywords that indicate IMPORTANT business emails
IMPORTANT_KEYWORDS = [
    'yours truly',
    'nolan',
    'blot',
    'vault labs',
    'partnership',
    'investor',
    'funding',
    'meeting',
    'contract',
    'proposal',
    'opportunity',
    'customer',
    'payment',
    'stripe',
    'revenue',
    'marcos',
    'raheem',
    'soren',
    'museum of ice cream',
    'edge city'
]

def is_important_email(from_addr, subject):
    """Determine if an email is important"""
    from_lower = from_addr.lower()
    subject_lower = subject.lower()
    
    # Skip obvious noise
    for skip in SKIP_SENDERS:
        if skip in from_lower:
            return False
    
    # Check for important keywords
    for keyword in IMPORTANT_KEYWORDS:
        if keyword in subject_lower or keyword in from_lower:
            return True
    
    # If sender is from a company domain (not gmail/yahoo/etc), might be important
    if not any(common in from_lower for common in ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']):
        # Could be a business contact
        return True
    
    return False

def load_credentials():
    import json
    with open('/home/wrenn/clawd/gmail-credentials.json', 'r') as f:
        creds = json.load(f)
    return creds['email'], creds['app_password']

def get_important_emails(hours=24):
    try:
        email_addr, password = load_credentials()
        
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_addr, password)
        mail.select('inbox')
        
        # Search for unread emails
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()
        
        important_emails = []
        # Get last 50 unread emails and filter
        for email_id in email_ids[-50:]:
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    subject = decode_header(msg['Subject'])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    
                    from_header = msg.get('From', 'Unknown')
                    date_header = msg.get('Date', '')
                    
                    # Only include if important
                    if is_important_email(from_header, subject):
                        important_emails.append({
                            'from': from_header,
                            'subject': subject,
                            'date': date_header
                        })
        
        mail.close()
        mail.logout()
        
        return important_emails
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    emails = get_important_emails()
    print(json.dumps(emails, indent=2))
