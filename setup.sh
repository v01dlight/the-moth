#!/bin/bash
# this script is intended to automate replacing the bot process on a server with a new one if the bot code has been updated

set -e

if [ -z "$1" ]
then
    echo "[*] Usage: $0 <token>"
    exit 1
fi

# Create venv only if missing
if [ ! -d "venv" ]
then
    python3 -m venv venv
fi

source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

npm install -g pm2

pm2 delete TheMoth_Discord-bot || true

pm2 start \
    "MOTH_BOT_TOKEN=$1 venv/bin/python theMoth.py" \
    --name TheMoth_Discord-bot

pm2 save --force
