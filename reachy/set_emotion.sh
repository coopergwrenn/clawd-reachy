#!/bin/bash
# Quick emotion setter for Clawd's Reachy Mini
# Usage: ./set_emotion.sh <emotion>
# Emotions: sleeping, idle, happy, working, thinking, surprised, sad, excited

EMOTION="${1:-idle}"
cd /home/wrenn/clawd/reachy
python3 emotions_api.py --emotion "$EMOTION"
