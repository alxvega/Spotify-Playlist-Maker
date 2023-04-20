#!/bin/bash

# Start Xvfb and set the DISPLAY environment variable
Xvfb :99 -screen 0 1366x768x16 > /dev/null 2>&1 &
export DISPLAY=:99

# Execute the Python script with arguments
python3 -u spotify_playmaker.py "$@"