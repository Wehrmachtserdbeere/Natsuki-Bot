<!-- markdownlint-disable no-inline-html no-trailing-punctuation -->

# Natsuki Bot

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

Table of Content

- [Natsuki Bot](#natsuki-bot)
  - [Installation](#installation)
    - [**What you will put into each file:**](#what-you-will-put-into-each-file)
      - [`longterm_lists.json`](#longterm_listsjson)
      - [`twitter_embedder_settings.json`](#twitter_embedder_settingsjson)
      - [`.env`](#env)
  - [Edit the Bot](#edit-the-bot)
  - [Reporting Bugs](#reporting-bugs)
  - [Supporting the Bot](#supporting-the-bot)
  - [Images and ASCII Art](#images-and-ascii-art)
    - [**Contributing ASCII Art to Examples**](#contributing-ascii-art-to-examples)
  - [Music](#music)
    - [**Playlists do not work!**](#playlists-do-not-work)
  - [Termux Notes](#termux-notes)
  - [Dev Notes](#dev-notes)

<!-- TOC end -->

## Installation

1. Clone the repository or download the source directly and put it into a folder with nothing else inside.
2. Create and fill these files (if they do not exist yet):
   - `longterm_lists.json`
   - `.env`
3. If you run this via Termux, you **must** run these commands in this order:

    ```plaintext
    pkg install python pip
    pkg install binutil
    pkg install python-tkinter
    pkg install clang python libffi openssl libsodium
    SODIUM_INSTALL=system pip install pynacl
    ```

    Please make sure to go into `settings.py` and change `is_phone` to `True`.

4. If using Command Prompt, Konsole, or similar terminals, go to the bot directory and run the following command:

    ```
    pip install -r requirements.txt
    ```

    This should install the required modules for the bot.

5. Set up the environment (Guaranteed to work in Python 3.13.3).
6. Edit the bot (More information below).
7. Run the bot.

### **What you will put into each file:**

#### `longterm_lists.json`

```json
{
    "true_natsukians": [
        "Put your own User ID here. This is used for Administrators who can use commands like adding and removing people to and from the blacklist."
    ],
    "blacklist": [],
    "whitelist": []
}
```

That's all for this file. It may be replaced with an optional globally shared blacklist one day.

#### `twitter_embedder_settings.json`

This file will be automatically created after running the bot once. Add the Server IDs as integers to the corresponding fields. Example:

```json
{
  "vxtwitter.com": [
    123456789,
    234567890
  ],
  "fxtwitter.com": [],
  "etc...": []
}
```

Sites **must** be HTTP**S**!

If a Server is not in the list, it defaults to the first entry in the file. In the above example, it would default to `vxtwitter.com`.

#### `.env`

**FIRST:** <br/>
[Create a Github Token](https://github.com/settings/tokens/new) and save it!

**AFTER THAT:** <br/>
Create a new [Github Gist](https://gist.github.com/) and name the file `longterm_lists.json` (I recommend you name the gist the same).

**NEXT:** <br/>
Get your Bot Token:

1. Go to the [Discord Developer Portal](https://discordapp.com/developers/applications/).
2. Give your bot a name.
3. Go into the **Bot** menu.
4. Press **Add Bot**.
5. Press **Click to Reveal Token** - this is your Bot Token.

**Do not share your Bot Token!**

Now put them in your `.env` file.

<sup><span style="color:grey">Code block set to Python markdown for reading convenience. Hashtags / Pound Signs can be included in the final file.</span></sup>

```py
# .env
DISCORD_TOKEN=your_discord.bot_token

# If it is expired get a new one here:
# https://github.com/settings/tokens/new
# The GIST_ID is the last part of the URL.
GITHUB_TOKEN=your_github_token
GIST_ID=theIDyouGETwhenYOUcreateAgist
```

**MAKE SURE YOU ADD `.env` TO YOUR `.gitignore` FILE!**

## Edit the Bot

You **must** edit the bot, otherwise, several commands will be bugged and non-functional, especially in non-Windows (<=v2.5.6) or Linux (>=v2.5.7) environments. To find what you need to edit:

1. Use the search function inside `bot.py` for the word `EDIT`.
2. Follow the steps provided in the comments.

These sections refer to direct paths to folders that, very likely, do not exist on your machine. You will have to edit them, or completely remove them via editing. This will have to be done every time you update the bot.

For documentation on DiscordPy, refer to the [Official Discord.py Documentation](https://discordpy.readthedocs.io/en/stable/api.html).

## Reporting Bugs

If the issue is related to the bot itself, check if your issue is already open or solved. If not, open a new issue on GitHub.

Alternatively, visit the [Strawberry Games / Strawberry Software Server](https://discord.gg/9EAGVZUt2Y) for support.

If you want your users to send bug reports, they can use the `/bug_report` command (if set up). You can disable this command or use it as a simple non-anonymous reporting tool.

## Supporting the Bot

If you have improvements for the bot, feel free to contact me on Discord or GitHub. We can discuss changes and fixes. If your contributions are added to the official bot, you will be credited.

Please **do not** contact me if your changes include political, religious, or ideological additions. They may be considered, but the likelihood is lower if they include such elements. Clean up the code first.

*If you decide to make a bot derived from this, I kindly request that you do not use the "Natsuki" name or imagery.*

## Images and ASCII Art

When starting the bot, you may see ASCII image art. You can remove this by setting `enable_ascii` to `False` inside `settings.py`.

You can also add more ASCII art by following the JSON file format and adding your own art. The JSON structure is as follows:

- `"logo"` (This is just the logo. No additional properties apart from `"logo"`.)
- `"natsukis"` (An array of objects—ASCII images and their IDs.)
  - `"id"` (A unique identifier, useful for debugging.)
  - `"image"` (Where the ASCII art is stored and displayed.)

To check ASCII art, create a Python file that prints the ASCII and run it in Command Prompt or your local terminal.

**Compatibility with anything other than Windows 10 Command Prompt is **not** guaranteed!**

**Important:** The ASCII art must **only** use UTF-8 characters!

It is unknown whether ANSI Color Codes work correctly on all machines.

### **Contributing ASCII Art to Examples**

- Open a suggestion issue to add your ASCII art. You can also do this on the [Support Server](https://discord.gg/9EAGVZUt2Y).
- Credit the original artist.
- Provide a screenshot of your terminal displaying the ASCII using the **default** font and size configuration.
- If the art was generated using AI (Text2Image, Image2Image, or similar), explicitly state this.
- You **do not** need to disclose AI tools such as brush smoothing or line tools.
- If your digital art could be mistaken for traditional, clarify that it is digital.

Keep the width around **64 characters** at most. The less, the better.

## Music

The music function is **buggy** and still in development.

### **Playlists do not work!**

- If you send a playlist link, only the selected song will play. If you can fix this, contact me, and I'll credit your fix.
- If the bot shows incorrect titles, lengths, or thumbnails, restart the bot. The queue is likely messed up. Avoid requesting multiple songs simultaneously.
- The Playlist command may sometimes show incorrect songs or fail to update properly.
- The skip command *should* work.

This is a rudimentary solution after major bots removed YouTube playback for an immature reason. *(But hey, while you can’t play YouTube videos anymore, at least you can be a child predator on Discord without facing any problems! Some of the Discord Administrators will even join you on that adventure!)*

- The bot **cannot** play age-restricted videos. There may be a way to bypass this, but I don’t know how. You might be able to do this by having yt-dlp log in using your credentials, but I don't plan on adding this functionality by default.
- **Country-restricted videos can be bypassed with a VPN.**
- If you're running the bot on a server, use a VPN to bypass country restrictions.

## Termux Notes

~~- Because Termux uses a different file system, the `webm_downloads` folder will be named `.\webm_downloads`. This will be hidden by default.~~ **FIXED IN VERSIONS >=2.3.26**

- ~~Use **FX File Explorer** on Android to manually clear it if necessary.~~ **FIXED IN VERSIONS >=2.3.26**
- ~~Location in **FX File Explorer**: `Home > [Your NatsukiBot Installation Directory] > .\webm_downloads`.~~ **FIXED IN VERSIONS >=2.3.26**
- As of **version >=2.3.26**, the folder is properly named `webm_downloads` on both **Windows** and **Termux**, and the auto-delete feature thus works correctly on both platforms. If you used versions **2.3.25 or earlier**, you might have to delete the old folder manually via `rm -d '.\webm_downloads'`.
- ~~Termux is a **lower priority** than Windows, with other OS support even lower. However, since I also use Termux, **compatibility is a top priority**. Expect nearly the same functionality as on PC.~~ As of version 2.5.7, Termux is **top priority**, closely followed by **Linux** (Arch), and other Operating Systems behind them.

## Dev Notes

This isn't part of the "documentation," just wanted to say **thank you** for using the bot!

I've worked on this for years (since **2018**!), and while the music system aged me like 20 years through sheer suffering, it's still fun!

Enjoy the bot! **\^-\^**
