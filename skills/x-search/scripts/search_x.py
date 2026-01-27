#!/usr/bin/env python3
"""Search X (Twitter) for posts using the v2 API"""

import requests
import json
import sys
from datetime import datetime, timedelta

def search_x(query, max_results=10, api_key=None, api_secret=None):
    """
    Search X for posts matching the query
    
    Args:
        query: Search query string
        max_results: Max number of results (1-100)
        api_key: X API Key
        api_secret: X API Secret
    
    Returns:
        List of posts with author, text, engagement
    """
    
    if not api_key or not api_secret:
        print("Error: X API credentials not provided")
        return []
    
    # X v2 API endpoint
    url = "https://api.twitter.com/2/tweets/search/recent"
    
    # Headers
    headers = {
        "Authorization": f"Bearer {api_secret}",  # For v2 API, we use Bearer token
    }
    
    # Query params
    params = {
        "query": query,
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "username,name,public_metrics",
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Build results with author info
            results = []
            users = {u["id"]: u for u in data.get("includes", {}).get("users", [])}
            
            for tweet in data.get("data", []):
                author_id = tweet.get("author_id")
                author = users.get(author_id, {})
                
                results.append({
                    "author": author.get("name", "Unknown"),
                    "handle": "@" + author.get("username", "unknown"),
                    "text": tweet.get("text", ""),
                    "created_at": tweet.get("created_at", ""),
                    "likes": tweet.get("public_metrics", {}).get("like_count", 0),
                    "retweets": tweet.get("public_metrics", {}).get("retweet_count", 0),
                    "replies": tweet.get("public_metrics", {}).get("reply_count", 0),
                    "tweet_id": tweet.get("id", ""),
                })
            
            return results
        
        elif response.status_code == 401:
            print("Error: Invalid X API credentials")
            return []
        else:
            print(f"Error: X API returned {response.status_code}")
            print(response.text[:200])
            return []
    
    except Exception as e:
        print(f"Error searching X: {e}")
        return []


def format_results(results):
    """Format search results for display"""
    if not results:
        print("No posts found.")
        return
    
    print(f"\n🔍 Found {len(results)} post(s):\n")
    
    for i, post in enumerate(results, 1):
        print(f"[{i}] {post['author']} ({post['handle']})")
        print(f"    {post['text'][:150]}...")
        print(f"    ❤️ {post['likes']} | 🔄 {post['retweets']} | 💬 {post['replies']}")
        print(f"    https://twitter.com/{post['handle'].lstrip('@')}/status/{post['tweet_id']}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 search_x.py '<query>' [max_results] [api_key] [api_secret]")
        sys.exit(1)
    
    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    api_key = sys.argv[3] if len(sys.argv) > 3 else None
    api_secret = sys.argv[4] if len(sys.argv) > 4 else None
    
    results = search_x(query, max_results, api_key, api_secret)
    format_results(results)
