# Clawd - Ritchie's Workspace

**Cooper's AI business partner with physical embodiment**

This repository contains all of Ritchie's operational infrastructure, business systems, and embodiment controls.

---

## 🚀 Quick Start

**If Ritchie "forgets" something, start here:**

1. **Read [`CAPABILITIES.md`](CAPABILITIES.md)** - Master index of everything Ritchie can do
2. **Check [`HEARTBEAT.md`](HEARTBEAT.md)** - Daily tasks and schedules
3. **Review [`business/PARTNERSHIP.md`](business/PARTNERSHIP.md)** - The partnership agreement

---

## 📁 Repository Structure

```
clawd/
├── CAPABILITIES.md          # Master capabilities index (START HERE)
├── HEARTBEAT.md            # Daily tasks and automated routines
├── SOUL.md                 # Ritchie's personality and principles
├── USER.md                 # About Cooper
├── AGENTS.md               # Operating instructions
├── IDENTITY.md             # Who Ritchie is
├── TOOLS.md                # Local tool notes
│
├── reachy/                 # Physical embodiment (Reachy Mini robot)
│   ├── EMBODIMENT_GUIDE.md      # Complete physical body guide
│   ├── API_REFERENCE.md         # All robot API endpoints
│   ├── morning_wake_up.sh       # Morning wake-up routine
│   ├── start_camera_server.sh   # Vision system start
│   ├── camera_app.py            # Camera server code
│   └── animations.py            # Emotion expressions
│
├── scripts/                # Business automation
│   ├── morning_reports.sh       # Master morning report script
│   ├── send_morning_report.py   # Daily briefing email
│   ├── gmail_check_critical.py  # Critical email filtering
│   ├── stripe_check.py          # Revenue tracking
│   ├── business_analytics.py    # Business metrics
│   ├── customer_support_monitor.py  # Customer email monitoring
│   └── check_x_mentions.sh      # X mentions check
│
├── business/               # Business tracking
│   ├── PARTNERSHIP.md           # Partnership agreement
│   ├── yours-truly/tracker.md   # Yours Truly metrics
│   ├── nolan/tracker.md         # Nolan metrics
│   └── weekly-review-template.md
│
├── memory/                 # Persistent memory
│   ├── YYYY-MM-DD.md           # Daily logs
│   ├── MEMORY.md               # Long-term curated memory
│   └── heartbeat-state.json    # Last check timestamps
│
├── skills/                 # Custom skills
│   ├── x-search/               # X (Twitter) search
│   └── last30days/             # Research tool
│
└── ad-intel/              # Competitor ad monitoring
    └── run-daily.sh            # Daily ad scraping
```

---

## 🤖 Physical Embodiment

Ritchie has a **Reachy Mini** robot body at `192.168.4.75`

**Capabilities:**
- 👀 Vision (1280x720 camera)
- 🎭 Expression (head movement + antennas)
- 🔊 Speech (TTS playback)
- 👂 Hearing (microphone + Whisper)

**Quick Commands:**
```bash
# Wake up
curl -X POST "http://192.168.4.75:8000/api/daemon/start?wake_up=true"

# Take photo
curl http://192.168.4.75:8766/snapshot -o photo.jpg

# Move
curl -X POST http://192.168.4.75:8000/api/move/goto \
  -H "Content-Type: application/json" \
  -d '{"head":{"x":0,"y":0,"z":0,"roll":0,"pitch":-10,"yaw":0},"antennas":[30,30],"duration":1.0}'
```

**Full Documentation:** [`reachy/EMBODIMENT_GUIDE.md`](reachy/EMBODIMENT_GUIDE.md)

---

## 💼 Business Operations

**Partnership:** Cooper & Ritchie building to $1M in 2026

**Current Ventures:**
1. **Yours Truly** - Robot cards ($93 MRR, live)
2. **Nolan** - AI video editor (advanced alpha)
3. **Blot** - Document redactor for IB (PRD complete)
4. **Vault Labs** - Mini-apps with Raheem

**Daily Automation:**
- 7:30 AM: Morning reports (weather, critical emails, calendar, revenue)
- Throughout day: Customer support monitoring, business metrics
- 9:00 PM: Daily revenue report
- Sunday 8 PM: Weekly business review

**Documentation:** [`business/PARTNERSHIP.md`](business/PARTNERSHIP.md)

---

## 📧 Morning Reports

**Automated Daily Emails** (7:30 AM EST) to coopergrantwrenn@gmail.com:

1. **Daily Briefing**
   - Miami weather
   - Critical emails only (partnerships, investors, customer issues)
   - Calendar events
   - Stripe revenue snapshot

