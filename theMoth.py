#!/usr/bin/python
import discord
import logging
import os
import random
import requests
import sqlite3
from bs4 import BeautifulSoup
from discord import commands
from html2text import html2text
from datetime import datetime, timedelta
import asyncio

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

BS = lambda text: BeautifulSoup(text, 'html.parser')

class SoothCard:
    def __init__(self, soup):
        self.url = soup.find('a')['href']
        self.num, self.name = soup.text.split('. ')

    def embed(self):
        znum = str(self.num).zfill(2)

        if not hasattr(self, 'soup'):
            s = requests.session()
            con = s.get(self.url)
            self.soup = BS(con.text).find('article')
            self.flavor = self.soup.find('p', {'class': 'flavor'}).text
            self.meanings = self.soup.find(string='Meanings:').find_parent('p').contents[1]

        embed = discord.Embed(
            title=self.name,
            description=self.meanings,
            url=self.url
        )
        embed.set_footer(text=self.flavor)
        embed.set_image(url=f"https://app.invisiblesunrpg.com/wpsite/wp-content/uploads/2018/04/{znum}.png")
        return embed

def get_sooth_list():
    s = requests.session()
    con = s.get(f'https://app.invisiblesunrpg.com/soothdeck/')
    soup = BS(con.text).find('article')

    by_name = dict()
    by_num = dict()

    for li in soup.find_all('li'):
        card = SoothCard(li)
        by_num[int(card.num)] = card
        by_name[card.name.lower()] = card

    return (by_name, by_num)

DECK_BY_NAME, DECK_BY_NUM = get_sooth_list()
logging.info(f'Loaded {len(DECK_BY_NAME)} cards into Sooth Deck')

def sooth_prefix_match(prefix):
    return [card for name, card in DECK_BY_NAME.items() if any(s.startswith(prefix.lower()) for s in [name, *name.split()])]

def sooth_complete(ctx: discord.AutocompleteContext):
    cards = sooth_prefix_match(ctx.value)
    return [card.name for card in cards]

## Bot

token = os.environ.get('MOTH_BOT_TOKEN')
intents = discord.Intents.default()
bot = discord.Bot()

# ----------------------
# Timer Database Helpers
# ----------------------

