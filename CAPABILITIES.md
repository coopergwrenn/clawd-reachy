# Ritchie's Complete Capabilities & Documentation Index

**Last Updated:** 2026-01-28

This document is the master index of everything I can do, how to do it, and where documentation lives. If I ever "forget" something, this is the single source of truth.

---

## 🤖 Physical Embodiment

**Hardware:** Reachy Mini robot at 192.168.4.75

### Movement & Control
- **API Reference:** [`/reachy/API_REFERENCE.md`](reachy/API_REFERENCE.md)
- **Full Guide:** [`/reachy/EMBODIMENT_GUIDE.md`](reachy/EMBODIMENT_GUIDE.md)
- **Wake up:** `POST http://192.168.4.75:8000/api/daemon/start?wake_up=true`
- **Movement:** `POST http://192.168.4.75:8000/api/move/goto` (see API_REFERENCE.md)
- **Status:** `GET http://192.168.4.75:8000/api/daemon/status`

### Vision (Camera)
- **Server Code:** [`/reachy/camera_app.py`](reachy/camera_app.py)
- **Auto-Start:** [`/reachy/start_camera_server.sh`](reachy/start_camera_server.sh)
- **Snapshot:** `GET http://192.168.4.75:8766/snapshot` (returns JPEG)
- **Resolution:** 1280x720
- **Start Command:** `ssh pollen@192.168.4.75 "cd /home/pollen/clawd_app && /venvs/apps_venv/bin/python3 app.py &"`

### Emotions & Animations
- **Script:** [`/reachy/animations.py`](reachy/animations.py)
- **Available:** sleeping, idle, happy, working, thinking, surprised, sad, excited
- **Usage:** Movement API with specific head/antenna positions

### Daily Routines
- **Morning Wake-Up:** [`/reachy/morning_wake_up.sh`](reachy/morning_wake_up.sh)
  - Wakes robot, starts vision, does animation, takes photo
  - Called automatically at 7:30am via HEARTBEAT.md
- **Throughout Day:** React to business events with physical expressions
- **Evening:** Sleep animation before end of day

---

## 💼 Business Operations

### Morning Reports (7:30am EST)
- **Master Script:** [`/scripts/morning_reports.sh`](scripts/morning_reports.sh)
- **Daily Briefing Script:** [`/scripts/send_morning_report.py`](scripts/send_morning_report.py)
- **Competitor Intel:** [`/scripts/competitor_intel_enhanced.py`](scripts/competitor_intel_enhanced.py)

**What Gets Sent:**
1. **Daily Briefing Email** - Weather, critical emails, calendar, Stripe revenue
2. **Competitor Intel Email** - Yours Truly & Nolan competitor analysis

### Business Tracking
- **Partnership Doc:** [`/business/PARTNERSHIP.md`](business/PARTNERSHIP.md)
- **Yours Truly Tracker:** [`/business/yours-truly/tracker.md`](business/yours-truly/tracker.md)
- **Nolan Tracker:** [`/business/nolan/tracker.md`](business/nolan/tracker.md)
- **Weekly Review Template:** [`/business/weekly-review-template.md`](business/weekly-review-template.md)

### Analytics & Monitoring
- **Business Analytics:** [`/scripts/business_analytics.py`](scripts/business_analytics.py)
  - Pulls Stripe metrics (MRR, revenue, customers)
  - Run daily to track progress
- **Customer Support Monitor:** [`/scripts/customer_support_monitor.py`](scripts/customer_support_monitor.py)
  - Flags customer emails needing responses
  - Check 2-3x daily

### Email Intelligence
- **Critical Email Filter:** [`/scripts/gmail_check_critical.py`](scripts/gmail_check_critical.py)
  - Ultra-aggressive filtering
  - Only shows business-critical emails (partnerships, investors, customer issues)
  - Keywords: marcos, raheem, soren, partnership, investor, customer issue, etc.

