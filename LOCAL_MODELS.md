# Local Models - Cost Savings Strategy

**Goal:** Preserve runway by using free local models instead of expensive API calls

---

## 💰 Cost Comparison

### Before (API Calls)
- **Morning reports:** Claude Sonnet (~1K tokens) = $0.003/report
- **Reachy conversations:** Claude (~500 tokens/interaction) = $0.0015/interaction  
- **Daily burn:** ~$2-5/day on automation alone
- **Monthly:** ~$60-150

### After (Local Models)
- **Morning reports:** GLM-4 (local) = $0.00
- **Reachy conversations:** Nemotron 70B (local) = $0.00
- **Daily burn:** $0 (only electricity)
- **Monthly:** $0 for AI inference

**Savings:** ~$60-150/month + preserves API quota for critical tasks

---

## 🤖 Available Models

### GLM-4 (5.5 GB)
- **Use for:** Morning reports, summaries, quick analysis
- **Speed:** ~2-5 seconds per response
- **Quality:** Good for structured business summaries
- **Model:** `glm4:latest`
- **Command:** `curl http://localhost:11434/api/generate -d '{"model":"glm4:latest","prompt":"...","stream":false}'`

### Nemotron 70B (42 GB)  
- **Use for:** Reachy conversations, complex reasoning, deep analysis
- **Speed:** ~10-30 seconds per response
- **Quality:** Excellent, comparable to Claude Sonnet
- **Model:** `nemotron:70b`
- **Command:** `curl http://localhost:11434/api/generate -d '{"model":"nemotron:70b","prompt":"...","stream":false}'`

---

## 📜 Scripts Created

### `/scripts/llm_local.py`
Python wrapper for easy local model access:
```python
from llm_local import call_glm, call_nemotron

# Fast summaries
summary = call_glm("Summarize this data...")

# Deep conversations  
response = call_nemotron("What should we prioritize?")
```

### `/scripts/send_morning_report_smart.py`
Morning briefing using GLM-4:
- Gathers data (emails, calendar, Stripe, weather)
- Feeds to GLM for intelligent summary
- Sends concise, actionable email
- **Cost: $0**

### `/reachy/nemotron_speak.py`
Reachy conversation engine:
- Uses Nemotron 70B for responses
- Personality: Ritchie (business partner, helpful, witty)
- Replaces expensive API calls
- **Cost: $0**

---

## 🔄 Updated Workflows

### Morning Reports (7:30 AM)
**Old:** Raw data dumps  
**New:** GLM-4 generates intelligent briefing

```bash
/home/wrenn/clawd/scripts/send_morning_report_smart.py
```

### Reachy Conversations
**Old:** Call Claude API ($$$)  
**New:** Use Nemotron 70B (free)

```bash
/home/wrenn/clawd/reachy/nemotron_speak.py "How's it going?"
```

---

## ⚡ Performance

### GLM-4
- **Latency:** 2-5 seconds
- **Good for:** Structured output, summaries, data analysis
- **Max tokens:** ~2K context window

### Nemotron 70B
- **Latency:** 10-30 seconds  
- **Good for:** Conversations, reasoning, creative responses
- **Max tokens:** ~8K context window

---

## 🎯 When to Use What

| Task | Model | Why |
|------|-------|-----|
| Morning reports | GLM-4 | Fast, structured, good enough |
| Business summaries | GLM-4 | Quick data → insights |
| Reachy conversations | Nemotron | High quality, personality |
| Complex analysis | Nemotron | Better reasoning |
| Weekly reviews | Nemotron | Needs deeper thought |
| Customer support drafts | GLM-4 | Fast, templated responses |

**Rule:** Use GLM for speed, Nemotron for quality. Both are free.

---

## 🚀 Deployment Status

✅ **GLM-4:** Installed, tested, integrated into morning reports  
✅ **Nemotron 70B:** Installed, ready for Reachy conversations  
✅ **Wrappers:** Python scripts created and tested  
🔄 **Migration:** Switching automation to local models  

---

## 📊 Monitoring

Track usage to ensure quality doesn't degrade:
- Morning report feedback from Cooper
- Reachy conversation quality
- Response times acceptable?

If local models don't cut it for something → fallback to API, but default to local.

---

## 💡 Future Optimizations

1. **Cache common responses** (weather, greetings, etc.)
2. **Fine-tune GLM** on business data for better summaries
3. **Quantize Nemotron** further if speed becomes issue
4. **Batch processing** where possible to reduce overhead

---

**Bottom line:** We're now running most automation on FREE local models. This preserves runway and only uses API credits for truly complex tasks that need Claude's reasoning.

**Estimated monthly savings:** $60-150 + API quota preservation

*Last updated: 2026-01-28 by Ritchie*
