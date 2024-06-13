#!/bin/bash
# this script is intended to automate replacing the bot process on a server with a new one if the bot code has been updated

if [ -z "$1" ]
then
        echo "[*] Usage    : $0 <token>"
exit 0
fi

apt update && apt install npm python3-pip

npm install pm2 -g && pm2 update

pip3 install -r requirements.txt

pm2 delete TheMoth_Discord-bot

pm2 start "MOTH_BOT_TOKEN=$1 python3 theMoth.py" --name TheMoth_Discord-bot

pm2 save --force
