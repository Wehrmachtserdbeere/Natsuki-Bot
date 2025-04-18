
# Natsuki Bot

## Installation

1. Clone the repository or download the source directly and put it into a folder with nothing else inside.
2. Create and fill these files:
   - `botToken.py`
   - `longterm_lists.json`
3. If you run this via Termux, you **must** run these commands in this order:

    ```
    pkg install python pip
    pkg install binutil
    pkg install python-tkinter
    pkg install clang python libffi openssl libsodium
    SODIUM_INSTALL=system pip install pynacl
    ```

    Please make sure to go into `settings.py` and change `is_phone` to `True`.

4. If using Command Prompt, go to the bot directory and run the following command:

    ```
    pip install -r requirements.txt
    ```

    This should install the required modules for the bot.

5. Set up the environment (Guaranteed to work in Python 3.13.3).
6. Edit the bot (More information below).
7. Run the bot.


### **What you will put into each file:**

#### `botToken.py`

```py
botToken = "your.bot.token"
```

To get your Bot Token:
1. Go to the [Discord Developer Portal](https://discordapp.com/developers/applications/).
2. Give your bot a name.
3. Go into the **Bot** menu.
4. Press **Add Bot**.
5. Press **Click to Reveal Token** - this is your Bot Token.

**Do not share your Bot Token!**

#### `longterm_lists.json`

```json
{
    "true_natsukians": [
        "Put your own User ID here. This is used for Administrators who can use commands like adding and removing people from the blacklist."
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
  "vxtwitter": [
    123456789,
    234567890
  ],
  "fxtwitter": [],
  "etc...": []
}
```

Falls back on a default value if a given Server is not in the list.

## Edit the Bot

You **must** edit the bot, otherwise, several commands will be bugged and non-functional. To find what you need to edit:

1. Use the search function inside `bot.py` for the word `EDIT`.
2. Follow the steps provided in the comments.

Alternatively, you can comment out or remove commands you don't need. For documentation on DiscordPy, refer to the [Official Discord.py Documentation](https://discordpy.readthedocs.io/en/stable/api.html).

## Reporting Bugs

If the issue is related to the bot itself, check if your issue is already open or solved. If not, open a new issue on GitHub.

Alternatively, visit the [Strawberry Games / Strawberry Software Server](https://discord.gg/9EAGVZUt2Y) for support.

If you want your users to send bug reports, they can use the `/bug_report` command (if set up). You can disable this command or use it as a simple non-anonymous reporting tool.

## Supporting the Bot

If you have improvements for the bot, feel free to contact me on Discord or GitHub. We can discuss changes and fixes. If your contributions are added to the official bot, you will be credited.

Please **do not** contact me if your changes include political, religious, or ideological additions. They may be considered, but the likelihood is lower if they include such elements. Clean up the code first.

*If you decide to make a bot derived from this, I kindly request that you do not use the "Natsuki" name or imagery.*

## Images / ASCII Art

When starting the bot, you may see ASCII image art. You can remove this by setting `enable_ascii` to `False` inside `settings.py`.

You can also add more ASCII art by following the JSON file format and adding your own art. The JSON structure is as follows:

- `"logo"` (This is just the logo. No additional properties apart from `"logo"`.)
- `"natsukis"` (An array of objects—ASCII images and their IDs.)
  - `"id"` (A unique identifier, useful for debugging.)
  - `"image"` (Where the ASCII art is stored and displayed.)

To check ASCII art, create a Python file that prints the ASCII and run it in Command Prompt.

**Compatibility with anything other than Windows 10 Command Prompt is **not** guaranteed!**

### **Important:** The ASCII art must **only** use UTF-8 characters!

#### **Contributing ASCII Art to Examples**

- Open a suggestion issue to add your ASCII art. You can also do this on the [Support Server](https://discord.gg/9EAGVZUt2Y).
- Credit the original artist.
- Provide a screenshot of your console displaying the ASCII.
- If the art was generated using AI (Text2Image or Image2Image), explicitly state this.
- You **do not** need to disclose AI tools like brush smoothing or line tools.
- If your digital art could be mistaken for traditional, clarify that it is digital.

Keep the width around **64 characters**.

## Music

The music function is **buggy** and still in development.

### **Playlists do not work!**

- If you send a playlist link, only the selected song will play. If you can fix this, contact me, and I'll credit your fix.
- If the bot shows incorrect titles, lengths, or thumbnails, restart the bot. The queue is likely messed up. Avoid requesting multiple songs simultaneously.
- The Playlist command may sometimes show incorrect songs or fail to update properly.
- The skip command **should** work.

This is a rudimentary solution after major bots removed YouTube playback for an immature reason. *(But hey, while you can’t play YouTube videos anymore, at least you can be a child predator on Discord without facing any problems! Some of the Discord Administrators even are those!)*

- The bot **cannot** play age-restricted videos. There may be a way to bypass this, but I don’t know how.
- **Country-restricted videos can be bypassed with a VPN.**
- If you're running the bot on a server, use a VPN to bypass country restrictions.

## Termux Notes

~~- Because Termux uses a different file system, the `webm_downloads` folder will be named `.\webm_downloads`. This will be hidden by default.~~ **FIXED IN VERSIONS >=2.3.26**
  - ~~Use **FX File Explorer** on Android to manually clear it if necessary.~~ **FIXED IN VERSIONS >=2.3.26**
  - ~~Location in **FX File Explorer**: `Home > [Your NatsukiBot Installation Directory] > .\webm_downloads`.~~ **FIXED IN VERSIONS >=2.3.26**
  - As of **version >=2.3.26**, the folder is properly named `webm_downloads` on both **Windows** and **Termux**, and the auto-delete feature thus works correctly on both platforms. If you used versions **2.3.25 or earlier**, you might have to delete the old folder manually via `rm -d '.\webm_downloads'`.
- Termux is a **lower priority** than Windows, with other OS support even lower. However, since I also use Termux, **compatibility is a top priority**. Expect nearly the same functionality as on PC.

## Dev Notes

This isn't part of the "documentation," just wanted to say **thank you** for using the bot!

I've worked on this for years (since **2018**!), and while the music system aged me like 20 years through sheer suffering, it's still fun!

Enjoy the bot! \^-\^  