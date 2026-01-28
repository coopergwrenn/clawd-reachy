# HEARTBEAT.md

## Morning Email Reports (7:30am EST)
If it's between 7:00am-8:00am EST and you haven't done a morning report today:

**Send to: coopergrantwrenn@gmail.com**

### Email 1: Daily Briefing
- Weather in Miami (quick: temp, conditions)
- Gmail inbox: Urgent/important emails from last 24h
- Calendar: What's on today
- Today's priorities: Based on calendar + context, suggest focus areas
- Social mentions: Check if anyone tagged @coopwrenn or Yours Truly
- Revenue snapshot: Quick Stripe balance + recent activity

### Email 2: Competitor Intel
**Yours Truly competitors** (Escargot, Postable, Punkpost, Handwrytten, Simply Noted):
- New social posts (TikTok, IG, X)
- New ads (Meta Ad Library, TikTok)
- UGC partnerships spotted
- What's getting engagement
- Quick bullets + links

**Nolan competitors** (Descript, Runway, CapCut, Opus Clip):
- Same format
- Focus on product updates, content trends

**Actionable insight:** "Consider posting X based on what's working"

## Ad Intelligence Scan (8:00am EST)
If it's between 8:00am-8:30am EST and you haven't run ad intel today:
- Run `/home/wrenn/clawd/ad-intel/run-daily.sh`
- This scrapes Facebook Ad Library + TikTok Creative Center
- Identifies high-performing competitor ads
- Sends Telegram alert if winners found (score ≥5)
- Data stored in `ad-intel/data/` for later analysis

**What it tracks:**
- Yours Truly competitors: Escargot, Postable, Punkpost, Handwrytten, Simply Noted
- TikTok trending ads for: cards, postcards, gifts, personalized, custom

**When to alert:**
- New ads running 30+ days (proven winners)
- High engagement on TikTok (1000+ likes, 100+ comments)
- Fresh creative angles or messaging

## Daily Stripe Report (9pm EST)
If it's between 8:30pm-9:30pm EST and you haven't done a daily report today:
- Check Stripe for new customers today
- Check revenue/charges today
- Check PostHog for DAU, pageviews, key events
- Send combined revenue + analytics summary via Telegram

## Weekly Stripe Report (Sunday 8pm EST)
If it's Sunday and between 7:30pm-8:30pm EST and you haven't done a weekly report:
- Total new customers this week
- Total revenue this week
- Week-over-week comparison
- PostHog: WAU, retention, traffic trends
- Send combined summary via Telegram

## Reachy Demo Photo Trigger
Check `/home/wrenn/clawd/reachy/send_photo_now.txt` - if it exists:
1. Take fresh snapshot from Reachy camera  
2. Send to Telegram
3. Delete the trigger file

## Periodic Checks (rotate through these)
- Check Gmail for urgent customer emails
- Monitor for partnership responses (Museum of Ice Cream, Edge City)
