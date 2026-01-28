#!/usr/bin/env python3
import sys
sys.path.insert(0, '/venvs/apps_venv/lib/python3.12/site-packages')
from flask import Flask, send_file, jsonify
from reachy_mini import ReachyMini
import subprocess

app = Flask(__name__)
robot = ReachyMini(media_backend="default")

@app.route('/')
def index():
    return jsonify({"status": "ok", "service": "Clawd App"})

@app.route('/snapshot')
def snapshot():
    img = robot.media.get_frame()
    import cv2, io
    _, buf = cv2.imencode('.jpg', img)
    return send_file(io.BytesIO(buf.tobytes()), mimetype='image/jpeg')

@app.route('/speak', methods=['POST'])
def speak():
    subprocess.run(['paplay', '/tmp/clawd_speech.wav'], capture_output=True)
    return jsonify({"status": "ok", "played": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8766)