DB_FILE = "timers.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS timers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  channel_id INTEGER,
                  name TEXT,
                  end_time TEXT)''')
    conn.commit()
    conn.close()

async def timer_watcher():
    await bot.wait_until_ready()
    while not bot.is_closed():
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        now = datetime.utcnow()
        c.execute("SELECT id, user_id, channel_id, name, end_time FROM timers")
        rows = c.fetchall()
        for row in rows:
            tid, user_id, channel_id, name, end_time = row
            end_time = datetime.fromisoformat(end_time)
            if now >= end_time:
                logging.info(f"Timer {name} (id={tid}) expired, sending notification...")
                channel = bot.get_channel(channel_id)
                if channel:
                    try:
                        await channel.send(f"<@{user_id}>, timer complete: **{name}**")
                    except Exception as e:
                        logging.error(f"Failed to send message for timer {tid}: {e}")
                c.execute("DELETE FROM timers WHERE id = ?", (tid,))
        conn.commit()
        conn.close()
        await asyncio.sleep(30)

init_db()

# ----------------------
# Timer Commands
# ----------------------

from discord.commands import SlashCommandGroup
timer = SlashCommandGroup("timer", "Manage timers")

def parse_duration(duration: str) -> timedelta:
    """Parse strings like '3d', '5h', '2w', '10m' into timedelta."""
    units = {"d": "days", "h": "hours", "m": "minutes", "w": "weeks"}
    amount = int(''.join([c for c in duration if c.isdigit()]))
    unit = ''.join([c for c in duration if c.isalpha()])
    if unit not in units:
        raise ValueError("Invalid unit (use d, h, m, w)")
    return timedelta(**{units[unit]: amount})

@timer.command(name="set", description="Set a new timer")
async def timer_set(ctx, duration: str, *, name: str):
    try:
        delta = parse_duration(duration)
    except Exception as e:
        return await ctx.respond(f"Error parsing duration: {e}")

    end_time = datetime.utcnow() + delta
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO timers (user_id, channel_id, name, end_time) VALUES (?, ?, ?, ?)",
              (ctx.author.id, ctx.channel.id, name, end_time.isoformat()))
    conn.commit()
    conn.close()
    await ctx.respond(f"Timer **{name}** set for {duration} from now.")

@timer.command(name="list", description="List active timers")
async def timer_list(ctx):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, end_time FROM timers WHERE user_id = ?", (ctx.author.id,))
    rows = c.fetchall()
    conn.close()
    if not rows:
        return await ctx.respond("You have no active timers.")
    msg = "Your timers:\n"
    for i, (tid, name, end_time) in enumerate(rows, start=1):
        remaining = datetime.fromisoformat(end_time) - datetime.utcnow()
        mins, secs = divmod(int(remaining.total_seconds()), 60)
        hrs, mins = divmod(mins, 60)
        days, hrs = divmod(hrs, 24)
        msg += f"{i}. **{name}** - {days}d {hrs}h {mins}m {secs}s remaining\n"
    await ctx.respond(msg)

@timer.command(name="cancel", description="Cancel a timer by number (from /timer list)")
async def timer_cancel(ctx, number: int):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id FROM timers WHERE user_id = ?", (ctx.author.id,))
    rows = c.fetchall()
    if number < 1 or number > len(rows):
        conn.close()
        return await ctx.respond("Invalid timer number.")
    tid = rows[number - 1][0]
    c.execute("DELETE FROM timers WHERE id = ?", (tid,))
    conn.commit()
    conn.close()
    await ctx.respond(f"Cancelled timer #{number}.")

bot.add_application_command(timer)

@bot.event
async def on_ready():
    logging.info(f'We have logged in as {bot.user}')
    if not hasattr(bot, "watcher_started"):
        bot.loop.create_task(timer_watcher())
        bot.watcher_started = True

# ----------------------
# Sooth Commands
# ----------------------

@bot.slash_command(name='sooth', description='Draw a random sooth card')
async def sooth(ctx):
    card = DECK_BY_NUM[random.randint(1,60)]
    logging.info(f'Drew card {card.num}: {card.name}')
    return await ctx.respond(None, embed=card.embed())

@bot.slash_command(name='getsooth', description='Get details of a given sooth card')
async def getsooth(ctx, prefix=commands.Option(str, 'Card name or unique prefix', name='card', autocomplete=sooth_complete, default='')):
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

    cards = sooth_prefix_match(prefix)

    if len(cards) > 1:
        cards = list(map(lambda c: c.name, cards))
        cards = ', '.join(cards[0:-1]) + ' or ' + cards[-1]
        logging.info(f'Matched prefix \"{prefix}\" to cards \"{cards}\"')
        return await ctx.respond(f'Did you mean {cards}?')

    if len(cards):
        logging.info(f'Matched prefix \"{prefix}\" to card \"{cards[0].name}\"')
        return await ctx.respond(None, embed=cards[0].embed())

    logging.info(f'Could not match \"{prefix}\"')
    return await ctx.respond('No matching sooth card!')

# ----------------------
# Character Generation
# ----------------------

@bot.slash_command(name='char', description='Generate a random character')
async def char(ctx):
    # Using Suns Apart flux (marking multiples):
    flux = lambda x: ['', '*', '!'][len(x) - len(set(x))]
    ret = ['```']
    for s in ['BODY', 'MIND', 'SOUL']:
        d = [random.randint(1, 6) for _ in range(3)]
        ret.append(f"{s}: {sum(d):2}{flux(d):1} {' + '.join(map(str, d))}")
    ret.append(f'  GD: {random.randint(1, 6):2}')
    ret.append(f"DoB: {random.choice(['Spring', 'Summer', 'Autumn', 'Winter'])} {random.randrange(1, 29)}")
    ret.append('```')
    return await ctx.respond('\n'.join(ret))

# ----------------------
# Roll Commands
# ----------------------

@bot.slash_command(name='save', description='Make a saving throw')
async def save(ctx,
        advantage: commands.Option(int, 'Use positive numbers for advantage, negative numbers for disadvantage.', required=False), # type: ignore
        stat: commands.Option(int, 'The value of the stat you are checking against.', required=False)): # type: ignore
    adv  = advantage or 0
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
