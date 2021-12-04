# the-moth
## Official bot of Satyrine's finest eatery... The Magniloquent Moth!

*Check us out at: https://themagniloquentmoth.blogspot.com*

### Features:

-can draw sooth cards

-can roll dice (thanks [xPMo](https://github.com/xPMo)!)

-can track flux for Invisible Sun dice (thanks [Baconaetor](https://github.com/Baconaetor)!)

### Usage:
-Add The Moth bot to your Discord server with this link:
https://discord.com/api/oauth2/authorize?client_id=879736921570557963&permissions=3072&scope=bot

-Make sure you grant the bot permissions to read and write messages in the channel(s) you want to use it in.

-type ```?help``` in a channel it can access and start exploring!

### Running Locally
You can either run this directly or through Docker. Either way, you'll
also need to create a bot token, which you can find instructions on
[https://www.writebots.com/discord-bot-token/](here).

To run directly, you'll need python3 and pip3 installed. Then you can run the following:

``` shell
pip3 install -r requirements.txt
MOTH_BOT_TOKEN=<your bot token> python3 theMoth.py
```

If you're interested in using docker, you can build and run using the following commands:

``` shell
docker build -t the-moth .
docker run -e MOTH_BOT_TOKEN=<your bot token> the-moth
```

### Credits:
Moth logo image by <a href="https://pixabay.com/users/nika_akin-13521770/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4658451">Nika Akin</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4658451">Pixabay</a>.
