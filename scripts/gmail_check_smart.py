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
    'luma-mail.com',
    'buildinglink.com',  # Building notifications
    'opentable.com',  # Restaurant reservations
    'yutori.com',  # Restaurant newsletter
    'shopify.com',  # Unless it's from customer support
    'ideabrowser.com',  # Newsletter
    'dice.fm',  # Events
    'buckmason.com',  # Shopping
    'menscrafted.com',  # Shopping
    'hardrockbet.com',  # Gambling
    'deltaairlines.com',  # Travel marketing
    'delta.com',  # Travel marketing
    'morphic.com',  # Unless directly relevant
    'se.ro',  # Newsletter
    'opusclip.com',  # Unless from their team directly
    'email.shopify.com'  # Shopify marketing
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
    
    # If it's from a personal email (gmail/yahoo/etc), more likely to be important
    if any(common in from_lower for common in ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'me.com', 'icloud.com']):
        return True
    
    # Otherwise skip - most company emails are marketing
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
