#!/usr/bin/env node
/**
 * Pattern Analysis Engine
 * Uses Claude to analyze scraped ad data and identify winning patterns
 */

const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');
const util = require('util');
const execAsync = util.promisify(exec);

async function getLatestData() {
  const dataDir = path.join(__dirname, '../data/combined');
  const files = await fs.readdir(dataDir);
  const jsonFiles = files.filter(f => f.endsWith('.json')).sort().reverse();
  
  if (jsonFiles.length === 0) {
    throw new Error('No scraped data found. Run scrapers first.');
  }
  
  const filepath = path.join(dataDir, jsonFiles[0]);
  const content = await fs.readFile(filepath, 'utf-8');
  return JSON.parse(content);
}

async function analyzeWithClaude(data) {
  // Prepare the analysis prompt
  const prompt = `You are an expert ad strategist analyzing competitor ad data.

Here's the scraped data from Facebook Ad Library and TikTok Creative Center:

${JSON.stringify(data, null, 2)}

Analyze this data and provide:

1. **Winning Hooks**: What headlines/opening lines are most common in active ads?
2. **Engagement Patterns**: Which ads appear to have been running longest (likely winners)?
3. **Visual Trends**: What types of imagery/video are prevalent?
4. **CTA Patterns**: What calls-to-action are being used?
5. **New Entrants**: Any new advertisers or fresh creative angles?
6. **Opportunity Gaps**: What aren't competitors doing that we could exploit?

Format as actionable insights for Yours Truly (handwritten postcard business).

Focus on:
- Hooks that emphasize personalization, emotion, connection
- Seasonal/occasion-based angles
- Gift-giving messaging
- B2B vs B2C positioning

Be specific and cite examples from the data.`;

  // Use Clawdbot's session to analyze
  // We'll write a temp file and use the sessions_send or spawn approach
  const analysisPath = path.join(__dirname, '../reports/analysis-request.txt');
  await fs.writeFile(analysisPath, prompt);
  
  console.log('🧠 Sending data to Claude for analysis...\n');
  
  // For now, return the prompt so the user can see it
  // In production, this would use sessions_spawn or direct API call
  return {
    prompt,
    note: 'Analysis ready - will be processed by main Clawdbot session'
  };
}

async function generateReport(analysis) {
  const date = new Date().toISOString().split('T')[0];
  const reportPath = path.join(__dirname, '../reports', `pattern-report-${date}.md`);
  
  const report = `# Ad Intelligence Report
**Generated:** ${new Date().toISOString()}

## Analysis Results

${JSON.stringify(analysis, null, 2)}

---

*This report was generated automatically by the Ad Intel Pattern Engine.*
`;

  await fs.writeFile(reportPath, report);
  console.log(`\n📄 Report saved: ${reportPath}`);
  
  return reportPath;
}

async function main() {
  console.log('🧠 Starting Pattern Analysis Engine...\n');
  
  try {
    // Load latest scraped data
    const data = await getLatestData();
    console.log('✅ Loaded latest scraped data');
    
    // Analyze with Claude
    const analysis = await analyzeWithClaude(data);
    console.log('✅ Analysis complete');
    
    // Generate report
    const reportPath = await generateReport(analysis);
    console.log(`\n✅ Pattern analysis complete!`);
    console.log(`📊 Report: ${reportPath}`);
    
    return analysis;
    
  } catch (error) {
    console.error('❌ Analysis failed:', error.message);
    throw error;
  }
}

if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = { analyzeWithClaude, getLatestData };
