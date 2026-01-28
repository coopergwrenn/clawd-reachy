#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Send morning report with GLM-4 intelligence (FREE local model)
"""
import json
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import sys
sys.path.insert(0, '/home/wrenn/clawd/scripts')

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

def call_glm(prompt):
    """Use local GLM-4 model"""
    try:
        result = subprocess.run(
            ['python3', '/home/wrenn/clawd/scripts/llm_local.py', 'glm', prompt],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        return f"GLM error: {str(e)}"

def generate_smart_report():
    """Generate report using GLM for intelligence"""
    
    # Gather raw data
    weather = get_weather()
    emails = run_check('gmail_check_critical.py')
    calendar = run_check('calendar_check_oauth.py')
    stripe = run_check('stripe_check.py')
    
    # Build context for GLM
    context = f"""Today's Business Data for Cooper (Yours Truly, Nolan, Blot):

Weather: {weather}

Critical Emails: {len(emails) if isinstance(emails, list) else 0}
Email details: {json.dumps(emails[:3]) if isinstance(emails, list) else 'None'}

Calendar: {len(calendar) if isinstance(calendar, list) else 0} events
Events: {json.dumps(calendar) if isinstance(calendar, list) else 'None'}

Revenue (last 24h): ${stripe.get('total_revenue', 0):.2f}
Available balance: ${stripe.get('available_balance', 0):.2f}
New customers: {stripe.get('new_customers', 0)}

Generate a concise, actionable morning briefing email. Include:
1. Weather context
2. Critical email summary (only if urgent)
3. Calendar highlights
4. Revenue insight
5. One clear priority for today

Keep it under 200 words. Be direct and businesslike."""

    # Get intelligent summary from GLM
    smart_summary = call_glm(context)
    
    # Format email
    body = f"""Good morning Cooper! 🌅

{smart_summary}

--
Ritchie 🤖
(Generated with local GLM-4 - $0 cost)"""
    
    return body

def send_email(to_email, subject, body):
    """Send email via Gmail SMTP"""
    try:
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
    subject = f"Daily Briefing (GLM-4 Local) - {datetime.now().strftime('%A, %B %d, %Y')}"
    
    print("📊 Generating smart morning report with local GLM-4...")
    body = generate_smart_report()
    
    print("\nEmail body:")
    print(body)
    print("\n✉️ Sending email...")
    
    success = send_email('coopergrantwrenn@gmail.com', subject, body)
    
    if success:
        print("✅ Email sent successfully! (Cost: $0 - local model)")
    else:
        print("❌ Failed to send email")
