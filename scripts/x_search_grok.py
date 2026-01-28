#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Search X using Grok API (has real-time X access)
"""
import json
import requests
from datetime import datetime

def load_credentials():
    with open('/home/wrenn/clawd/xai-credentials.json', 'r') as f:
        return json.load(f)

def search_x_mentions():
    """Search for mentions of @coopwrenn and Yours Truly"""
    creds = load_credentials()
    
    # Ask Grok to search X for mentions
    prompt = """Search X (Twitter) for recent mentions and activity related to:
1. @coopwrenn
2. "Yours Truly" (the handwritten card/postcard company)

Return the most relevant posts from the last 24 hours. For each post include:
- Author username
- Post text
- Engagement (likes, retweets)
- Link to post

Format as JSON."""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {creds['api_key']}"
    }
    
    data = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that searches X (Twitter) and returns structured data."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": creds['model'],
        "stream": False,
        "temperature": 0
    }
    
    try:
        response = requests.post(creds['api_url'], headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Try to parse as JSON, otherwise return raw
        try:
            mentions_data = json.loads(content)
            return mentions_data
        except:
            return {
                'raw_response': content,
                'timestamp': datetime.now().isoformat()
            }
            
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    mentions = search_x_mentions()
    print(json.dumps(mentions, indent=2))
