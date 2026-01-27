#!/usr/bin/env node
/**
 * Winner Alert System
 * Identifies high-value ads and sends Telegram alerts
 */

const fs = require('fs').promises;
const path = require('path');

function scoreAd(ad, source) {
  let score = 0;
  
  // Facebook scoring
  if (source === 'facebook') {
    // Ads with longer copy often perform well
    if (ad.bodyText && ad.bodyText.length > 100) score += 2;
    
    // Multiple media = more investment
    if (ad.media && ad.media.length > 1) score += 2;
    
    // Strong CTAs
    if (ad.linkText && ad.linkText.length > 0) score += 1;
    
    // Long-running ads (likely winners)
    if (ad.startDate) {
      const startDate = new Date(ad.startDate);
      const now = new Date();
      const daysRunning = (now - startDate) / (1000 * 60 * 60 * 24);
      
      if (daysRunning > 30) score += 3;
      else if (daysRunning > 14) score += 2;
      else if (daysRunning > 7) score += 1;
    }
  }
  
  // TikTok scoring
  if (source === 'tiktok') {
    // High engagement
    if (ad.stats) {
      if (ad.stats.likes && parseInt(ad.stats.likes) > 1000) score += 3;
      if (ad.stats.comments && parseInt(ad.stats.comments) > 100) score += 2;
      if (ad.stats.shares && parseInt(ad.stats.shares) > 50) score += 2;
    }
    
    // Video content (if present)
    if (ad.videoUrl) score += 1;
  }
  
  return score;
}

async function identifyWinners() {
  const dataDir = path.join(__dirname, '../data/combined');
  const files = await fs.readdir(dataDir);
  const jsonFiles = files.filter(f => f.endsWith('.json')).sort().reverse();
  
  if (jsonFiles.length === 0) {
    console.log('No data files found');
    return { winners: [], threshold: 5 };
  }
  
  const filepath = path.join(dataDir, jsonFiles[0]);
  const content = await fs.readFile(filepath, 'utf-8');
  const data = JSON.parse(content);
  
  const winners = [];
  const threshold = 5; // Minimum score to be considered a "winner"
  
  // Check previous file to find NEW winners
  let previousData = null;
  if (jsonFiles.length > 1) {
    const prevPath = path.join(dataDir, jsonFiles[1]);
    try {
      previousData = JSON.parse(await fs.readFile(prevPath, 'utf-8'));
    } catch (e) {
      // Previous file not available, that's okay
    }
  }
  
  // Score Facebook ads
  if (data.sources?.facebook?.competitors) {
    for (const [competitor, ads] of Object.entries(data.sources.facebook.competitors)) {
      ads.forEach(ad => {
        const score = scoreAd(ad, 'facebook');
        if (score >= threshold) {
          winners.push({
            source: 'facebook',
            competitor,
            score,
            ad,
            isNew: !previousData // Mark as new if no previous data
          });
        }
      });
    }
  }
  
  // Score TikTok ads
  if (data.sources?.tiktok?.keywords) {
    for (const [keyword, ads] of Object.entries(data.sources.tiktok.keywords)) {
      ads.forEach(ad => {
        const score = scoreAd(ad, 'tiktok');
        if (score >= threshold) {
          winners.push({
            source: 'tiktok',
            keyword,
            score,
            ad,
            isNew: !previousData
          });
        }
      });
    }
  }
  
  // Sort by score
  winners.sort((a, b) => b.score - a.score);
  
  return { winners, threshold };
}

function formatTelegramMessage(winners) {
  if (winners.length === 0) {
    return '📊 **Ad Intel Daily Report**\n\nNo new high-performing ads detected today.';
  }
  
  let message = `🎯 **Ad Intel Alert**\n\nFound ${winners.length} high-performing ads:\n\n`;
  
  // Show top 5
  const topWinners = winners.slice(0, 5);
  
  topWinners.forEach((winner, index) => {
    message += `**${index + 1}. ${winner.source.toUpperCase()}** (Score: ${winner.score})\n`;
    
    if (winner.source === 'facebook') {
      message += `📘 **${winner.competitor}**\n`;
      if (winner.ad.bodyText) {
        const preview = winner.ad.bodyText.substring(0, 150);
        message += `💬 "${preview}${winner.ad.bodyText.length > 150 ? '...' : ''}"\n`;
      }
      if (winner.ad.linkText) {
        message += `🔗 ${winner.ad.linkText}\n`;
      }
      if (winner.ad.startDate) {
        message += `📅 Running since: ${winner.ad.startDate}\n`;
      }
    } else if (winner.source === 'tiktok') {
      message += `🎵 **${winner.keyword}**\n`;
      if (winner.ad.title) {
        message += `📝 ${winner.ad.title}\n`;
      }
      if (winner.ad.stats) {
        const stats = [];
        if (winner.ad.stats.likes) stats.push(`❤️ ${winner.ad.stats.likes}`);
        if (winner.ad.stats.comments) stats.push(`💬 ${winner.ad.stats.comments}`);
        if (winner.ad.stats.shares) stats.push(`🔄 ${winner.ad.stats.shares}`);
        if (stats.length > 0) {
          message += stats.join(' | ') + '\n';
        }
      }
    }
    
    message += '\n';
  });
  
  if (winners.length > 5) {
    message += `\n_...and ${winners.length - 5} more. Check the full report for details._`;
  }
  
  return message;
}

async function main() {
  console.log('🚨 Analyzing ads for winners...\n');
  
  const { winners, threshold } = await identifyWinners();
  
  console.log(`📊 Found ${winners.length} ads scoring ≥${threshold}\n`);
  
  const message = formatTelegramMessage(winners);
  console.log('─'.repeat(50));
  console.log(message);
  console.log('─'.repeat(50));
  
  // Save alert data
  const date = new Date().toISOString().split('T')[0];
  const alertPath = path.join(__dirname, '../reports', `alert-${date}.json`);
  await fs.writeFile(alertPath, JSON.stringify({ winners, message }, null, 2));
  
  console.log(`\n💾 Alert data saved: ${alertPath}`);
  console.log('\n✅ Ready to send to Telegram');
  
  // Return message for Clawdbot to send
  return { message, winners };
}

if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = { identifyWinners, formatTelegramMessage };
