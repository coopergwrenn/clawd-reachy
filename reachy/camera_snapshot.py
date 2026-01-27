#!/usr/bin/env python3
"""
Take a snapshot from Reachy Mini's camera.
Tries multiple methods to get an image.
"""

import sys
import os
import time
import requests
from pathlib import Path
from datetime import datetime

REACHY_HOST = "192.168.4.75"
SNAPSHOT_DIR = Path("/home/wrenn/clawd/reachy/snapshots")

# Ensure snapshot directory exists
SNAPSHOT_DIR.mkdir(exist_ok=True)


def try_webrtc_snapshot():
    """Try to get snapshot via WebRTC (requires SDK with gstreamer)."""
    try:
        sys.path.insert(0, '/home/wrenn/clawd/reachy-venv/lib/python3.12/site-packages')
        from reachy_mini import ReachyMini
        
        with ReachyMini(connection_mode='network', timeout=10) as mini:
            frame = mini.media.get_frame()
            if frame is not None:
                import cv2
                filename = SNAPSHOT_DIR / f"snap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(str(filename), frame)
                print(f"✅ Saved: {filename}")
                return str(filename)
    except Exception as e:
        print(f"WebRTC method failed: {e}")
    return None


def try_http_snapshot():
    """Try various HTTP endpoints for snapshots."""
    endpoints = [
        f"http://{REACHY_HOST}:8000/camera/snapshot",
        f"http://{REACHY_HOST}:8000/api/camera/snapshot",
        f"http://{REACHY_HOST}:8000/snapshot",
        f"http://{REACHY_HOST}:8080/snapshot",
        f"http://{REACHY_HOST}:8554/snapshot",
    ]
    
    for url in endpoints:
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200 and resp.headers.get('content-type', '').startswith('image'):
                filename = SNAPSHOT_DIR / f"snap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                filename.write_bytes(resp.content)
                print(f"✅ Saved: {filename}")
                return str(filename)
        except:
            pass
    
    print("❌ No HTTP snapshot endpoint found")
    return None


def main():
    print(f"📷 Attempting to capture from Reachy Mini at {REACHY_HOST}...")
    
    # Try HTTP first (faster if available)
    result = try_http_snapshot()
    
    if not result:
        # Try WebRTC
        print("Trying WebRTC method...")
        result = try_webrtc_snapshot()
    
    if result:
        print(f"✅ Snapshot saved: {result}")
    else:
        print("❌ Could not capture snapshot")
        print("\nCamera access requires one of:")
        print("1. A snapshot app installed on Reachy Mini")
        print("2. GStreamer + WebRTC SDK setup")
        print("\nConsider installing the conversation app which handles camera.")


if __name__ == "__main__":
    main()
