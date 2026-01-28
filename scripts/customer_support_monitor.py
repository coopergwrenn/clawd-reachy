#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Monitor customer emails and draft responses
"""
import imaplib
import email
from email.header import decode_header
import json
from datetime import datetime

# Customer support keywords
SUPPORT_KEYWORDS = [
    'issue',
    'problem',
    'help',
    'wrong',
    'mistake',
    'cancel',
    'refund',
    'didn\'t receive',
    'not delivered',
    'quality',
    'complaint',
    'disappointed',
    'question about'
]

def load_credentials():
    with open('/home/wrenn/.secrets/gmail.json', 'r') as f:
        creds = json.load(f)
    return creds['email'], creds['app_password']

def is_customer_support_email(from_addr, subject, body_preview=''):
    """Check if email is a customer support request"""
    from_lower = from_addr.lower()
    subject_lower = subject.lower()
    body_lower = body_preview.lower()
    
    # Skip if from known marketing/system addresses
    skip_domains = ['noreply', 'no-reply', 'donotreply', 'notifications@']
    if any(domain in from_lower for domain in skip_domains):
        return False
    
    # Check for support keywords
    combined_text = f"{subject_lower} {body_lower}"
    for keyword in SUPPORT_KEYWORDS:
        if keyword in combined_text:
            return True
    
    # Personal emails (gmail/yahoo/etc) to business address likely need response
    if any(domain in from_lower for domain in ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com']):
        # If it's not automated, probably a customer
        return True
    
    return False

def get_customer_emails():
    """Get unread emails that look like customer support requests"""
    try:
        email_addr, password = load_credentials()
        
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_addr, password)
        mail.select('inbox')
        
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()
        
        customer_emails = []
        for email_id in email_ids[-50:]:
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    subject = decode_header(msg['Subject'])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    
                    from_header = msg.get('From', 'Unknown')
                    
                    # Get body preview
                    body_preview = ''
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                body_preview = str(part.get_payload(decode=True))[:500]
                                break
                    else:
                        body_preview = str(msg.get_payload(decode=True))[:500]
                    
                    if is_customer_support_email(from_header, subject, body_preview):
                        customer_emails.append({
                            'from': from_header,
                            'subject': subject,
                            'date': msg.get('Date', ''),
                            'body_preview': body_preview[:200]
                        })
        
        mail.close()
        mail.logout()
        
        return customer_emails
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    emails = get_customer_emails()
    print(json.dumps(emails, indent=2))
