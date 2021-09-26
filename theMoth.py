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
        await message.channel.send('Supported commands:\n?sooth - draws a random sooth card\n?roll - rolls dice, eg ?roll 2d6 or ?roll d20 +5')

    if message.content.startswith('?sooth'):
        # generate a random number between 1 and 60, with leading zeros if needed
        cardNum = str(random.randint(1,60)).zfill(2)
        # post the link to the card image matching that number (Discord should auto-embed the image)
        await message.channel.send("https://app.invisiblesunrpg.com/wpsite/wp-content/uploads/2018/04/"+cardNum+".png")
        # post the link to the details page for that card. The <> wrapping on the URL prevents Discord from embedding a link preview (looks cleaner that way)
        await message.channel.send("Details: <https://app.invisiblesunrpg.com/soothdeck/card-"+cardNum+"/>")

    if message.content.startswith('?roll'):
        # split into the dice groups we're rolling
        args = message.content.split()[1:]
        if not args:
            # if it just told to roll, roll a standard mundane die
            res = random.randrange(10)
            return await message.channel.send(res)
        try:
            if len(args) < 2:
                # if only passed a number, roll the mundane die, then magic die
                count = int(args[0]) - 1
                res = "Mundane Die: " + str(random.randrange(10))
                for _ in range(count):
                    res += " Magic Die: " + str(random.randrange(10))
                return await message.channel.send(res)
            res = []
            bonus = 0
            for arg in args:
                if arg[0] in ['+', '-']:
                    # bonus modifier
                    bonus += int(arg)
                    continue
                count, sides = arg.split('d')
                sides = int(sides)
                count = int(count or 1)
                res += [1 + random.randrange(sides) for _ in range(count)]
            if len(res) < 2 and not bonus:
                # only rolled one die, just post its roll
                return await message.channel.send(str(res[0]))
            # rhs: total sum
            rhs = sum(res) + bonus
            # lhs: dice rolls joined by '+'
            lhs = '+'.join(map(str, res))
            # add bonus to lhs string
            if bonus > 0:
                lhs += f'+{bonus}'
            elif bonus < 0:
                lhs += f'{bonus}'
            # post the final message, e.g.: "4+3+1 = 8"
            return await message.channel.send(f'{lhs} = {rhs}')
        except ValueError:
            return await message.channel.send(f'Invalid dice or bonus spec: {arg}. Use /"?roll/" to roll a single Invisible Sun die. (Mundane) To add magic die, just include the total number of dice. (Including Mundane) For other dice rolls, use the form [count]d[sides], +[bonus], or -[bonus]')

client.run('YOUR BOT TOKEN HERE')
