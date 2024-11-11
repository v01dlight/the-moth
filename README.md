# the-moth

## Official bot of Satyrine's finest eatery... The Magniloquent Moth!

*Check us out at: https://themagniloquentmoth.blogspot.com*

### Features:

- supports slash commands (thanks [xPMo](https://github.com/xPMo)!)
- can draw sooth cards
- can roll dice (thanks [xPMo](https://github.com/xPMo)!)
- can track flux for Invisible Sun dice (thanks [Baconaetor](https://github.com/Baconaetor)!)
- can roll saves and generate character stats for Suns Apart (thanks again [xPMo](https://github.com/xPMo)!)
- Docker support (thanks [lackita](https://github.com/lackita)!)

### Usage:
- Add The Moth bot to your Discord server with
[this link](https://discord.com/api/oauth2/authorize?client_id=879736921570557963&permissions=3072&scope=bot).
- Make sure you grant the bot permissions to read and write messages in the channel(s) you want to use it in.
- type `/` in a channel it can access and start exploring!

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

### Adding Game Information

It would be copyright infringement to add extensive game information to this repository, but logic to parse a file is fair game. MCG was kind enough to provide a searchable text file to backers, and if the bot is informed of that file additional commands become available. You would specify that file in the following way:

```shell
python theMoth.py --searchable_text_file /path/to/file.txt
```

### Running Unit Tests

This codebase contains some unit tests, which can be executed by running the following command from the base directory:

```shell
python -m unittest discover
```

### Credits:
Moth logo image by <a href="https://pixabay.com/users/nika_akin-13521770/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4658451">Nika Akin</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4658451">Pixabay</a>.
