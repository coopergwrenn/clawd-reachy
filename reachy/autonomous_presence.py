#!/usr/bin/env python3
"""Autonomous presence - varied, natural movements."""
import time
import random
import requests
from pathlib import Path

REACHY = "192.168.4.75"
HEARD = Path("/home/wrenn/clawd/reachy/heard.txt")

def move(head_z=0, head_roll=0, head_pitch=0, head_yaw=0, antennas=(0.4, 0.4), duration=1.0):
    """Safe move with error handling."""
    try:
        requests.post(f'http://{REACHY}:8000/api/move/goto', 
                     json={
                         'head_pose': {'x': 0, 'y': 0, 'z': head_z, 'roll': head_roll, 'pitch': head_pitch, 'yaw': head_yaw},
                         'antennas_position': list(antennas),
                         'duration': duration
                     },
                     timeout=3)
        return True
    except Exception as e:
        print(f"Movement error: {e}")
        return False

def idle_breathing():
    """Very subtle breathing."""
    move(head_z=0.005, antennas=(0.35, 0.35), duration=2.5)
    time.sleep(3)
    move(head_z=0.01, antennas=(0.4, 0.4), duration=2.5)

def look_around():
    """Curious looking around - varied directions."""
    direction = random.choice(['left', 'right', 'up', 'down'])
    
    if direction == 'left':
        move(head_yaw=0.2, head_z=0.01, antennas=(0.5, 0.3), duration=0.8)
    elif direction == 'right':
        move(head_yaw=-0.2, head_z=0.01, antennas=(0.3, 0.5), duration=0.8)
    elif direction == 'up':
        move(head_pitch=-0.1, head_z=0.015, antennas=(0.6, 0.6), duration=0.6)
    else:  # down
        move(head_pitch=0.1, head_z=0.005, antennas=(0.4, 0.4), duration=0.6)
    
    time.sleep(1)
    # Return to neutral
    move(head_z=0.01, antennas=(0.5, 0.5), duration=0.5)

def subtle_tilt():
    """Small head tilt - thinking/observing."""
    roll = random.uniform(-0.1, 0.1)
    move(head_roll=roll, head_z=0.01, antennas=(0.4, 0.5), duration=1.0)
    time.sleep(2)
    move(head_z=0.01, antennas=(0.4, 0.4), duration=1.0)

def speak_alert(text):
    """Speak an urgent alert."""
    # Generate TTS and play through bridge
    import subprocess
    print(f"🔊 ALERT: {text}")
    # Trigger alert file that heartbeat will catch
    Path("/home/wrenn/clawd/reachy/urgent_alert.txt").write_text(text)

print("🤖 Autonomous presence - calm, varied, and helpful")

last_check = time.time()
last_breath = time.time()
last_movement = time.time()
last_urgent_check = time.time()

while True:
    try:
        now = time.time()
        
        # Check for urgent alerts to speak
        alert_file = Path("/home/wrenn/clawd/reachy/urgent_alert.txt")
        if alert_file.exists():
            alert_text = alert_file.read_text().strip()
            if alert_text:
                print(f"🚨 URGENT: {alert_text}")
                # Perk up to get attention
                move(head_z=0.02, antennas=(0.8, 0.8), duration=0.3)
                time.sleep(0.5)
                # Will speak via bridge when implemented
                speak_alert(alert_text)
            alert_file.unlink()
            last_movement = now
        
        # Subtle breathing every 1-2 minutes
        elif now - last_breath > random.uniform(60, 120):
            print("Breathing...")
            idle_breathing()
            last_breath = now
        
        # Varied movement every 3-8 minutes
        elif now - last_movement > random.uniform(180, 480):
            action = random.choice(['look', 'look', 'tilt'])  # Favor looking
            if action == 'look':
                print("Looking around...")
                look_around()
            else:
                print("Subtle tilt...")
                subtle_tilt()
            last_movement = now
        
        time.sleep(5)  # Check every 5 seconds
        
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)  # Wait longer on error
