#!/home/wrenn/clawd/scripts/venv/bin/python3
"""
Search for X mentions using web search (what actually works)
This is a wrapper that outputs JSON for the morning report
"""
import json
import sys
from datetime import datetime

# This script is meant to be called from the main morning report
# which has access to Clawdbot's web_search tool

# For now, return a placeholder that indicates manual search needed
def get_mentions():
    return {
        'note': 'X mentions checked via web_search during morning report generation',
        'timestamp': datetime.now().isoformat(),
        'queries': [
            'site:x.com @coopwrenn',
            'site:x.com "yours truly" cards',
            'site:x.com cooperwrenn'
        ]
    }

if __name__ == '__main__':
    print(json.dumps(get_mentions(), indent=2))
