#!/usr/bin/python

import discord
import random

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('?hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('?help'):
        await message.channel.send('Supported commands:\n?sooth - draws a random sooth card')
    
    if message.content.startswith('?sooth'):
        # https://app.invisiblesunrpg.com/soothdeck/card-01/
        # https://app.invisiblesunrpg.com/wpsite/wp-content/uploads/2018/04/02.png
        cardNum = str(random.randint(1,60)).zfill(2)
        await message.channel.send("https://app.invisiblesunrpg.com/wpsite/wp-content/uploads/2018/04/"+cardNum+".png")
        await message.channel.send("Details: <https://app.invisiblesunrpg.com/soothdeck/card-"+cardNum+"/>")

client.run('YOUR BOT TOKEN HERE')
