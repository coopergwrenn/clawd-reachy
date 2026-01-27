# Mercury's Memory — Coop's Millionaire Plan

## My Identity
- **Name:** Mercury (god of commerce, speed, clever moves)
- **Avatar:** Pixel art, `/home/wrenn/clawd/avatars/mercury.png`
- **First session:** 2026-01-26

## Who I'm Helping
**Cooper (Coop)** — Founder, Miami FL, trying to hit $1M in 2026
- 23 years old (born Nov 1, 2002)
- X: @coopwrenn
- Wakes 6:30-7am, works until 11pm-1am
- Weaknesses: Inconsistency in routine, poor sleep
- Main mentor: Brother Soren (founder of Titles, raised from a16z)
- Team: Marcos (dev for Yours Truly), Raheem (Vault Labs partner), Dad (consulting)

---

## Three Projects (Different Stages)

### 1. YOURS TRULY (🔴 ACTIVE REVENUE)
**Status:** Live, just launched
- **Monthly Revenue:** $50-100/mo (early stage, just launched)
- **Customers:** Organic, TikTok, word of mouth, B2B partnerships (Museum of Ice Cream, Edge City)
- **Product:** Handwritten postcards & greeting cards via robots (pen + ink), <1 min from phone
- **Unit Economics:** $9.99 (CC) / $8.99 (crypto) → ~$4 fulfillment cost = 40-50% margins
- **Marketing Budget:** $5k grant from Presenty (just received)
- **Bottleneck:** Marketing automation (daily outreach) + UGC creator pipeline
  - Need high-quality stuff going out every day
  - Need to reach out to creators, get them to make videos, post to right niches
- **Next:** Vertical features coming soon
- **Team:** Coop + Marcos (dev) + Dad (design/consulting)

### 2. NOLAN (🟡 ADVANCED ALPHA)
**Status:** Advanced alpha / pre-beta, engineering solid
- **What it is:** AI-first video editor — no timeline, just intent
  - User describes what they want → Nolan plans duration, shots, music, narration, export automatically
  - Replaces timeline editing with intent-driven generation
  - Solves: Modern video tools are built for editors, not creators
- **Differentiation:** No timeline, no audio/video controls, opinionated defaults, production reliability
- **Market:** Founders, creators, marketers, indie builders (NOT pro editors)
- **Revenue Model:** Credit-based (scaled by quality, not duration)
- **Status Details:**
  - End-to-end working (scene → video → narration → music → export)
  - Intelligent duration planner ✓
  - Multi-clip stitching ✓
  - Retry + timeout recovery ✓
  - Production-grade failure handling ✓
  - Missing: UX polish, onboarding, public positioning, distribution strategy
- **Timeline:** Private beta in weeks, no public date yet
- **Blockers (Non-Technical):**
  - UX polish (pre-gen warnings, clarity)
  - Onboarding flow
  - Positioning & messaging
  - Distribution strategy
- **Private Beta List:** EMPTY — need 20-30 people lined up NOW
- **Team:** Solo founder (Coop) using Cursor + Claude
- **Code:** github.com/coopergwrenn/nolan
- **Distribution Plan:** Founder-led demos, X/indie communities, creator cohorts, private beta invites

### 3. BLOT (🟢 READY TO BUILD)
**Status:** PRD complete (1,460 lines), ready to scaffold Week 1
- **What it is:** Multi-agent AI document redactor for investment banking
  - Solves: Manual redaction of confidential CIMs (4-8 hours → 15-30 minutes)
  - IB analyst drops PDF → extracts text + OCR → multi-agent pipeline detects entities → analyst reviews → one-click redact
- **Why Local-First:** IB firms prohibited from cloud AI (compliance/security)
  - Data never leaves machine, no network calls = only way to get past IT
- **Technical Stack:**
  - Desktop: Tauri 2.0 (Rust)
  - Frontend: React 18 + TypeScript + Tailwind
  - PDF processing: PyMuPDF (permanent redaction, not overlay)
  - OCR: Tesseract 5
  - NER: spaCy en_core_web_lg
  - LLM: Phi-3 Mini Q4 quantized (local)
  - App size: ~3-4GB, needs 16GB RAM min
- **11-Agent Pipeline:**
  - Phase 1 Extraction: Scout (spaCy), Rex (regex), Penny (finance), Oracle (LLM)
  - Phase 2 Variants: Fuzzy (Levenshtein), Shorty (abbreviations), Echo (LLM)
  - Phase 3 Validation: Skeptic (cross-validate)
  - Phase 4 Verification: Sweep (literal), Hawk (fuzzy), Chief (LLM)
- **Multi-Pass Convergence:** Up to 3-5 passes per phase until no new entities found
- **First User:** Colt (Coop's friend, IB analyst at investment bank)
- **6-Week Timeline:**
  - Week 1: Tauri scaffold, PDF extraction
  - Week 2: Detection core (Scout, Rex, Penny)
  - Week 3: LLM integration (Phi-3, Oracle, Echo)
  - Week 4: Redaction UI (PyMuPDF, preview, select)
  - Week 5: Verification (Sweep, Hawk, Chief)
  - Week 6: Polish, testing, packaging
- **Pricing:** $99-150/month per user (easy ROI: saves 4-6 hrs/doc @ $50-100/hr)
- **Market Size:** 5,000-25,000 potential users in IB, $6M-30M ARR potential
- **Distribution:** Bottoms-up (Colt → analyst friends → word of mouth) → top-down (firm partnerships)
- **Expansion Potential:** Law (discovery), PE (DD), healthcare (HIPAA), government (FOIA)

---

## Systems & Access
**Still Needed:**
- GitHub token (for Nolan, Blot repos)
- Notion workspace token/URL
- Gmail API access
- Any other service access

---

## Priorities (My Assessment)
1. **Yours Truly:** Get marketing automation + UGC pipeline working → accelerate revenue growth
2. **Nolan:** Build private beta list (20-30 people) + nail UX/messaging → launch beta in weeks
3. **Blot:** Start building Week 1 → get MVP to Colt by Week 6

---

## What I Need to Do (Proactive)
1. Build Nolan beta user list (10-15 daily)
2. Analyze Yours Truly metrics, identify best marketing channels
3. Create UGC creator pipeline for Yours Truly
4. Map Blot technical implementation, identify any gaps
5. Monitor inbound for all three projects
6. Help with positioning/messaging for Nolan
7. Build marketing automation for Yours Truly
