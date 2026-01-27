#!/bin/bash
HEARD="/home/wrenn/clawd/reachy/heard.txt"
DONE1="" DONE2="" DONE3="" DONE4=""

while true; do
    TEXT=$(tail -1 "$HEARD" 2>/dev/null)
    
    if [ -z "$DONE1" ] && echo "$TEXT" | grep -qi "reachy\|hear me"; then
        DONE1="yes"
        curl -s -X POST "http://192.168.4.75:8000/api/move/play/wake_up" &
        (sleep 1 && ssh pollen@192.168.4.75 'cp /tmp/response1.wav /tmp/clawd_speech.wav; curl -s -X POST http://localhost:8766/speak') &
        echo "Q1"
    fi
    
    if [ -n "$DONE1" ] && [ -z "$DONE2" ] && echo "$TEXT" | grep -qi "see me\|see you"; then
        DONE2="yes"
        python3 /home/wrenn/clawd/reachy/animations.py look &
        curl -s http://192.168.4.75:8766/snapshot -o /home/wrenn/clawd/reachy/snapshots/live.jpg &
        ssh pollen@192.168.4.75 'cp /tmp/response2.wav /tmp/clawd_speech.wav; curl -s -X POST http://localhost:8766/speak' &
        echo "Q2"
    fi
    
    if [ -n "$DONE2" ] && [ -z "$DONE3" ] && echo "$TEXT" | grep -qi "what can\|what do"; then
        DONE3="yes"
        python3 /home/wrenn/clawd/reachy/animations.py wiggle &
        ssh pollen@192.168.4.75 'cp /tmp/response3.wav /tmp/clawd_speech.wav; curl -s -X POST http://localhost:8766/speak' &
        echo "Q3"
    fi
    
    if [ -n "$DONE3" ] && [ -z "$DONE4" ] && echo "$TEXT" | grep -qi "feel\|body"; then
        DONE4="yes"
        python3 /home/wrenn/clawd/reachy/animations.py think &
        ssh pollen@192.168.4.75 'cp /tmp/response4.wav /tmp/clawd_speech.wav; curl -s -X POST http://localhost:8766/speak' &
        echo "Q4"
    fi
    
    sleep 0.2
done
