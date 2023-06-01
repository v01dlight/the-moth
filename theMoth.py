#!/usr/bin/python
import discord
import logging
import os
import random
import re
import requests
from bs4 import BeautifulSoup
from discord import commands
from html2text import html2text

token = os.environ.get('MOTH_BOT_TOKEN')

intents = discord.Intents.default()
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

def soothcardembed(cardNum):
    # post the link to the card image matching that number (Discord should auto-embed the image)
    # post the link to the details page for that card. The <> wrapping on the URL prevents Discord from embedding a link preview (looks cleaner that way)
    cardNum = str(cardNum).zfill(2)
    s = requests.session()
    con = s.get(f'https://app.invisiblesunrpg.com/soothdeck/card-{cardNum}/')
    soup = BeautifulSoup(con.text).find('article')
    name = soup.find('h2').text
    meanings = ''.join(map(str, soup.find(string='Meanings:').find_parent('p').contents))
    meanings = html2text(meanings)
    embed = discord.Embed(
        title=name,
        description=f"[Card details](https://app.invisiblesunrpg.com/soothdeck/card-{cardNum}/)\n{meanings}"
    )
    embed.set_image(url=f"https://app.invisiblesunrpg.com/wpsite/wp-content/uploads/2018/04/{cardNum}.png")
    await ctx.respond(None, embed=embed)

def get_sooth_list():
    s = requests.session()
    con = s.get(f'https://app.invisiblesunrpg.com/soothdeck/')
    soup = BeautifulSoup(con.text).find('article')
    def li2kv(x):
        x = x.text.split('. ')
        return (x[1].lower(), {'name': x[1], 'num': x[0]})
    cards = dict(map(li2kv, soup.find_all('li')))
    return cards

SOOTH_DECK = get_sooth_list()

@bot.slash_command(name='sooth', description='Draw a random sooth card')
async def sooth(ctx):
    # generate a random number between 1 and 60, with leading zeros if needed
    cardNum = random.randint(1,60)
    return await ctx.respond(None, embed=soothcardembed(cardNum))

@bot.slash_command(name='char', description='Generate a random character')
async def char(ctx):
    # Using Suns Apart flux:
    flux = lambda x: ['', '*', '!'][len(x) - len(set(x))]
    ret = ['```']
    for s in ['CER', 'QUA', 'SOR']:
        d = [random.randint(1, 6) for _ in range(3)]
        ret.append(f"{s}: {sum(d):2}{flux(d):1} {' + '.join(map(str, d))}")
    ret.append(f' HP: {random.randint(1, 6):2}')
    ret.append(f"DoB: {random.choice(['Spring', 'Summer', 'Autumn', 'Winter'])} {random.randrange(1, 29)}")
    ret.append('```')
    return await ctx.respond('\n'.join(ret))

@bot.slash_command(name='save', description='Make a saving throw')
async def save(
        ctx,
        advantage: commands.Option(int, 'Use positive numbers for advantage, negative numbers for disadvantage.', required=False),
        stat: commands.Option(int, 'The value of the stat you are checking against.', required=False)
    ):
    adv  = advantage or 0
    # TODO: Add args
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
        return await ctx.respond(f'Critical Success! ({saves})')
    if save == 20:
        return await ctx.respond(f'Critical Fail! ({saves})')
    if stat:
        if save <= stat:
            return await ctx.respond(f'Success! ({saves})')
        return await ctx.respond(f'Fail! ({saves})')
    else:
        return await ctx.respond(f'Rolled: {saves}')

@bot.slash_command(name='debug', description='print context on localhost')
async def debug(ctx):
    logging.warning(vars(ctx))
    logging.warning(json.dumps(ctx.interaction.data))
    return await ctx.respond('[O_O]')

@bot.slash_command(name='roll', description='Roll dice. Defaults to a mundane die (d10 with 0).')
async def roll(ctx, dice=commands.Option(str, 'Use +[num] to add Invisible Sun MD. Use [num]d[sides] ... (+|-)[bonus] to roll arbitrary dice.', default='')):
    if not dice:
        # if it just told to roll, roll a standard mundane die
        res = random.randrange(10)
        return await ctx.respond(res)
    args = str(dice).split()
    try:

        # Invisible Sun roll
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
            return await ctx.respond(res)

        # Standard roll
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
            return await ctx.respond(f'{dice}: {res[0]}')
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
        return await ctx.respond(f'{dice}: {lhs} = {rhs}')
    except:
        return await ctx.respond(f'Invalid dice or bonus spec: {dice}.'
               '\nUse "/roll" to roll a single Invisible Sun die (mundane).'
               '\nTo add magic dice, use +[# of magic dice].'
               '\nFor other dice rolls, use the form [count]d[sides], +[bonus], or -[bonus]')

@bot.slash_command(name='getsooth', description='Get details of a given sooth card')
async def getsooth(ctx, card=commands.Option(str, 'Unique prefix to card name', default='')):
    if not card:
        deck = ', '.join(map(lambda c: c['name'], SOOTH_DECK.values()))
        return await ctx.respond(f'Cards:\n{deck}')
    keys = list(filter(lambda k: k.startswith(card.lower()), SOOTH_DECK))
    if len(keys) > 1:
        keys = list(map(lambda k: SOOTH_DECK[k]['name'], keys))
        keys = ', '.join(keys[0:-1]) + ' or ' + keys[-1]
        return await ctx.respond(f'Did you mean {keys}?')
    if len(keys):
        return await ctx.respond(None, embed=soothcardembed(ctx, SOOTH_DECK[keys[0]]['num']))
    return await ctx.respond('No matching sooth card!')

bot.run(token)
