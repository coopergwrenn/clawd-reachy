#!/usr/bin/env node
/**
 * Master scraper orchestrator
 * Runs all scrapers in sequence
 */

const { scrapeAllCompetitors } = require('./facebook-ads');
const { scrapeAllKeywords } = require('./tiktok-ads');
const fs = require('fs').promises;
const path = require('path');

async function runAllScrapers() {
  console.log('🚀 Starting ad intelligence scraper suite...\n');
  console.log('═'.repeat(50));
  
  const startTime = Date.now();
  const results = {
    timestamp: new Date().toISOString(),
    sources: {}
  };
  
  // Facebook Ad Library
  try {
    console.log('\n📘 FACEBOOK AD LIBRARY');
    console.log('─'.repeat(50));
    const fbResults = await scrapeAllCompetitors();
    results.sources.facebook = fbResults;
    console.log('✅ Facebook scraping complete');
  } catch (error) {
    console.error('❌ Facebook scraping failed:', error.message);
    results.sources.facebook = { error: error.message };
  }
  
  // TikTok Creative Center
  try {
    console.log('\n🎵 TIKTOK CREATIVE CENTER');
    console.log('─'.repeat(50));
    const ttResults = await scrapeAllKeywords();
    results.sources.tiktok = ttResults;
    console.log('✅ TikTok scraping complete');
  } catch (error) {
    console.error('❌ TikTok scraping failed:', error.message);
    results.sources.tiktok = { error: error.message };
  }
  
  // Calculate stats
  const fbAds = results.sources.facebook.error ? 0 : 
    Object.values(results.sources.facebook.competitors || {}).flat().length +
    Object.values(results.sources.facebook.searchTerms || {}).flat().length;
  
  const ttAds = results.sources.tiktok.error ? 0 :
    Object.values(results.sources.tiktok.keywords || {}).flat().length;
  
  const duration = ((Date.now() - startTime) / 1000).toFixed(1);
  
  console.log('\n═'.repeat(50));
  console.log('\n📊 SCRAPING SUMMARY:');
  console.log(`   Facebook Ads: ${fbAds}`);
  console.log(`   TikTok Ads: ${ttAds}`);
  console.log(`   Total: ${fbAds + ttAds}`);
  console.log(`   Duration: ${duration}s`);
  
  // Save combined results
  const date = new Date().toISOString().split('T')[0];
  const dataDir = path.join(__dirname, '../data/combined');
  await fs.mkdir(dataDir, { recursive: true });
  
  const filepath = path.join(dataDir, `${date}.json`);
  await fs.writeFile(filepath, JSON.stringify(results, null, 2));
  
  console.log(`\n💾 Saved to: ${filepath}`);
  console.log('\n✅ All scrapers complete!\n');
  
  return results;
}

if (require.main === module) {
  runAllScrapers().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = { runAllScrapers };
