#!/usr/bin/python

import discord
import random
import os
import re

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
        await message.channel.send('Supported commands:'
            '\n`?sooth` - draws a random sooth card'
            '\n`?char` - generates a Suns Apart character'
            '\n`?roll` - rolls dice and sums them.'
            '\n- Arguments of the form `(<num>)d<n>` are treated as `<num>` (or 1) dice, each with `<n>` sides. Add `[+-]<b>` to add a flat bonus'
            '\n- With no arguments, `?roll` will roll a mundane die from Invisible Sun.'
            '\n- With a +[number] argument it will roll a mundane die plus that many magic dice, e.g. `?roll +3`'
            '\n`?save` - rolls a d20 as a save.'
            '\n- Add arguments of the form `(<num>)a...` or `(<num>)d...` to roll at an advantage or disadvantage'
            '\n- Add an integer argument to automatically compare to a stat to determine success.'
            '\n- e.g.: `?save adv` to roll a save at advantage. `?save 2d 14` or `?save -2a 14` to roll a save at double advantage against a STAT of 14.'
            )

    if message.content.startswith('?sooth'):
        # generate a random number between 1 and 60, with leading zeros if needed
        cardNum = str(random.randint(1,60)).zfill(2)
        # post the link to the card image matching that number (Discord should auto-embed the image)
        await message.channel.send("https://app.invisiblesunrpg.com/wpsite/wp-content/uploads/2018/04/"+cardNum+".png")
        # post the link to the details page for that card. The <> wrapping on the URL prevents Discord from embedding a link preview (looks cleaner that way)
        return await message.channel.send("Details: <https://app.invisiblesunrpg.com/soothdeck/card-"+cardNum+"/>")

    if message.content.startswith('?char'):
        # Using Suns Apart flux:
        flux = lambda x: ['', '*', '!'][len(x) - len(set(x))]
        ret = ['```']
        for s in ['CER', 'QUA', 'SOR']:
            d = [random.randint(1, 6) for _ in range(3)]
            ret.append(f"{s}: {sum(d):2}{flux(d):1} {' + '.join(map(str, d))}")
        ret.append(f' HP: {random.randint(1, 6):2}')
        ret.append(f"DoB: {random.choice(['Spring', 'Summer', 'Autumn', 'Winter'])} {random.randrange(1, 29)}")
        ret.append('```')
        return await message.channel.send('\n'.join(ret))

    if message.content.startswith('?save'):
        args = message.content.split()[1:]
        adv  = 0
        stat = None
        for arg in args:
            m = re.match('^(-?\d*)([ad])', arg)
            if m:
                m = m.groups()
                if m[1] =='a':
                    adv += int(m[0] or 1)
                else:
                    adv -= int(m[0] or 1)
                continue
            try:
                newstat = int(arg)
                if stat is not None:
                    return await message.channel.send(f'Too many stat arguments: {stat} and {arg}.')
                stat = newstat
            except:
                return await message.channel.send(f'Invalid argument: {arg}')
        saves = [random.randint(1, 20) for _ in range(abs(adv) + 1)]

        if adv > 0:
            save = min(saves)
        else:
            save = max(saves)

        if adv:
            saves = ', '.join(map(str, saves)) + f': **{save}**'
        else:
            saves = f'**{save}**'

        if save == 1:
            return await message.channel.send(f'Critical Success! ({saves})')
        if save == 20:
            return await message.channel.send(f'Critical Fail! ({saves})')
        try:
            stat = int(message.content.split()[1])
            if save <= stat:
                return await message.channel.send(f'Success! ({saves})')
            return await message.channel.send(f'Fail! ({saves})')
        except:
            return await message.channel.send(f'Rolled: {saves}')

    if message.content.startswith('?roll'):
        # split into the dice groups we're rolling
        args = message.content.split()[1:]
        if not args:
            # if it just told to roll, roll a standard mundane die
            res = random.randrange(10)
            return await message.channel.send(res)
        try:
            if args[0].startswith('+'):
                if len(args) > 1: raise ValueError
                # if adding magic dice, roll the mundane die, then number of magic die
                count = int(args[0])
                res = "Mundane: " + str(random.randrange(10)) + '\n' + "Magic: "
                fluxcount = 0
                for _ in range(count -1):
                    roll = random.randrange(10)
                    res += str(roll) + " | "
                    if roll == 0: fluxcount += 1
                roll = random.randrange(10)
                res += str(roll)
                if roll == 0: fluxcount += 1
                if fluxcount > 0:
                    res += '\n'
                    if fluxcount == 1: res += "Minor "
                    if fluxcount == 2: res += "Major "
                    if fluxcount == 3: res += "Grand "
                    if fluxcount == 4: res += "Tetra-"
                    if fluxcount == 5: res += "Penta-"
                    if fluxcount == 6: res += "Hexa-"
                    if fluxcount == 7: res += "Hepta-"
                    if fluxcount == 8: res += "Octo-"
                    if fluxcount >= 9: res += "VISLA GAZES UPON YOU... how did you even do this? "
                    res += "Flux!"
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
        except:
            return await message.channel.send(f'Invalid dice or bonus spec: {message.content}.'
                   ' Use "?roll" to roll a single Invisible Sun die (mundane).'
                   ' To add magic dice, use +[# of magic dice].'
                   ' For other dice rolls, use the form [count]d[sides], +[bonus], or -[bonus]')

client.run(os.environ.get('MOTH_BOT_TOKEN'))
