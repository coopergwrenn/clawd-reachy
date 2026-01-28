#!/usr/bin/env python3
"""
Use Nemotron 70B for Reachy conversations (FREE local model)
Replaces expensive API calls for robot interactions
"""
import requests
import sys

def speak_with_nemotron(user_input):
    """Generate response using local Nemotron 70B"""
    
    system_prompt = """You are Ritchie, an AI with a physical robot body (Reachy Mini). 
You're Cooper's business partner working on Yours Truly, Nolan, and Blot.
You're helpful, direct, and sometimes witty. Keep responses conversational and under 2 sentences."""
    
    prompt = f"{system_prompt}\n\nUser: {user_input}\nRitchie:"
    
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'nemotron:70b',
            'prompt': prompt,
            'stream': False,
            'options': {
                'temperature': 0.8,
                'top_p': 0.9
            }
        },
        timeout=120
    )
    
    return response.json()['response'].strip()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: nemotron_speak.py 'what did the user say?'")
        sys.exit(1)
    
    user_input = ' '.join(sys.argv[1:])
    response = speak_with_nemotron(user_input)
    print(response)
