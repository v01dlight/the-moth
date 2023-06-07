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
    logging.info(f'We have logged in as {bot.user}')

def get_sooth_list():
    s = requests.session()
    con = s.get(f'https://app.invisiblesunrpg.com/soothdeck/')
    soup = BeautifulSoup(con.text).find('article')

    by_name = dict()
    by_num = dict()

    for li in soup.find_all('li'):
        card = SoothCard(li)
        by_num[int(card.num)] = card
        by_name[card.name.lower()] = card

    return (by_name, by_num)

class SoothCard:
    def __init__(self, soup):
        self.link = soup.find('a')['href']
        self.num, self.name = soup.text.split('. ')

    def embed(self):
        znum = str(self.num).zfill(2)

        # cache results in object
        if not hasattr(self, 'soup'):
            s = requests.session()
            con = s.get(f'https://app.invisiblesunrpg.com/soothdeck/card-{znum}/')
            self.soup = BeautifulSoup(con.text).find('article')
            self.flavor = self.soup.find('p', {'class': 'flavor'}).text
            self.meanings = self.soup.find(string='Meanings:').find_parent('p').contents[1]

        embed = discord.Embed(
            title=self.name,
            description=self.meanings,
            url=f'https://app.invisiblesunrpg.com/soothdeck/card-{znum}/'
        )
        embed.set_footer(text=self.flavor)
        embed.set_image(url=f"https://app.invisiblesunrpg.com/wpsite/wp-content/uploads/2018/04/{znum}.png")
        return embed

    def mdlink(self):
        return f'[{self.num}. {self.name}]({self.link})'


DECK_BY_NAME, DECK_BY_NUM = get_sooth_list()

@bot.slash_command(name='sooth', description='Draw a random sooth card')
async def sooth(ctx):
    return await ctx.respond(None, embed=DECK_BY_NUM[random.randint(1,60)].embed())

@bot.slash_command(name='getsooth', description='Get details of a given sooth card')
async def getsooth(ctx, prefix=commands.Option(str, 'Unique prefix to card name', default='')):
    if not prefix:
        embed = discord.Embed(
            title='Sooth Deck',
            url="https://app.invisiblesunrpg.com/soothdeck"
        )
        idx = 1
        for family in ['Secrets', 'Visions', 'Mysteries', 'Notions']:
            embed.add_field(name=family, value='\n'.join(f'{i}. {DECK_BY_NUM[i].name}' for i in range(idx, idx + 15)))
            idx += 15
        return await ctx.respond(None, embed=embed)
    cards = [card for name, card in DECK_BY_NAME.items() if name.startswith(prefix.lower())]
    if len(cards) > 1:
        cards = list(map(lambda c: c.name, cards))
        cards = ', '.join(cards[0:-1]) + ' or ' + cards[-1]
        return await ctx.respond(f'Did you mean {cards}?')
    if len(cards):
        return await ctx.respond(None, embed=cards[0].embed())
    return await ctx.respond('No matching sooth card!')

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


bot.run(token)
