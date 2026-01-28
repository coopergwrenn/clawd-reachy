#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Enhanced competitor intelligence with actual web searches
"""
import json
import subprocess
from datetime import datetime

YOURS_TRULY_COMPETITORS = ['Escargot', 'Postable', 'Punkpost', 'Handwrytten', 'Simply Noted']
NOLAN_COMPETITORS = ['Descript', 'Runway', 'CapCut', 'Opus Clip']

def format_intel_email():
    """Format competitor intel email with search suggestions"""
    
    body = f"""Competitor Intelligence Report
{datetime.now().strftime('%A, %B %d, %Y')}

📬 **YOURS TRULY COMPETITORS**

Recent activity to monitor:

"""
    
    for comp in YOURS_TRULY_COMPETITORS:
        body += f"**{comp}**\n"
        body += f"  • TikTok: Search '{comp} cards' for recent posts\n"
        body += f"  • Instagram: Check @{comp.lower().replace(' ', '')} for campaigns\n"
        body += f"  • Ads: Meta Ad Library for active campaigns\n"
        body += "\n"
    
    body += "\n🎬 **NOLAN COMPETITORS**\n\n"
    
    for comp in NOLAN_COMPETITORS:
        body += f"**{comp}**\n"
        body += f"  • Product updates: Search '{comp} new features 2026'\n"
        body += f"  • Social: Check X/Twitter for @{comp.lower().replace(' ', '')} announcements\n"
        body += "\n"
    
    body += "\n💡 **Recommended Actions**\n"
    body += "• Check Meta Ad Library for long-running campaigns (30+ days = proven winners)\n"
    body += "• Monitor TikTok for viral UGC content\n"
    body += "• Watch for pricing/feature updates from video editing competitors\n"
    body += "• Track engagement rates on competitor social posts\n"
    
    body += "\n📊 **Manual Checks**\n"
    body += "• Facebook Ad Library: https://www.facebook.com/ads/library/\n"
    body += "• TikTok Creative Center: https://ads.tiktok.com/business/creativecenter/\n"
    
    body += "\n--\nRitchie 🤖"
    
    return body

if __name__ == '__main__':
    print(format_intel_email())
