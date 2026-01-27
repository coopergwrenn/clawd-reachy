# Ad Intelligence System

Automated ad scraping, pattern analysis, and creative generation for Yours Truly.

## What It Does

1. **Scrapes Competitor Ads** (Facebook Ad Library + TikTok Creative Center)
2. **Identifies Winners** (scores ads based on engagement & longevity)
3. **Sends Daily Alerts** (Telegram notifications for high-performers)
4. **Pattern Analysis** (Claude analyzes what's working)
5. **Creative Generation** (controlled - requires approval before scaling)

## Setup

### Install Dependencies

```bash
cd /home/wrenn/clawd/ad-intel
npm install
```

### Run Manually

```bash
# Full daily pipeline
./run-daily.sh

# Or run individual steps:
npm run scrape    # Scrape ad libraries
npm run notify    # Identify winners & generate alert
npm run analyze   # Deep pattern analysis (weekly)
```

## Daily Automation

The system runs automatically via HEARTBEAT.md every morning around 7:30 AM EST.

It will:
- Scrape competitor ads from Facebook & TikTok
- Score them based on engagement signals
- Alert you via Telegram if high-performers are found
- Store data in `data/` for historical analysis

## Data Structure

```
ad-intel/
├── scrapers/          # Ad library scrapers
│   ├── facebook-ads.js
│   ├── tiktok-ads.js
│   └── run-all.js
├── analysis/          # Pattern detection & alerts
│   ├── pattern-engine.js
│   ├── alert-winners.js
│   └── creative-gen.js (coming soon)
├── data/              # Scraped ad data (JSON)
│   ├── facebook/      # Daily Facebook scrapes
│   ├── tiktok/        # Daily TikTok scrapes
│   └── combined/      # Combined daily data
└── reports/           # Analysis reports & alerts
```

## Competitors Being Tracked

**Yours Truly:**
- Escargot
- Postable
- Punkpost
- Handwrytten
- Simply Noted

**Nolan** (add when ready):
- Descript
- Runway
- CapCut
- Opus Clip

## Winner Scoring

Ads are scored based on:

**Facebook:**
- Copy length (longer = more investment)
- Multiple media assets
- Strong CTAs
- Days running (30+ days = proven winner)

**TikTok:**
- Likes (1000+ = high engagement)
- Comments (100+ = viral potential)
- Shares (50+ = valuable content)
- Video presence

**Threshold:** Score ≥5 triggers an alert

## Creative Generation Workflow

**IMPORTANT:** Creative generation requires approval before scaling.

1. System identifies winning patterns
2. **You review samples first** (3-5 variations)
3. If approved, system generates 50-100 variations
4. Output: Scripts, hooks, CTAs ready for UGC/video production

This prevents wasting API credits on unwanted variations.

## Integration with Nolan

When ready, generated scripts can be piped directly into Nolan for video production:

```bash
# Future integration
node analysis/creative-gen.js --samples 5 --output scripts/
nolan generate --script scripts/winning-hook-1.txt
```

## Next Steps

- [ ] Install dependencies (`npm install`)
- [ ] Test manual run (`./run-daily.sh`)
- [ ] Verify Telegram alerts work
- [ ] Add Nolan competitors (when ready)
- [ ] Build creative generation workflow (controlled)

## Cost Estimates

- **Scraping:** Free (public ad libraries)
- **Analysis (Claude):** ~$0.02-0.05 per daily run
- **Generation:** ~$0.10-0.20 per 100 variations

Total: ~$3-5/month for daily intel + weekly generation

## Troubleshooting

If scrapers fail:
1. Check internet connection
2. Ad libraries may have changed HTML structure
3. Run with `DEBUG=1` for verbose logs
4. Rate limits: scrapers include 2-3 second delays

If no winners detected:
1. Lower threshold in `alert-winners.js` (line 86)
2. Check if competitors are running new campaigns
3. Expand competitor list or search terms
