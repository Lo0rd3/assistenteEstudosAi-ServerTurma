#!/bin/bash
# Start SSH
/usr/sbin/sshd
# Start Flask
export FLASK_APP=webfiles.py
export FLASK_RUN_PORT=8080
export FLASK_RUN_HOST=0.0.0.0
python3 webfiles.py
