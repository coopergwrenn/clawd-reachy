#!/usr/bin/env node
/**
 * Facebook Ad Library Scraper
 * Scrapes competitor ads and extracts engagement signals
 */

const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');

const COMPETITORS = [
  'Escargot',
  'Postable',
  'Punkpost',
  'Handwrytten',
  'Simply Noted'
];

const SEARCH_TERMS = [
  'handwritten cards',
  'personalized postcards',
  'greeting cards',
  'thank you cards',
  'custom stationery'
];

async function scrapeAdLibrary(query, region = 'US') {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();
    
    // Facebook Ad Library URL
    const url = `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=${region}&q=${encodeURIComponent(query)}&search_type=keyword_unordered`;
    
    console.log(`Scraping: ${query}`);
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
    
    // Wait for ads to load
    await page.waitForSelector('[data-testid="search_result_item"]', { timeout: 10000 });
    
    // Extract ad data
    const ads = await page.evaluate(() => {
      const results = [];
      const adCards = document.querySelectorAll('[data-testid="search_result_item"]');
      
      adCards.forEach((card, index) => {
        if (index >= 20) return; // Limit to 20 ads per query
        
        const advertiser = card.querySelector('[role="heading"]')?.textContent?.trim() || 'Unknown';
        const bodyText = card.querySelector('[data-testid="ad_creative_body"]')?.textContent?.trim() || '';
        const linkText = card.querySelector('[data-testid="ad_creative_link_title"]')?.textContent?.trim() || '';
        const startDate = card.querySelector('[data-testid="ad_start_date"]')?.textContent?.trim() || '';
        
        // Extract image/video URLs
        const media = [];
        card.querySelectorAll('img').forEach(img => {
          if (img.src && !img.src.includes('emoji')) {
            media.push({ type: 'image', url: img.src });
          }
        });
        
        card.querySelectorAll('video').forEach(video => {
          if (video.src) {
            media.push({ type: 'video', url: video.src });
          }
        });
        
        results.push({
          advertiser,
          bodyText,
          linkText,
          startDate,
          media,
          scrapedAt: new Date().toISOString()
        });
      });
      
      return results;
    });
    
    return ads;
    
  } catch (error) {
    console.error(`Error scraping ${query}:`, error.message);
    return [];
  } finally {
    await browser.close();
  }
}

async function scrapeAllCompetitors() {
  const results = {
    scrapedAt: new Date().toISOString(),
    competitors: {},
    searchTerms: {}
  };
  
  // Scrape by competitor name
  for (const competitor of COMPETITORS) {
    console.log(`\n🔍 Scraping competitor: ${competitor}`);
    const ads = await scrapeAdLibrary(competitor);
    results.competitors[competitor] = ads;
    
    // Rate limit
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  
  // Scrape by search term
  for (const term of SEARCH_TERMS) {
    console.log(`\n🔍 Scraping search term: ${term}`);
    const ads = await scrapeAdLibrary(term);
    results.searchTerms[term] = ads;
    
    // Rate limit
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  
  return results;
}

async function saveResults(results) {
  const date = new Date().toISOString().split('T')[0];
  const dataDir = path.join(__dirname, '../data/facebook');
  
  await fs.mkdir(dataDir, { recursive: true });
  
  const filepath = path.join(dataDir, `${date}.json`);
  await fs.writeFile(filepath, JSON.stringify(results, null, 2));
  
  console.log(`\n✅ Saved ${filepath}`);
  return filepath;
}

async function main() {
  console.log('🚀 Starting Facebook Ad Library scraper...\n');
  
  const results = await scrapeAllCompetitors();
  
  const totalAds = 
    Object.values(results.competitors).flat().length +
    Object.values(results.searchTerms).flat().length;
  
  console.log(`\n📊 Scraped ${totalAds} ads total`);
  
  await saveResults(results);
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { scrapeAdLibrary, scrapeAllCompetitors };
