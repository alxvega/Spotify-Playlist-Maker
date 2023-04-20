#!/bin/bash

# Start Xvfb and set the DISPLAY environment variable
Xvfb :99 -screen 0 1366x768x16 > /dev/null 2>&1 &
export DISPLAY=:99

# Get email and password from environment variables
email="$EMAIL"
password="$PASSWORD"

# Execute the Python script with arguments and email/password
python3 -u spotify_playmaker.py "$@" --email "$email" --password "$password"
