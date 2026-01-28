# System Architecture - Local vs. Remote

**Critical Understanding:** Local models generate text. APIs give real-time data.

---

## 🏗️ Two-Layer System

### Layer 1: Data Collection (ALWAYS APIs - Real-Time)
- ✅ **Gmail API** → Pull actual emails via IMAP
- ✅ **Stripe API** → Real revenue numbers, customers, charges
- ✅ **Google Calendar API** → Actual calendar events
- ✅ **xAI Grok API** → Real-time X (Twitter) search
- ✅ **Web Search (Brave)** → Current web results
- ✅ **Clawdbot tools** → Browser control, web fetch, etc.

**These NEVER use local models.** Always direct API calls for fresh, real data.

### Layer 2: Intelligence & Formatting (Local Models - Free)
- 💰 **GLM-4** → Summarize the data into actionable insights
- 💰 **Nemotron 70B** → Generate conversational responses
- 💰 **Local only** → No internet access, just text generation

**These process the data from Layer 1, but don't fetch new data.**

---

## 📊 Example: Morning Report Flow

```
1. REAL DATA (APIs - always fresh):
   ├─ Gmail API → 3 critical emails found
   ├─ Stripe API → $1.00 revenue today, $1,065 balance
   ├─ Google Calendar → 2 events today
   ├─ xAI Grok → No X mentions found
   └─ Weather API → Miami 17°C, cloudy

2. LOCAL INTELLIGENCE (GLM-4 - free):
   ├─ Take all the real data above
   ├─ Generate actionable summary
   ├─ Suggest priorities based on calendar/revenue
   └─ Format into professional email

3. SEND (Gmail SMTP):
   └─ Deliver intelligent briefing to Cooper
```

**Cost:** APIs are cheap/free, GLM is free → Total: ~$0

---

## 🎯 When to Use What

### ALWAYS Use APIs (Real-Time Data)
- ✅ Checking email
- ✅ Pulling Stripe revenue
- ✅ Calendar events
- ✅ X mentions search
- ✅ Web search
- ✅ Competitor monitoring
- ✅ Customer support emails

### ALWAYS Use Local Models (Text Generation)
- 💰 Summarizing data into insights
- 💰 Drafting email responses
- 💰 Generating business analysis
- 💰 Conversational responses
- 💰 Weekly review narratives

### When to Use Claude API
- 🧠 **Complex reasoning** that local models struggle with
- 🧠 **Multi-step planning** requiring strong logic
- 🧠 **Code generation** (Claude is better than local)
- 🧠 **Critical decisions** where quality matters most

**Rule:** Try local first, escalate to Claude if quality isn't good enough.

---

## 🚨 Critical Rule

**NEVER use local models to:**
- Search the web (they can't access internet)
- Check APIs (they don't have real-time data)
- Make decisions requiring current information
- Access databases or external services

**Local models are TEXT PROCESSORS, not DATA SOURCES.**

---

## 🔄 Hybrid Intelligence

**Best of both worlds:**

```python
# 1. Get REAL data from APIs
emails = fetch_from_gmail_api()        # Real-time
revenue = fetch_from_stripe_api()      # Real-time
mentions = search_x_via_grok_api()     # Real-time

# 2. Use local model to make it intelligent
raw_data = json.dumps({
    'emails': emails,
    'revenue': revenue,
    'mentions': mentions
})

insight = call_glm(f"Analyze this business data and suggest priorities: {raw_data}")

# 3. Send actionable intelligence
send_to_cooper(insight)
```

**Result:** Fresh data + intelligent analysis, minimal cost.

---

## 💡 Example Use Cases

### ❌ WRONG: Ask local model for weather
```python
# This would return outdated/hallucinated data
weather = call_glm("What's the weather in Miami?")  # DON'T DO THIS
```

### ✅ RIGHT: API for data, local model for summary
```python
# Get real weather
weather = curl_wttr_in("Miami")  # Real-time API

# Generate intelligent summary
summary = call_glm(f"Weather is {weather}. Should Cooper plan outdoor meetings today?")
```

### ❌ WRONG: Ask local model about X mentions
```python
mentions = call_glm("Search X for @coopwrenn mentions")  # Can't access X!
```

### ✅ RIGHT: API for search, local model for analysis
```python
# Real X search via Grok API
mentions = search_x_via_grok("@coopwrenn")  # Real-time data

# Analyze with local model
analysis = call_glm(f"These X mentions were found: {mentions}. Which need Cooper's attention?")
```

---

## 📊 Cost Breakdown

### Data Collection (APIs)
- Gmail IMAP: **FREE**
- Google Calendar: **FREE**  
- Stripe API: **FREE** (under rate limits)
- xAI Grok: **~$0.002/request** (pay-per-use)
- Brave Search: **FREE tier** (2,000 queries/month)
- Weather (wttr.in): **FREE**

**Monthly: ~$5-10 for API calls**

### Intelligence Layer
- GLM-4 (local): **$0**
- Nemotron 70B (local): **$0**

**Monthly: $0**

### Total Automation Cost
- **Before:** $60-150/month (all Claude API)
- **After:** $5-10/month (APIs) + $0 (local models)
- **Savings:** $50-140/month = **~1 month of runway preserved per year**

---

## 🎯 Quality Assurance

**Monitor these to ensure local models are good enough:**
1. Cooper's feedback on morning report quality
2. Are insights actually actionable?
3. Is anything critical being missed?

**If local models aren't cutting it:**
- Fallback to Claude for that specific task
- Document why local failed
- Keep trying to improve prompts for local models

**Default strategy:** Try local, escalate to Claude if needed.

---

## 🔐 Security Note

**Local models run on DGX** (our hardware, our control)
- No data leaves the machine during generation
- API calls still go to external services (Gmail, Stripe, etc.)
- Credentials stay local
- No third-party AI services see our business data during summarization

**This is actually MORE secure** than sending everything to Claude.

---

## 📝 Summary

**The system architecture:**
1. **APIs** → Get REAL data (emails, revenue, calendar, X mentions)
2. **Local Models** → Process data into intelligence ($0 cost)
3. **Claude/API** → Only when local quality isn't good enough (rare)

**Cooper's concern addressed:**
- ✅ Real-time internet intelligence INTACT (all APIs still used)
- ✅ X search still uses xAI Grok API (real-time)
- ✅ Web search still uses Brave API (current results)
- ✅ All external data sources still active
- ✅ Local models only process/summarize, never fetch

**We're not losing intelligence - we're getting smarter about cost!**

*Last updated: 2026-01-28 by Ritchie*
