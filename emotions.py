#!/usr/bin/env python3
"""Reachy Mini emotion controller for Clawd."""

import sys
import time
import numpy as np

# Add venv to path
sys.path.insert(0, '/home/wrenn/clawd/reachy-venv/lib/python3.12/site-packages')

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

# Emotion definitions: (head_z, head_roll, antenna_angle, duration)
# head_z: positive = look up, negative = look down (mm)
# head_roll: tilt left/right (degrees)
# antenna_angle: positive = perky, negative = droopy (degrees)

EMOTIONS = {
    "sleeping": {
        "head": {"z": -5, "roll": 5},
        "antennas": -10,
        "duration": 2.0,
        "animation": "breathe"
    },
    "idle": {
        "head": {"z": 0, "roll": 0},
        "antennas": 15,
        "duration": 1.0,
        "animation": "blink"
    },
    "happy": {
        "head": {"z": 15, "roll": 0},
        "antennas": 45,
        "duration": 0.8,
        "animation": "wiggle"
    },
    "working": {
        "head": {"z": 5, "roll": -5},
        "antennas": 20,
        "duration": 1.0,
        "animation": "think"
    },
    "thinking": {
        "head": {"z": 10, "roll": 15},
        "antennas": 30,  # Will be asymmetric
        "duration": 1.2,
        "animation": None
    },
    "surprised": {
        "head": {"z": 20, "roll": 0},
        "antennas": 60,
        "duration": 0.3,
        "animation": "shake"
    },
    "sad": {
        "head": {"z": -15, "roll": 0},
        "antennas": -25,
        "duration": 1.5,
        "animation": None
    },
    "excited": {
        "head": {"z": 10, "roll": 0},
        "antennas": 50,
        "duration": 0.5,
        "animation": "bounce"
    },
}


class ClawdEmotions:
    """Control Reachy Mini emotions for Clawd."""
    
    def __init__(self, host: str = None):
        """Initialize connection to Reachy Mini.
        
        Args:
            host: IP address of Reachy Mini. If None, auto-discovers.
        """
        self.host = host
        self.mini = None
        self.current_emotion = None
    
    def connect(self) -> bool:
        """Connect to Reachy Mini."""
        try:
            if self.host:
                self.mini = ReachyMini(host=self.host)
            else:
                self.mini = ReachyMini()
            print(f"✓ Connected to Reachy Mini")
            return True
        except Exception as e:
            print(f"✗ Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from Reachy Mini."""
        if self.mini:
            self.mini = None
            print("Disconnected from Reachy Mini")
    
    def set_emotion(self, emotion: str) -> bool:
        """Set Reachy Mini's emotion.
        
        Args:
            emotion: One of: sleeping, idle, happy, working, thinking, 
                     surprised, sad, excited
        
        Returns:
            True if successful
        """
        if emotion not in EMOTIONS:
            print(f"Unknown emotion: {emotion}")
            return False
        
        if not self.mini:
            print("Not connected to Reachy Mini")
            return False
        
        config = EMOTIONS[emotion]
        head = config["head"]
        antenna_angle = config["antennas"]
        duration = config["duration"]
        
        try:
            # Special handling for thinking (asymmetric antennas)
            if emotion == "thinking":
                antennas = np.deg2rad([antenna_angle, antenna_angle - 20])
            else:
                antennas = np.deg2rad([antenna_angle, antenna_angle])
            
            # Move to emotion pose
            self.mini.goto_target(
                head=create_head_pose(
                    z=head["z"],
                    roll=head["roll"],
                    degrees=True,
                    mm=True
                ),
                antennas=antennas,
                duration=duration,
                method="minjerk"
            )
            
            self.current_emotion = emotion
            print(f"😊 Set emotion: {emotion}")
            
            # Run animation if defined
            if config.get("animation"):
                self._animate(config["animation"])
            
            return True
            
        except Exception as e:
            print(f"Error setting emotion: {e}")
            return False
    
    def _animate(self, animation: str):
        """Run a looping animation."""
        # Animations would run in background - simplified for now
        pass
    
    def wake_up(self):
        """Wake up sequence."""
        if not self.mini:
            return
        
        # Start sleeping
        self.set_emotion("sleeping")
        time.sleep(1)
        
        # Slowly wake
        self.mini.goto_target(
            head=create_head_pose(z=0, roll=0, degrees=True, mm=True),
            antennas=np.deg2rad([0, 0]),
            duration=1.5
        )
        time.sleep(0.5)
        
        # Alert and happy
        self.set_emotion("happy")
    
    def sleep(self):
        """Go to sleep sequence."""
        if not self.mini:
            return
        
        # Yawn (look up, stretch)
        self.mini.goto_target(
            head=create_head_pose(z=20, roll=0, degrees=True, mm=True),
            antennas=np.deg2rad([30, 30]),
            duration=1.0
        )
        time.sleep(0.8)
        
        # Settle into sleep
        self.set_emotion("sleeping")


def main():
    """Test the emotion controller."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Control Reachy Mini emotions")
    parser.add_argument("--host", help="Reachy Mini IP address")
    parser.add_argument("--emotion", default="idle", 
                        choices=list(EMOTIONS.keys()),
                        help="Emotion to display")
    parser.add_argument("--test", action="store_true",
                        help="Run through all emotions")
    args = parser.parse_args()
    
    clawd = ClawdEmotions(host=args.host)
    
    if not clawd.connect():
        sys.exit(1)
    
    try:
        if args.test:
            print("\n🎭 Testing all emotions...\n")
            for emotion in EMOTIONS:
                print(f"  → {emotion}")
                clawd.set_emotion(emotion)
                time.sleep(2)
            print("\n✓ Done!")
        else:
            clawd.set_emotion(args.emotion)
            time.sleep(2)
    
    finally:
        clawd.disconnect()


if __name__ == "__main__":
    main()
