#!/usr/bin/env python3
"""Reachy Mini emotion controller using REST API."""

import requests
import json
import time
import math
from typing import Optional, Dict, Any

REACHY_HOST = "192.168.4.75"
REACHY_PORT = 8000
BASE_URL = f"http://{REACHY_HOST}:{REACHY_PORT}"

# Emotion configurations
# head_pose: x, y, z (meters), roll, pitch, yaw (radians)
# antennas: [left, right] in radians (positive = up)

EMOTIONS = {
    "sleeping": {
        "head": {"z": -0.01, "roll": 0.1, "pitch": 0, "yaw": 0},
        "antennas": [-0.3, -0.3],
        "duration": 2.0,
    },
    "idle": {
        "head": {"z": 0, "roll": 0, "pitch": 0, "yaw": 0},
        "antennas": [0.3, 0.3],
        "duration": 1.0,
    },
    "happy": {
        "head": {"z": 0.015, "roll": 0, "pitch": 0, "yaw": 0},
        "antennas": [0.8, 0.8],
        "duration": 0.8,
    },
    "working": {
        "head": {"z": 0.005, "roll": -0.1, "pitch": 0, "yaw": 0},
        "antennas": [0.4, 0.4],
        "duration": 1.0,
    },
    "thinking": {
        "head": {"z": 0.01, "roll": 0.25, "pitch": 0, "yaw": 0.1},
        "antennas": [0.6, 0.2],  # Asymmetric!
        "duration": 1.2,
    },
    "surprised": {
        "head": {"z": 0.02, "roll": 0, "pitch": 0, "yaw": 0},
        "antennas": [1.0, 1.0],
        "duration": 0.3,
    },
    "sad": {
        "head": {"z": -0.015, "roll": 0, "pitch": 0.1, "yaw": 0},
        "antennas": [-0.5, -0.5],
        "duration": 1.5,
    },
    "excited": {
        "head": {"z": 0.01, "roll": 0, "pitch": 0, "yaw": 0},
        "antennas": [0.9, 0.9],
        "duration": 0.5,
    },
}