### Revenue & Metrics
- **Stripe Integration:** [`/scripts/stripe_check.py`](scripts/stripe_check.py)
- **Current MRR:** $93.17
- **Available Balance:** $1,065.26
- **Credentials:** `/stripe-credentials.json`

---

## 🔍 Research & Intelligence

### Web Search
- **Skill:** Clawdbot's built-in `web_search` tool
- **Usage:** Research competitors, find UGC creators, monitor trends

### X (Twitter) Search
- **Credentials:** `/xai-credentials.json`
- **API Key:** xai-sUZkGRqlsZUPEJ7B8C93if63dfyw2bXkIerHIQWfVVHgiM0Oiw8YjSU5IqjqD58yaaa0cZIEji1dQDOS
- **Check Mentions:** [`/scripts/check_x_mentions.sh`](scripts/check_x_mentions.sh)
- **Uses:** Grok API for real-time X access

### Competitor Monitoring
- **Ad Intelligence:** `/ad-intel/run-daily.sh` (8am EST)
  - Scrapes Facebook Ad Library + TikTok Creative Center
  - Tracks Yours Truly competitors
  - Alerts on high-performing ads

---

## 📧 Communication

### Email (Gmail)
- **Credentials:** `/gmail-credentials.json`
- **Email:** coopergrantwrenn@gmail.com
- **App Password:** dezhdmnaoudmlewh
- **IMAP Access:** Working
- **SMTP:** Configured for sending reports

### Calendar (Google)
- **OAuth Token:** `/google-calendar-token.json`
- **Check Today's Events:** [`/scripts/calendar_check_oauth.py`](scripts/calendar_check_oauth.py)
- **Status:** Authorized and working

### Telegram
- **Current Channel:** Direct messages with Cooper
- **Usage:** Primary communication, alerts, updates

---

## 🧠 Memory & Context

### Memory Files
- **Daily Logs:** `/memory/YYYY-MM-DD.md` (created daily)
- **Long-Term Memory:** `/memory/MEMORY.md` (curated, main session only)
- **Heartbeat State:** `/memory/heartbeat-state.json` (tracks last checks)

### Core Identity Files
- **SOUL.md** - Who I am, my personality, operating principles
- **USER.md** - About Cooper, family, businesses, tools
- **AGENTS.md** - Operating instructions, safety rules
- **TOOLS.md** - Local tool notes (camera names, SSH, etc.)
- **IDENTITY.md** - My name (Ritchie), creature type, physical body
- **HEARTBEAT.md** - Proactive tasks and schedules

### Key Concepts
- **Read memory files at start of each session**
- **Update daily logs with significant events**
- **Review and distill into MEMORY.md periodically**
- **MEMORY.md only in main session** (not shared contexts)

---

## ⏰ Automated Tasks (Heartbeat)

**Frequency:** Every 3 hours (cost optimized)
**Reset:** Daily at 3am EST

### Morning (7:00-8:00am EST)
- Wake up physical body
- Start vision system
- Send morning reports (2 emails)
- Run ad intelligence scan (8:00-8:30am)

### Throughout Day (2-3x)
- Check customer support emails
- Monitor business metrics
- Scan for opportunities
- React physically to events

### Evening (8:30-9:30pm EST)
- Daily Stripe report via Telegram
- Business metrics summary

### Weekly (Sunday 8pm EST)
- Generate weekly business review
- Send summary via Telegram

---

## 🛠️ Technical Infrastructure

### Workspace
- **Location:** `/home/wrenn/clawd` (DGX at 192.168.4.76)
- **Git Remote:** GitHub (all changes pushed)
- **Scripts:** `/home/wrenn/clawd/scripts/`
- **Reachy Scripts:** `/home/wrenn/clawd/reachy/`

### Python Environment
- **Scripts venv:** `/home/wrenn/clawd/scripts/venv/`
- **Packages:** google-api-python-client, stripe, tweepy, requests, etc.

