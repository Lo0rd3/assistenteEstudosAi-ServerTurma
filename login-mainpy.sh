#!/bin/bash
cd "$(getent passwd $(whoami) | cut -d: -f6)" 2>/dev/null || cd /
python3 /app/main.py