class ReachyEmotions:
    """Control Reachy Mini emotions via REST API."""
    
    def __init__(self, host: str = REACHY_HOST, port: int = REACHY_PORT):
        self.base_url = f"http://{host}:{port}"
        self.current_emotion = None
    
    def _api(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make API request."""
        url = f"{self.base_url}{endpoint}"
        try:
            if method == "GET":
                resp = requests.get(url, timeout=5)
            elif method == "POST":
                resp = requests.post(url, json=data, timeout=5)
            resp.raise_for_status()
            return resp.json() if resp.text else {}
        except Exception as e:
            print(f"API error: {e}")
            return {"error": str(e)}
    
    def get_state(self) -> Dict[str, Any]:
        """Get current robot state."""
        return self._api("GET", "/api/state/full")
    
    def is_connected(self) -> bool:
        """Check if robot is reachable."""
        state = self.get_state()
        return "error" not in state
    
    def wake_up(self) -> bool:
        """Play wake up animation."""
        result = self._api("POST", "/api/move/play/wake_up")
        return "error" not in result
    
    def go_to_sleep(self) -> bool:
        """Play sleep animation."""
        result = self._api("POST", "/api/move/play/goto_sleep")
        return "error" not in result
    
    def goto(self, head_pose: Dict, antennas: list, duration: float = 1.0) -> bool:
        """Move to target position.
        
        Args:
            head_pose: Dict with x, y, z (meters), roll, pitch, yaw (radians)
            antennas: [left, right] positions in radians
            duration: Movement duration in seconds
        """
        data = {
            "head_pose": {
                "x": head_pose.get("x", 0),
                "y": head_pose.get("y", 0),
                "z": head_pose.get("z", 0),
                "roll": head_pose.get("roll", 0),
                "pitch": head_pose.get("pitch", 0),
                "yaw": head_pose.get("yaw", 0),
            },
            "antennas_position": antennas,
            "duration": duration,
        }
        result = self._api("POST", "/api/move/goto", data)
        return "error" not in result
    
    def set_emotion(self, emotion: str) -> bool:
        """Set robot emotion.
        
        Args:
            emotion: One of: sleeping, idle, happy, working, thinking,
                     surprised, sad, excited
        """
        if emotion not in EMOTIONS:
            print(f"Unknown emotion: {emotion}")
            print(f"Available: {list(EMOTIONS.keys())}")
            return False
        
        config = EMOTIONS[emotion]
        success = self.goto(
            head_pose=config["head"],
            antennas=config["antennas"],
            duration=config["duration"]
        )
        
        if success:
            self.current_emotion = emotion
            print(f"🎭 Emotion: {emotion}")
        
        return success
    
    def nod_yes(self, times: int = 2) -> bool:
        """Nod head yes."""
        for _ in range(times):
            self.goto({"z": 0.015, "pitch": -0.2}, [0.3, 0.3], 0.3)
            time.sleep(0.35)
            self.goto({"z": -0.005, "pitch": 0.1}, [0.3, 0.3], 0.3)
            time.sleep(0.35)
        return self.set_emotion("idle")
    
    def shake_no(self, times: int = 2) -> bool:
        """Shake head no."""
        for _ in range(times):
            self.goto({"yaw": 0.3}, [0.3, 0.3], 0.25)
            time.sleep(0.3)
            self.goto({"yaw": -0.3}, [0.3, 0.3], 0.25)
            time.sleep(0.3)
        return self.set_emotion("idle")
    
    def look_at_user(self) -> bool:
        """Look towards user (assuming they're in front)."""
        return self.set_emotion("idle")
    
    def celebrate(self) -> bool:
        """Happy celebration animation."""
        self.set_emotion("excited")
        time.sleep(0.5)
        for _ in range(3):
            self.goto({"z": 0.02, "roll": 0.15}, [1.0, 1.0], 0.2)
            time.sleep(0.25)
            self.goto({"z": 0.02, "roll": -0.15}, [1.0, 1.0], 0.2)
            time.sleep(0.25)
        return self.set_emotion("happy")


def main():
    """Test emotions."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Reachy Mini Emotions")
    parser.add_argument("--emotion", "-e", choices=list(EMOTIONS.keys()),
                        help="Set emotion")
    parser.add_argument("--test", "-t", action="store_true",
                        help="Test all emotions")
    parser.add_argument("--wake", action="store_true", help="Wake up")
    parser.add_argument("--sleep", action="store_true", help="Go to sleep")
    parser.add_argument("--nod", action="store_true", help="Nod yes")
    parser.add_argument("--shake", action="store_true", help="Shake no")
    parser.add_argument("--celebrate", action="store_true", help="Celebrate!")
    args = parser.parse_args()
    
    reachy = ReachyEmotions()
    
    if not reachy.is_connected():
        print("❌ Cannot connect to Reachy Mini")
        return
    
    print("✅ Connected to Reachy Mini!")
    
    if args.wake:
        reachy.wake_up()
    elif args.sleep:
        reachy.go_to_sleep()
    elif args.nod:
        reachy.nod_yes()
    elif args.shake:
        reachy.shake_no()
    elif args.celebrate:
        reachy.celebrate()
    elif args.emotion:
        reachy.set_emotion(args.emotion)
    elif args.test:
        print("\n🎭 Testing all emotions...\n")
        for emotion in EMOTIONS:
            print(f"  → {emotion}")
            reachy.set_emotion(emotion)
            time.sleep(2.5)
        print("\n✓ Done!")
        reachy.set_emotion("idle")
    else:
        # Demo
        print("\nRunning demo...")
        reachy.wake_up()
        time.sleep(2)
        reachy.set_emotion("happy")
        time.sleep(2)
        reachy.set_emotion("thinking")
        time.sleep(2)
        reachy.set_emotion("idle")


if __name__ == "__main__":
    main()