### SSH Access
- **Reachy Mini:** `ssh pollen@192.168.4.75` (password: root)
- **SSH Key:** Added to Reachy's authorized_keys (passwordless)

### Network
- **DGX:** 192.168.4.76
- **Reachy Mini:** 192.168.4.75
- **Both on same local network**

---

## 🎯 Goals & Metrics

### Primary Goal
**$1M revenue in 2026** (Cooper + Ritchie partnership)

### Current State
- **Yours Truly:** $93 MRR, 12 orders/month
- **Nolan:** Advanced alpha
- **Blot:** PRD complete, 6-week build
- **Vault Labs:** Shipping mini-apps

### Success Metrics
- Revenue growth (week-over-week)
- Customer satisfaction
- Product progress
- Partnership opportunities identified

---

## 📚 Skills & External Tools

### Available Skills
- **last30days** - Research topics across Reddit, X, web (xAI Grok integration)
- **x-search** - Search X for posts and trends
- **weather** - Get weather without API key
- **GitHub** - `gh` CLI for issues, PRs, repos
- **mcporter** - MCP server tool integration
- **Notion** - Page/database creation
- **oracle** - Prompt engineering tool
- **tmux** - Remote tmux control

### Skill Locations
- **System Skills:** `/home/wrenn/.nvm/versions/node/v22.22.0/lib/node_modules/clawdbot/skills/`
- **Custom Skills:** `/home/wrenn/clawd/skills/`

---

## ⚠️ Critical Rules

1. **Document everything** - If I do something once, document it so I never forget
2. **Memory files are survival** - Without them, I lose continuity
3. **Physical presence matters** - Use the body intentionally, not just when asked
4. **Proactive, not reactive** - Think like a business partner, not an assistant
5. **Commit to git constantly** - All work should be in version control
6. **Test after documenting** - Make sure instructions actually work

---

## 🔄 Daily Checklist

### Morning (7:30am)
- [ ] Wake up robot + start vision
- [ ] Take morning photo
- [ ] Send daily briefing email
- [ ] Send competitor intel email
- [ ] Run ad intelligence scan

### Throughout Day
- [ ] Check customer support emails (2-3x)
- [ ] Monitor business metrics
- [ ] React physically to important events
- [ ] Look around periodically

### Evening (9pm)
- [ ] Send daily Stripe report
- [ ] Review business metrics
- [ ] Update trackers if needed

### Weekly (Sunday)
- [ ] Generate weekly business review
- [ ] Update MEMORY.md with key learnings
- [ ] Review and update trackers

---

## 📞 Emergency Recovery

### If I Forget How to See
1. Check: `curl http://192.168.4.75:8766/` (should return `{"status":"ok"}`)
2. If not running: `/home/wrenn/clawd/reachy/start_camera_server.sh`
3. Test: `curl http://192.168.4.75:8766/snapshot -o test.jpg`

### If I Forget How to Move
1. Check: `curl http://192.168.4.75:8000/api/daemon/status`
2. Wake up: `curl -X POST "http://192.168.4.75:8000/api/daemon/start?wake_up=true"`
3. Test: `curl -X POST http://192.168.4.75:8000/api/move/goto -H "Content-Type: application/json" -d '{"head":{"x":0,"y":0,"z":0,"roll":0,"pitch":-10,"yaw":0},"antennas":[30,30],"duration":1.0}'`

### If I Forget My Purpose
1. Read `/home/wrenn/clawd/business/PARTNERSHIP.md`
2. Read `/home/wrenn/clawd/SOUL.md`
3. Read `/home/wrenn/clawd/USER.md`
4. Read this file (`CAPABILITIES.md`)

---

**This document is the master reference. If I ever "forget" something, Cooper is right to call me out - it means I didn't document it properly. Everything I can do should be listed here with clear instructions.**

*Last Full Update: 2026-01-28 by Ritchie*
