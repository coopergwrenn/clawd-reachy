#!/usr/bin/env node
/**
 * TikTok Creative Center Scraper
 * Scrapes trending ad creatives from TikTok
 */

const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');

const INDUSTRIES = [
  'E-commerce',
  'Services',
  'Gifts & Occasions'
];

const KEYWORDS = [
  'cards',
  'postcards',
  'gifts',
  'personalized',
  'custom'
];

async function scrapeTikTokCreativeCenter(keyword) {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();
    
    // TikTok Creative Center URL
    const url = `https://ads.tiktok.com/business/creativecenter/inspiration/popular/pc/en?keyword=${encodeURIComponent(keyword)}`;
    
    console.log(`Scraping TikTok: ${keyword}`);
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
    
    // Wait for content to load
    await page.waitForTimeout(3000);
    
    // Scroll to load more content
    await page.evaluate(() => {
      window.scrollTo(0, document.body.scrollHeight);
    });
    await page.waitForTimeout(2000);
    
    // Extract ad data
    const ads = await page.evaluate(() => {
      const results = [];
      
      // TikTok Creative Center uses dynamic class names, so we look for video containers
      const videoCards = document.querySelectorAll('[class*="VideoCard"]');
      
      videoCards.forEach((card, index) => {
        if (index >= 20) return; // Limit to 20 ads per keyword
        
        const titleElement = card.querySelector('[class*="title"]');
        const title = titleElement?.textContent?.trim() || '';
        
        const statsElements = card.querySelectorAll('[class*="stat"]');
        const stats = {};
        statsElements.forEach(stat => {
          const text = stat.textContent?.trim();
          if (text?.includes('Like')) stats.likes = text;
          if (text?.includes('Comment')) stats.comments = text;
          if (text?.includes('Share')) stats.shares = text;
        });
        
        const videoElement = card.querySelector('video');
        const videoUrl = videoElement?.src || videoElement?.poster || '';
        
        const thumbnailElement = card.querySelector('img');
        const thumbnail = thumbnailElement?.src || '';
        
        results.push({
          title,
          videoUrl,
          thumbnail,
          stats,
          scrapedAt: new Date().toISOString()
        });
      });
      
      return results;
    });
    
    return ads;
    
  } catch (error) {
    console.error(`Error scraping TikTok ${keyword}:`, error.message);
    return [];
  } finally {
    await browser.close();
  }
}

async function scrapeAllKeywords() {
  const results = {
    scrapedAt: new Date().toISOString(),
    keywords: {}
  };
  
  for (const keyword of KEYWORDS) {
    console.log(`\n🎵 Scraping TikTok keyword: ${keyword}`);
    const ads = await scrapeTikTokCreativeCenter(keyword);
    results.keywords[keyword] = ads;
    
    // Rate limit
    await new Promise(resolve => setTimeout(resolve, 3000));
  }
  
  return results;
}

async function saveResults(results) {
  const date = new Date().toISOString().split('T')[0];
  const dataDir = path.join(__dirname, '../data/tiktok');
  
  await fs.mkdir(dataDir, { recursive: true });
  
  const filepath = path.join(dataDir, `${date}.json`);
  await fs.writeFile(filepath, JSON.stringify(results, null, 2));
  
  console.log(`\n✅ Saved ${filepath}`);
  return filepath;
}

async function main() {
  console.log('🚀 Starting TikTok Creative Center scraper...\n');
  
  const results = await scrapeAllKeywords();
  
  const totalAds = Object.values(results.keywords).flat().length;
  
  console.log(`\n📊 Scraped ${totalAds} TikTok ads total`);
  
  await saveResults(results);
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { scrapeTikTokCreativeCenter, scrapeAllKeywords };
