#!/usr/bin/env python3
import requests
import json
from pathlib import Path
import time

REPLICATE_API_KEY = "r8_H7NpNJQwqwQDA2yQTxVFyVZsuaOWXYU3Oq5JG"

prompt = "professional digital art of Mercury, god of commerce and speed, modern aesthetic, dynamic energy, golden accents, clever confident expression, sleek tech-forward design, high quality"

# Try calling via the model identifier directly
payload = {
    "input": {
        "prompt": prompt,
        "image_size": "1024x1024"
    }
}

headers = {
    "Authorization": f"Token {REPLICATE_API_KEY}",
    "Content-Type": "application/json"
}

model = "black-forest-labs/flux-pro"

print(f"🎨 Generating Mercury avatar...")
print(f"Model: {model}")
print(f"Prompt: {prompt}\n")

try:
    # Create prediction using model identifier
    response = requests.post(
        f"https://api.replicate.com/v1/predictions",
        json={**payload, "stream": False},
        headers=headers,
        timeout=10
    )
    
    print(f"Response code: {response.status_code}")
    
    if response.status_code in [201, 200]:
        prediction = response.json()
        prediction_id = prediction.get("id")
        
        if prediction_id:
            print(f"⏳ Generation started (ID: {prediction_id})")
            
            # Poll for completion
            max_attempts = 180
            attempt = 0
            
            while attempt < max_attempts:
                check_response = requests.get(
                    f"https://api.replicate.com/v1/predictions/{prediction_id}",
                    headers=headers,
                    timeout=10
                )
                
                if check_response.status_code == 200:
                    prediction = check_response.json()
                    status = prediction.get("status")
                    
                    if status == "succeeded":
                        output = prediction.get("output")
                        if output:
                            image_url = output[0] if isinstance(output, list) else output
                            print(f"✓ Generation complete!")
                            print(f"URL: {image_url}\n")
                            
                            # Download and save
                            img_response = requests.get(image_url, timeout=30)
                            if img_response.status_code == 200:
                                output_dir = Path("/home/wrenn/clawd/avatars")
                                output_dir.mkdir(exist_ok=True)
                                
                                img_path = output_dir / "mercury.png"
                                with open(img_path, 'wb') as f:
                                    f.write(img_response.content)
                                print(f"✓ Saved to: {img_path}")
                                exit(0)
                        break
                    elif status == "failed":
                        print(f"✗ Failed: {prediction.get('error')}")
                        exit(1)
                    else:
                        print(f"Status: {status}... ({attempt+1}s)")
                
                attempt += 1
                time.sleep(1)
        else:
            print("No prediction ID returned")
            print(json.dumps(prediction, indent=2))
    else:
        print(f"API Error ({response.status_code}):")
        print(response.text[:500])
        exit(1)

except Exception as e:
    print(f"Error: {e}")
    exit(1)
