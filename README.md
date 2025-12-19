# the-moth

## Official bot of Satyrine's finest eatery... The Magniloquent Moth!

*Check us out at: https://themagniloquentmoth.blogspot.com*

## Features:

- supports slash commands (thanks [xPMo](https://github.com/xPMo)!)
- can draw sooth cards
- can roll dice (thanks [xPMo](https://github.com/xPMo)!)
- can track flux for Invisible Sun dice (thanks [Baconaetor](https://github.com/Baconaetor)!)
- can roll saves and generate character stats for Suns Apart (thanks again [xPMo](https://github.com/xPMo)!)
- Docker support (thanks [lackita](https://github.com/lackita)!)
- can track timers (helpful for tracking real-time downtime actions in West Marches games)

## Adding to Discord
- Add The Moth bot to your Discord server with
[this link](https://discord.com/api/oauth2/authorize?client_id=879736921570557963&permissions=3072&scope=bot).
- Make sure you grant the bot permissions to read and write messages in the channel(s) you want to use it in.
- type `/` in a channel it can access and start exploring!

## Bot Commands
### Timer Commands

All timer commands are under the `/timer` group.

#### `/timer set <duration> <name>`
Set a new personal timer.  
- **duration**: Time until the timer expires. Use formats like `10m` (minutes), `3h` (hours), `2d` (days), or `1w` (weeks).  
- **name**: Name of the timer.  

**Example:**  
```

/timer set duration: 1d name: Cooking pie

```

#### `/timer list`
List all your active timers with remaining time.  

#### `/timer cancel <number>`
Cancel a timer by the number listed in `/timer list`.  

**Example:**  
```

/timer cancel number: 2

```

---

### Sooth Commands

#### `/sooth`
Draw a random Sooth card from the Invisible Sun deck. Returns an embedded message with the card image, meaning, and flavor text.  

#### `/getsooth <card>`
Get details about a specific Sooth card. Supports unique prefixes for autocomplete. If multiple matches are found, the bot will suggest possible cards.  
- **card**: The name or prefix of the card.  

**Examples:**  
```

/getsooth
[returns list of all cards]

/getsooth card: Revealing
[returns the Revealing Knife]

/getsooth card: En
[Returns "Did you mean Endless Maze, Enticing Jewel, Endless Woods or Enveloping Darkness?"]

```

---

### Character Generation

#### `/char`
Generate a random character.
- **BODY**, **MIND**, **SOUL**: core stats
- **GD**: Guard, ability to avoid harm in combat
- **DoB**: season (same as month in my setting) and day of birth

**Example:**  
```

/char
[returns something like:]
BODY:  6  2 + 3 + 1
MIND: 10* 4 + 3 + 3
SOUL: 11* 4 + 4 + 3
  GD:  2
DoB: Summer 24

```

---

### NPC Generation

#### `/npc <npc_type> <number>`
Generate a random NPC from a set of name and detail tables (currently drawn from [The Monster Overhaul](https://coinsandscrolls.blogspot.com/2023/02/osr-monster-overhaul-megapost.html), which you should pick up because it's excellent).
- `npc_type`: currently either peasant, or townsfolk for more well-to-do NPCs
- `number`: defaults to 1, but allows generating up to 50 NPCs at once

**Example:**  
```

/npc npc_type: peasant
[returns something like:]
Mariota - Angular, asymmetrical chin

/npc npc_type: townsfolk number: 5
[returns something like:]
1. Huget Scobie
2. Stephen Rosny
3. Isolda Chepstow
4. Gilbert Oggerham
5. Avice Bedrule

```

---

### Dice and Saving Throws

#### `/roll [dice]`
Rolls dice! Supports several formats, both for *Invisible Sun* and *Suns Apart*/*Age of Iron*:
- Default: rolls a single mundane die (d10).  
- `+[num]`: Roll that many Invisible Sun magic dice.  
- `[count]d[sides]`: Roll arbitrary dice (only one die size at a time).  
- `+/-[bonus]`: Apply a bonus or penalty.  

**Examples:**  
```

/roll                  # rolls 1 mundane die (d10)
/roll dice: +3         # rolls a mundane die and 3 magic dice
/roll dice: 2d6 +3     # rolls 2 six-sided dice plus 3
/roll dice: 4d8 -1     # rolls 4 eight-sided dice minus 1

```

#### `/save [advantage] [stat]`
Make a saving throw.  
- **advantage**: Positive for advantage, negative for disadvantage.  
- **stat**: The value of the stat you are checking against.  

**Examples:**  
```

/save                              # rolls a single d20
/save advantage: 1 stat: 12        # rolls with advantage against stat 12
/save advantage: -2 stat: 15       # rolls with double disadvantage against stat 15

```

---

## Installation
### Running Locally
You can either run this directly or through Docker. Either way, you'll
also need to create a bot token, which you can find instructions on
[here](https://www.writebots.com/discord-bot-token/).

To run directly, you'll need python3 and pip3 installed. Then you can run the following:

``` shell
pip3 install -r requirements.txt
MOTH_BOT_TOKEN=$your_bot_token python3 theMoth.py
```

If you're interested in using docker, you can build and run using the following commands:

``` shell
docker build -t the-moth .
docker run -e MOTH_BOT_TOKEN=$your_bot_token the-moth
```

### Running on a Remote Server
For the "official" instance of the bot, I pay for a cloud server and I run it off that with [pm2](https://www.npmjs.com/package/pm2) to ensure that the bot process stays alive with no downtime. Since I was constantly forgetting how to update the production instance of the bot after making code changes, I created a setup script which automates the process of updating some tooling and replacing the running bot process with a fresh one. So for me, the way I would run this is:

``` shell
ssh root@$my_server_ip
git clone https://github.com/v01dlight/the-moth.git
cd the-moth
chmod +x setup.sh
./setup.sh "$my_bot_token"
```

### Credits:
Moth logo image by <a href="https://pixabay.com/users/nika_akin-13521770/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4658451">Nika Akin</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4658451">Pixabay</a>.
