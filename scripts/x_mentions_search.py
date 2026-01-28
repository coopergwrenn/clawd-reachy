#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Check X for mentions using search (works with limited API access)
"""
import json
import subprocess
from datetime import datetime, timedelta

def search_mentions():
    """Search for mentions of @coopwrenn and Yours Truly"""
    
    queries = [
        "@coopwrenn",
        "yours truly cards",
        "yours truly postcards"
    ]
    
    results = {
        'mentions': [],
        'timestamp': datetime.now().isoformat()
    }
    
    for query in queries:
        # Use the x-search skill via node script
        try:
            result = subprocess.run(
                ['node', '/home/wrenn/clawd/skills/x-search/search.js', query],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data.get('tweets'):
                    results['mentions'].extend([
                        {
                            'query': query,
                            'author': tweet.get('author'),
                            'text': tweet.get('text'),
                            'engagement': tweet.get('engagement'),
                            'url': tweet.get('url')
                        }
                        for tweet in data['tweets'][:5]  # Top 5 per query
                    ])
        except Exception as e:
            results['errors'] = results.get('errors', [])
            results['errors'].append(f"{query}: {str(e)}")
    
    return results

if __name__ == '__main__':
    mentions = search_mentions()
    print(json.dumps(mentions, indent=2))
