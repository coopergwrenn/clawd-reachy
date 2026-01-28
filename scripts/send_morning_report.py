#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Generate and send morning briefing email
"""
import json
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def run_check(script):
    """Run a check script and return JSON output"""
    try:
        result = subprocess.run(
            [f'/home/wrenn/clawd/scripts/{script}'],
            capture_output=True,
            text=True,
            timeout=30
        )
        return json.loads(result.stdout) if result.stdout else None
    except Exception as e:
        return {'error': str(e)}

def get_weather():
    """Get Miami weather"""
    try:
        result = subprocess.run(
            ['curl', '-s', 'wttr.in/Miami?format=%l:+%c+%t+%h+%w'],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except:
        return "Weather unavailable"

def format_email_body():
    """Generate the email body"""
    weather = get_weather()
    emails = run_check('gmail_check_imap.py')
    calendar = run_check('calendar_check_oauth.py')
    stripe = run_check('stripe_check.py')
    x_mentions = run_check('x_search_grok.py')
    
    body = f"""Good morning Cooper! 🌅

📍 **Miami Weather**
{weather}

📧 **Inbox Update**
"""
    
    if isinstance(emails, list) and len(emails) > 0:
        body += f"You have {len(emails)} unread emails from the last 24 hours:\n\n"
        for email in emails[:5]:
            body += f"  • From: {email['from']}\n"
            body += f"    Subject: {email['subject']}\n\n"
        if len(emails) > 5:
            body += f"  ...and {len(emails) - 5} more\n\n"
    else:
        body += "Inbox is clear! ✅\n\n"
    
    body += "📅 **Today's Calendar**\n"
    if isinstance(calendar, dict):
        if calendar.get('note'):
            body += f"{calendar['note']}\n\n"
        elif calendar.get('events') and len(calendar['events']) > 0:
            for event in calendar['events']:
                body += f"  • {event['start']}: {event['summary']}\n"
                if event.get('location'):
                    body += f"    Location: {event['location']}\n"
            body += "\n"
        else:
            body += "No events scheduled today\n\n"
    else:
        body += "Calendar check unavailable\n\n"
    
    body += "💰 **Revenue Snapshot (Last 24h)**\n"
    if isinstance(stripe, dict) and 'error' not in stripe:
        body += f"  • Revenue: ${stripe.get('total_revenue', 0):.2f}\n"
        body += f"  • Charges: {stripe.get('total_charges', 0)}\n"
        body += f"  • New customers: {stripe.get('new_customers', 0)}\n"
        body += f"  • Available balance: ${stripe.get('available_balance', 0):.2f}\n\n"
        
        if stripe.get('recent_charges'):
            body += "Recent charges:\n"
            for charge in stripe['recent_charges'][:3]:
                body += f"  • ${charge['amount']:.2f} - {charge.get('customer_email', 'Unknown')} - {charge['created']}\n"
    else:
        body += "Unable to fetch Stripe data\n"
    
    body += "\n🐦 **Social Mentions**\n"
    if isinstance(x_mentions, dict) and x_mentions.get('mentions'):
        mentions_count = len(x_mentions['mentions'])
        body += f"Found {mentions_count} recent mentions:\n"
        for mention in x_mentions['mentions'][:5]:
            body += f"  • @{mention.get('author', 'Unknown')}: {mention.get('text', '')[:80]}...\n"
    else:
        body += "No new mentions detected\n"
    
    body += "\n🐦 **Social Mentions (X)**\n"
    if isinstance(x_mentions, dict):
        if x_mentions.get('error'):
            body += f"Error checking X: {x_mentions['error']}\n"
        elif x_mentions.get('raw_response'):
            body += x_mentions['raw_response'][:500] + "\n"
        else:
            body += "No significant mentions found\n"
    body += "\n"
    
    body += "\n🎯 **Today's Focus**\n"
    
    if isinstance(calendar, dict) and calendar.get('events'):
        events_count = len(calendar['events'])
        if events_count > 0:
            body += f"  • You have {events_count} events today - plan around them\n"
        else:
            body += "  • Clear calendar - good day to focus on deep work\n"
    else:
        body += "  • Check your calendar manually\n"
    
    body += "\n--\nRitchie 🤖"
    
    return body

def send_email(to_email, subject, body):
    """Send email via Gmail SMTP"""
    try:
        # Load credentials
        with open('/home/wrenn/clawd/gmail-credentials.json', 'r') as f:
            creds = json.load(f)
            email = creds['email']
            password = creds['app_password']
        
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == '__main__':
    subject = f"Daily Briefing - {datetime.now().strftime('%A, %B %d, %Y')}"
    body = format_email_body()
    
    print("Email body:")
    print(body)
    print("\nSending email...")
    
    success = send_email('coopergrantwrenn@gmail.com', subject, body)
    
    if success:
        print("✅ Email sent successfully!")
    else:
        print("❌ Failed to send email")
