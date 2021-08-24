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
        # generate a random rumber between 1 and 60, with leading zeros if needed
        cardNum = str(random.randint(1,60)).zfill(2)
        # post the link to the card image matching that number (Discord should auto-embed the image)
        await message.channel.send("https://app.invisiblesunrpg.com/wpsite/wp-content/uploads/2018/04/"+cardNum+".png")
        # post the link to the details page for that card. The <> wrapping on the URL prevents Discord from embedding a link preview (looks cleaner that way)
        await message.channel.send("Details: <https://app.invisiblesunrpg.com/soothdeck/card-"+cardNum+"/>")

client.run('YOUR BOT TOKEN HERE')