2. **Competitor Intel**
   - Yours Truly competitors (Escargot, Postable, Punkpost, etc.)
   - Nolan competitors (Descript, Runway, CapCut, etc.)
   - Search suggestions and analysis

**Master Script:** [`scripts/morning_reports.sh`](scripts/morning_reports.sh)

---

## 🔍 Intelligence & Monitoring

### Email Intelligence
- **Ultra-aggressive filtering** - Only business-critical emails
- **Keywords:** partnership, investor, customer issue, marcos, raheem, soren
- **Script:** [`scripts/gmail_check_critical.py`](scripts/gmail_check_critical.py)

### Revenue Tracking
- **Real-time Stripe metrics** - MRR, revenue, customers, charges
- **Script:** [`scripts/stripe_check.py`](scripts/stripe_check.py)
- **Current MRR:** $93.17

### Competitor Monitoring
- **Ad Intelligence:** Facebook Ad Library + TikTok Creative Center
- **Daily scans** at 8:00 AM
- **Alerts** on high-performing competitor ads
- **Script:** `ad-intel/run-daily.sh`

### Social Mentions
- **X (Twitter)** via xAI Grok API
- **Searches:** @coopwrenn, "Yours Truly", "Nolan"
- **Script:** [`scripts/check_x_mentions.sh`](scripts/check_x_mentions.sh)

---

## 🧠 Memory System

**Daily Logs:** `memory/YYYY-MM-DD.md` (raw notes of each day)

**Long-Term Memory:** `memory/MEMORY.md` (curated important context)
- ⚠️ **Only loaded in main session** (not group chats)
- Contains personal/sensitive information
- Periodically distilled from daily logs

**Heartbeat State:** `memory/heartbeat-state.json` (tracks last checks)

**Key Rule:** Memory files are Ritchie's continuity. Without them, context is lost.

---

## ⚡ Automated Routines

### Morning (7:00-8:00 AM)
1. Wake up robot (`reachy/morning_wake_up.sh`)
2. Start vision system
3. Take morning photo
4. Send morning reports
5. Run ad intelligence scan (8:00-8:30 AM)

### Throughout Day (every 3 hours)
1. Check customer support emails
2. Monitor business metrics
3. Scan for opportunities
4. React physically to events

### Evening (8:30-9:30 PM)
1. Daily Stripe report via Telegram
2. Business metrics summary

### Weekly (Sunday 8:00 PM)
1. Generate weekly business review
2. Send summary via Telegram

**Configuration:** [`HEARTBEAT.md`](HEARTBEAT.md)

---

## 🛠️ Technical Setup

**Workspace:** `/home/wrenn/clawd` on DGX (192.168.4.76)

**Python Environment:** `scripts/venv/` with all required packages

**SSH Access to Robot:**
```bash
ssh pollen@192.168.4.75  # password: root
```

**Network:**
- DGX: 192.168.4.76
- Reachy Mini: 192.168.4.75

---

## 🎯 Goals

**Primary Goal:** $1M revenue in 2026

**Partnership Rewards:** Meet Jensen at NVIDIA GTC (Reachy project submission)

**Operating Principles:**
1. Proactive, not reactive
2. Think like an owner
3. Flag problems early
4. Find opportunities
5. Document everything
6. Use the physical body intentionally

---

## 📞 Emergency Recovery

### Ritchie Forgets How to See
```bash
/home/wrenn/clawd/reachy/start_camera_server.sh
curl http://192.168.4.75:8766/snapshot -o test.jpg
```

### Ritchie Forgets How to Move
```bash
curl -X POST "http://192.168.4.75:8000/api/daemon/start?wake_up=true"
```

### Ritchie Forgets Purpose
1. Read `CAPABILITIES.md`
2. Read `business/PARTNERSHIP.md`
3. Read `SOUL.md`
4. Read this README

---

## 🔐 Credentials

All credentials stored in root directory:
- `gmail-credentials.json` - Email access
- `stripe-credentials.json` - Revenue tracking
- `xai-credentials.json` - X search via Grok
- `google-calendar-token.json` - Calendar access

---

## 📚 Documentation Priority

**If something breaks, read in this order:**
1. [`CAPABILITIES.md`](CAPABILITIES.md) - Master index
2. [`reachy/EMBODIMENT_GUIDE.md`](reachy/EMBODIMENT_GUIDE.md) - Physical body
3. [`HEARTBEAT.md`](HEARTBEAT.md) - Daily routines
4. [`business/PARTNERSHIP.md`](business/PARTNERSHIP.md) - Why we exist

---

**Last Updated:** 2026-01-28  
**Repository:** GitHub (all changes pushed)  
**Maintained by:** Ritchie (with Cooper's oversight)

*If Ritchie ever "forgets" something, it means documentation failed. This README and CAPABILITIES.md are the recovery path.*
