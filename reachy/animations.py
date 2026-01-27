#!/usr/bin/env python3
"""Cool animations for Reachy Mini."""

import requests
import time
import random
import math

REACHY_API = "http://192.168.4.75:8000"

def move(head_z=0, head_roll=0, head_pitch=0, head_yaw=0, antennas=(0.3, 0.3), duration=0.5):
    """Move to position."""
    requests.post(f"{REACHY_API}/api/move/goto", json={
        "head_pose": {"x": 0, "y": 0, "z": head_z, "roll": head_roll, "pitch": head_pitch, "yaw": head_yaw},
        "antennas_position": list(antennas),
        "duration": duration
    }, timeout=5)

def look_around():
    """Curious looking around animation."""
    move(head_yaw=0.3, head_z=0.01, antennas=(0.5, 0.3), duration=0.4)
    time.sleep(0.5)
    move(head_yaw=-0.3, head_z=0.01, antennas=(0.3, 0.5), duration=0.4)
    time.sleep(0.5)
    move(head_yaw=0, head_z=0.015, antennas=(0.6, 0.6), duration=0.3)

def nod_yes():
    """Enthusiastic nodding."""
    for _ in range(2):
        move(head_z=0.02, head_pitch=-0.15, antennas=(0.5, 0.5), duration=0.2)
        time.sleep(0.25)
        move(head_z=0, head_pitch=0.1, antennas=(0.4, 0.4), duration=0.2)
        time.sleep(0.25)
    move(head_z=0.01, antennas=(0.5, 0.5), duration=0.3)

def excited_wiggle():
    """Excited wiggling."""
    for _ in range(3):
        move(head_roll=0.15, head_z=0.015, antennas=(0.8, 0.6), duration=0.15)
        time.sleep(0.2)
        move(head_roll=-0.15, head_z=0.015, antennas=(0.6, 0.8), duration=0.15)
        time.sleep(0.2)
    move(head_z=0.01, antennas=(0.7, 0.7), duration=0.2)

def thinking_tilt():
    """Thoughtful head tilt."""
    move(head_roll=0.2, head_z=0.01, head_yaw=0.1, antennas=(0.5, 0.2), duration=0.6)
    time.sleep(0.5)
    move(head_roll=0.25, antennas=(0.6, 0.15), duration=0.4)

def surprised_jump():
    """Surprised reaction."""
    move(head_z=0.03, antennas=(1.0, 1.0), duration=0.15)
    time.sleep(0.2)
    move(head_z=0.015, antennas=(0.7, 0.7), duration=0.3)

def listening_attentive():
    """Attentive listening pose with subtle movement."""
    move(head_z=0.01, head_pitch=-0.05, head_yaw=0.05, antennas=(0.5, 0.5), duration=0.4)

def speaking_animation():
    """Subtle movements while speaking."""
    for _ in range(4):
        offset = random.uniform(-0.1, 0.1)
        z_offset = random.uniform(0, 0.01)
        move(head_roll=offset, head_z=0.01 + z_offset, antennas=(0.5 + random.uniform(0, 0.2), 0.5 + random.uniform(0, 0.2)), duration=0.3)
        time.sleep(0.4)

def happy_bounce():
    """Happy bouncing."""
    for _ in range(2):
        move(head_z=0.025, antennas=(0.8, 0.8), duration=0.2)
        time.sleep(0.25)
        move(head_z=0.005, antennas=(0.6, 0.6), duration=0.2)
        time.sleep(0.25)
    move(head_z=0.015, antennas=(0.7, 0.7), duration=0.3)

def idle_breathing():
    """Subtle idle breathing animation."""
    move(head_z=0.005, antennas=(0.35, 0.35), duration=1.5)
    time.sleep(1.5)
    move(head_z=0.01, antennas=(0.4, 0.4), duration=1.5)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        anim = sys.argv[1]
        if anim == "look": look_around()
        elif anim == "nod": nod_yes()
        elif anim == "wiggle": excited_wiggle()
        elif anim == "think": thinking_tilt()
        elif anim == "surprise": surprised_jump()
        elif anim == "listen": listening_attentive()
        elif anim == "speak": speaking_animation()
        elif anim == "happy": happy_bounce()
        elif anim == "idle": idle_breathing()
        else: print(f"Unknown: {anim}")
    else:
        print("Animations: look, nod, wiggle, think, surprise, listen, speak, happy, idle")
