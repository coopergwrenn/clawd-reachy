#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Check Gmail for ONLY business-critical emails
Ultra-aggressive filtering - only show what matters for $1M goal
"""
import imaplib
import email
from email.header import decode_header
import json
import re

# ONLY show emails with these exact keywords (case insensitive)
CRITICAL_KEYWORDS = [
    'partnership',
    'investor',
    'funding',
    'investment',
    'acquisition',
    'contract',
    'customer support',
    'customer issue',
    'refund request',
    'marcos',  # Your developer
    'raheem',  # Business partner
    'soren',  # Brother/mentor
    'museum of ice cream',  # Partnership
    'edge city',  # Partnership
    'yours truly',  # Your company (from customers/partners)
    'nolan',  # Your product (from users/partners)
    'blot',  # Your product
    'vault labs',  # Your company
    'revenue',
    'payment failed',
    'subscription cancelled'
]

# Known business contacts (add as you identify them)
BUSINESS_CONTACTS = [
    'marcos',
    'raheem',
    'soren',
    'cooperwrenn'  # Your own domain if you have one
]

def is_critical_email(from_addr, subject):
    """Only return True for genuinely business-critical emails"""
    from_lower = from_addr.lower()
    subject_lower = subject.lower()
    
    # Check if from known business contact
    for contact in BUSINESS_CONTACTS:
        if contact in from_lower:
            return True
    
    # Check for critical keywords
    for keyword in CRITICAL_KEYWORDS:
        if keyword in subject_lower:
            return True
    
    # Stripe notifications about actual issues (NOT marketing)
    if 'stripe' in from_lower:
        # Only show if it's a problem, not marketing
        if any(word in subject_lower for word in ['failed', 'cancelled', 'dispute', 'chargeback', 'action required', 'suspended']):
            return True
        # Skip Stripe marketing
        if any(word in subject_lower for word in ['get more', 'new feature', 'webinar', 'update:', 'announcing']):
            return False
    
    return False

def load_credentials():
    import json
    with open('/home/wrenn/clawd/gmail-credentials.json', 'r') as f:
        creds = json.load(f)
    return creds['email'], creds['app_password']

def get_critical_emails(hours=24):
    try:
        email_addr, password = load_credentials()
        
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_addr, password)
        mail.select('inbox')
        
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()
        
        critical_emails = []
        for email_id in email_ids[-100:]:  # Check last 100 unread
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    subject = decode_header(msg['Subject'])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    
                    from_header = msg.get('From', 'Unknown')
                    
                    if is_critical_email(from_header, subject):
                        critical_emails.append({
                            'from': from_header,
                            'subject': subject,
                            'date': msg.get('Date', '')
                        })
        
        mail.close()
        mail.logout()
        
        return critical_emails
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    emails = get_critical_emails()
    print(json.dumps(emails, indent=2))
