#!/usr/bin/env python3
"""
Clawd State Manager - Updates Reachy Mini based on activity state.

States are written to a file and this daemon syncs them to the robot.
Can also be called directly to set state.

Usage:
    # Set state directly
    python clawd_state.py thinking
    python clawd_state.py working
    python clawd_state.py happy
    
    # Run as daemon (watches state file)
    python clawd_state.py --daemon
"""

import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime, timedelta

# Add project path
sys.path.insert(0, str(Path(__file__).parent))
from emotions_api import ReachyEmotions

STATE_FILE = Path("/home/wrenn/clawd/reachy/.clawd_state")
IDLE_TIMEOUT = 300  # 5 minutes of no activity -> sleeping

# State priority (higher = more important, won't be overridden)
STATE_PRIORITY = {
    "sleeping": 0,
    "idle": 1,
    "working": 2,
    "thinking": 3,
    "happy": 4,
    "sad": 4,
    "surprised": 5,
    "excited": 5,
}


def read_state() -> dict:
    """Read current state from file."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except:
            pass
    return {"emotion": "idle", "updated": datetime.now().isoformat()}


def write_state(emotion: str, message: str = None):
    """Write state to file."""
    state = {
        "emotion": emotion,
        "updated": datetime.now().isoformat(),
        "message": message,
    }
    STATE_FILE.write_text(json.dumps(state))
    return state


def set_emotion(emotion: str, message: str = None):
    """Set Clawd's emotion (updates file and robot)."""
    # Write to state file
    write_state(emotion, message)
    
    # Update robot
    reachy = ReachyEmotions()
    if reachy.is_connected():
        reachy.set_emotion(emotion)
        return True
    else:
        print("⚠️  Could not connect to Reachy Mini")
        return False


def run_daemon():
    """Run as daemon, watching state file and handling idle timeout."""
    print("🤖 Clawd State Daemon starting...")
    reachy = ReachyEmotions()
    
    if not reachy.is_connected():
        print("❌ Cannot connect to Reachy Mini!")
        sys.exit(1)
    
    print("✅ Connected to Reachy Mini")
    
    last_state = None
    last_activity = datetime.now()
    
    # Start idle
    reachy.set_emotion("idle")
    write_state("idle")
    
    while True:
        try:
            state = read_state()
            current_emotion = state.get("emotion", "idle")
            updated = datetime.fromisoformat(state.get("updated", datetime.now().isoformat()))
            
            # Check if state changed
            if current_emotion != last_state:
                print(f"🎭 State changed: {last_state} → {current_emotion}")
                reachy.set_emotion(current_emotion)
                last_state = current_emotion
                last_activity = datetime.now()
            
            # Check for idle timeout (go to sleep)
            if current_emotion not in ["sleeping"] and \
               (datetime.now() - updated) > timedelta(seconds=IDLE_TIMEOUT):
                print("😴 Idle timeout - going to sleep")
                reachy.set_emotion("sleeping")
                write_state("sleeping", "idle timeout")
                last_state = "sleeping"
            
            time.sleep(0.5)  # Poll every 500ms
            
        except KeyboardInterrupt:
            print("\n👋 Daemon stopping...")
            reachy.set_emotion("sleeping")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Clawd State Manager")
    parser.add_argument("emotion", nargs="?", 
                        choices=["sleeping", "idle", "happy", "working", 
                                "thinking", "surprised", "sad", "excited"],
                        help="Emotion to set")
    parser.add_argument("--daemon", "-d", action="store_true",
                        help="Run as daemon")
    parser.add_argument("--message", "-m", help="Optional message/context")
    args = parser.parse_args()
    
    if args.daemon:
        run_daemon()
    elif args.emotion:
        set_emotion(args.emotion, args.message)
    else:
        # Show current state
        state = read_state()
        print(f"Current state: {state}")


if __name__ == "__main__":
    main()
