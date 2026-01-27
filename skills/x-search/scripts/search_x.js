#!/usr/bin/env node
/**
 * Search X (Twitter) for posts using the API v2
 */

const { TwitterApi } = require('twitter-api-v2');

async function searchX(query, maxResults = 10) {
  const client = new TwitterApi({
    appKey: 'HPbGGhHNq50Wk8IBWQatAJjds',
    appSecret: 'v7s3U8mDRz1OiyO8zJH6nax9z2DUOfzC8T7rCSyvu4U4aAaVau',
    accessToken: '1459579479047630851-SsS3asYMCBPqqkRly7QEBQ4GNQ9jcC',
    accessSecret: 'fKR3359TAOHXiDK5jw2X0VwPKjqrFc8O7vdlQl2TjtLw4',
  });

  try {
    const result = await client.v2.search(query, {
      max_results: Math.min(maxResults, 100),
      'tweet.fields': 'created_at,public_metrics,author_id',
      expansions: 'author_id',
      'user.fields': 'username,name,public_metrics',
    });

    if (!result.data || result.data.length === 0) {
      console.log('No posts found.');
      return;
    }

    // Build results with author info
    const users = {};
    if (result.includes && result.includes.users) {
      result.includes.users.forEach(u => {
        users[u.id] = u;
      });
    }

    console.log(`\n🔍 Found ${result.data.length} post(s):\n`);

    result.data.forEach((tweet, i) => {
      const author = users[tweet.author_id] || {};
      const metrics = tweet.public_metrics || {};

      console.log(`[${i + 1}] ${author.name || 'Unknown'} (@${author.username || 'unknown'})`);
      console.log(`    ${tweet.text.substring(0, 150)}${tweet.text.length > 150 ? '...' : ''}`);
      console.log(`    ❤️  ${metrics.like_count || 0} | 🔄 ${metrics.retweet_count || 0} | 💬 ${metrics.reply_count || 0}`);
      console.log(`    https://twitter.com/${author.username || 'unknown'}/status/${tweet.id}`);
      console.log();
    });

  } catch (error) {
    console.error('✗ Error searching X:', error.message);
    process.exit(1);
  }
}

// Get query from command line
const query = process.argv[2];
const maxResults = parseInt(process.argv[3] || '10');

if (!query) {
  console.log('Usage: node search_x.js "<query>" [max_results]');
  process.exit(1);
}

searchX(query, maxResults);
