# Natsuki Bot

## Installation

1. Clone the repository or download the source directly and put it into a folder with nothing else inside.
2. Create and fill these files:
- `botToken.py`
- `longterm_lists.json`
3. If you run this via termux, you **have** to run these commands in this order:
    
    `pkg install python pip`

    `pkg install binutil`

    `pkg install python-tkinter`

    `pkg install clang python libffi openssl libsodium`

    `SODIUM_INSTALL=system pip install pynacl`

    Please make sure to go into `settings.py` and change `is_phone` to `True`

4. Using Command Prompt, go to the bot directory and run the following command:
	
    `pip install -r requirements.txt`
	
    This should install the modules required to run the bot.

5. Set up the environment (Guaranteed to work in Python 3.12.3)
6. Edit the bot (More information below)
7. Run the bot

**What you will put into each file:**
`botToken.py`
```py
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
        "Put your own User ID here. This is used for Administrators who can use commands like adding and removing people from the blacklist.",
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

## Images / ASCII Art

When starting the bot, you may see ASCII image art. You can remove this by setting `enable_ascii` to `False` inside `settings.py`.

Similarly, you can add more art by following the JSON file format, and adding your own ASCII art. The JSON is stuctured as follows:

| `"logo"` (This is just the logo. It has no additional properties apart from `"logo"`)

| `"natsukis"` (This is an array of Objects - the images and their IDs.)

| | Object (Because the objects do not have specific names, this stand-in name is used.)

| | `"id"` (This is the **id**entifier property, which is useful for debugging in case a printed ASCII art is incorrectly displayed.)

| | `"image"` (This is the property where the ASCII art is stored. To display the ASCII, this property is called.)

An easy way to check ASCII art is to create a Python file that prints the ASCII, then opening the Python file inside Command Prompt.

*Compatibility with the anything but the Windows 10 Command Prompt is **not** guaranteed!*

### Important: The ASCII art must **only** use UTF-8 characters!
It will not work otherwise.

If you wish to add your own ASCII art to the examples, open a suggestion issue, credit the original artist, and provide a screenshot of your console running either the bot or another program to display the ASCII art.

Generally, keep its width to ~64 characters.

## Music

The Music function is kinda buggy and still worked on.

**Playlists do not work!** If you send the link to a playlist, it will only play the selected song. If you can fix this issue, please contact me and I will add your fix and add you to the credits!

If the bot starts acting up, examples include showing the wrong title, length, or thumbnail, you will have to restart the bot. That means the queue messed up and will inevitably start playing the wrong songs. Avoid requesting songs at the same time.

The Playlist command is slightly bugged, sometimes not showing the correct songs, or showing the song that is currently playing.

The skip command *should* work.

Please be aware that this is a rudimentary solution to play YT stuff after all big bots removed the feature for an immature reason. (But hey, while you cannot play YouTube videos or get support for playing them, at least you can be a child predator on Discord without facing any problems! Some of the Discord Administrators even are some!)

If you use the music modules, beware that the bot cannot play things that are blocked in your country. From my testing, it ~~can~~ **CAN NOT** play age-restricted videos. You might be able to bypass it, but I do not know how. You **can** bypass country restrictions by using a VPN however.

If you use a Server, you will have to run the Server with a VPN. This way, you bypass most country restrictions.

## Dev notes

This isn't part of the "documentation". Just want to thank you for using the bot! I've worked on it for a few years already and although it made me age like 20 years through the suffering of trying to get the music stuff working, it's fun. Have fun with the bot \^-\^
