# Natsuki Bot

## Installation

1. Clone the repository or download the source directly and put it into a folder with nothing else inside.
2. Create and fill two files:
- `botToken.py`
- `longterm_lists.json`
3. (Optional) Using Command Prompt, go to the bot directory and run the following command:
	`$ pip install -r requirements.txt`
	This should install the modules required to run the bot.
4. Set up the environment (Guaranteed to work in Python 3.11.3)
5. Edit the bot (More information below)
6. Run the bot

**What you will put into each file:**
`botToken.py`
```python
botToken = "your.bot.token"
```
To get your Bot Token:
1. Go to the [Discord Developer Portal](https://discordapp.com/developers/applications/)
2. Give Your Bot a Name
3. Go into the **Bot** menu
4. Press **Add Bot**
5. Press **Click to Reveal Token** and voilà you have your Bot Token.

**Do not share your Bot Token!**  

`longterm_lists.json`
```json
{
    "true_natsukians": [
        "YOUR_USER_ID"
    ],
    "blacklist": [],
    "whitelist": []
}
```
That's all for this file. It may be replaced with an optional globally shared blacklist one day.

## Edit the Bot

You will have to edit the bot, otherwise several commands will be bugged and not work. To find what you have to edit:
1. Use the Search function for the word `EDIT`
2. Follow the steps provided

Alternatively you can comment out (or remove) commands you don't need/want. For documentation on DiscordPy, please head over to the [Official Discord.py Documentaton](https://discordpy.readthedocs.io/en/stable/api.html)
## Reporting Bugs

If it is related to the bot itself, please search if your issue is solved or open, if not then please open an issue on GitHub.
If you want your Users to be able to send you bug reports, they can use the command `/bug_report` if you set it up. You can also disable this command, or use it as a rudimentary non-anonymous reporting tool.

## Supporting the Bot

If you have improvements for the bot, feel free to contact me on Discord or GitHub. We can discuss the changes and fixes. If these changes/fixes are added to the official bot, you will be credited.

Please refrain from contact me if you are planning to add your political, religious, or other ideological things to the bot. Your changes may be considered, but this chance is lowered if you add politics, religion, or similar. Clean up the code and then you will be good to go.

*If you decide to make a bot like that derived from this bot, I kindly request you to not use the Natsuki name or imagery with it.*

## Music

The Music function is kinda buggy and still worked on.

If the bot starts acting up, examples include showing the wrong title, length, or thumbnail, you will have to restart the bot.
That means the queue messed up and will inevitably start playing the wrong songs. Avoid requesting songs at the same time.
Queue command is slightly bugged, sometimes not showing the correct songs, or showing the song that is currently playing. The skip command *should* work.
Please be aware that this is a rudimentary solution to play YT stuff after all big bots removed the feature.

If you use the music modules, beware that the bot cannot play things that are blocked in your country. From my brief testing, it can play age-restricted videos.

## Dev notes

This isn't part of the "documentation". Just want to thank you for using the bot! I've worked on it for a few years already and although it made me age like 20 years through the suffering of trying to get the music stuff working, it's fun. Have fun with the bot \^-\^
