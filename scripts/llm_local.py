#!/usr/bin/env python3
"""
Local LLM wrapper - use GLM-4 or Nemotron instead of API calls
"""
import requests
import json
import sys

def call_glm(prompt, system="You are a helpful business assistant."):
    """Use GLM-4 for fast, efficient text generation (morning reports, summaries)"""
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'glm4:latest',
            'prompt': f"{system}\n\n{prompt}",
            'stream': False
        },
        timeout=30
    )
    return response.json()['response']

def call_nemotron(prompt, system="You are Ritchie, Cooper's AI business partner."):
    """Use Nemotron 70B for deeper conversations (Reachy interactions, complex analysis)"""
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'nemotron:70b',
            'prompt': f"{system}\n\n{prompt}",
            'stream': False
        },
        timeout=120
    )
    return response.json()['response']

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: llm_local.py <glm|nemotron> 'prompt here'")
        sys.exit(1)
    
    model = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else ""
    
    if model == 'glm':
        print(call_glm(prompt))
    elif model == 'nemotron':
        print(call_nemotron(prompt))
    else:
        print(f"Unknown model: {model}. Use 'glm' or 'nemotron'")
        sys.exit(1)
