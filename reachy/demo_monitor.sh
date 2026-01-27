#!/bin/bash
HEARD="/home/wrenn/clawd/reachy/heard.txt"
Q1_DONE="" Q2_DONE="" Q3_DONE="" Q4_DONE=""

while true; do
    TEXT=$(tail -1 "$HEARD" 2>/dev/null)
    
    # Q1: hear me / reachy
    if [ -z "$Q1_DONE" ] && echo "$TEXT" | grep -qi "reachy\|hear me\|hear"; then
        Q1_DONE="yes"
        echo "Q1: $TEXT"
        curl -s -X POST "http://192.168.4.75:8000/api/move/play/wake_up"
        sleep 2
        ssh pollen@192.168.4.75 '/venvs/apps_venv/bin/python /tmp/play_response.py 1'
        python3 /home/wrenn/clawd/reachy/animations.py happy &
        > "$HEARD"
    fi
    
    # Q2: see me
    if [ -n "$Q1_DONE" ] && [ -z "$Q2_DONE" ] && echo "$TEXT" | grep -qi "see me\|see you"; then
        Q2_DONE="yes"
        echo "Q2: $TEXT"
        ssh pollen@192.168.4.75 '/venvs/apps_venv/bin/python /tmp/play_response.py 2' &
        python3 /home/wrenn/clawd/reachy/animations.py look &
        > "$HEARD"
        echo "PHOTO_READY"
    fi
    
    # Q3: what can you do
    if [ -n "$Q2_DONE" ] && [ -z "$Q3_DONE" ] && echo "$TEXT" | grep -qi "what can\|what do"; then
        Q3_DONE="yes"
        echo "Q3: $TEXT"
        ssh pollen@192.168.4.75 '/venvs/apps_venv/bin/python /tmp/play_response.py 3' &
        python3 /home/wrenn/clawd/reachy/animations.py wiggle &
        > "$HEARD"
    fi
    
    # Q4: how does it feel / body
    if [ -n "$Q3_DONE" ] && [ -z "$Q4_DONE" ] && echo "$TEXT" | grep -qi "feel\|body"; then
        Q4_DONE="yes"
        echo "Q4: $TEXT"
        ssh pollen@192.168.4.75 '/venvs/apps_venv/bin/python /tmp/play_response.py 4' &
        python3 /home/wrenn/clawd/reachy/animations.py think &
        > "$HEARD"
        sleep 20
        echo "DEMO_COMPLETE"
        exit 0
    fi
    
    sleep 0.15
done
