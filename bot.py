__author__ = "Strawberry Software"
__copyright__ = "Copyright 2019-2025"
__credits__ = [
    "Strawberry",
    "Vim - An old Friend of Strawberry's",
    "italy2003 (https://www.pixiv.net/en/users/66835722)"
    ]
__license__ = "MIT"
__version__ = "2.3.25"
__maintainer__ = "Strawberry"
__status__ = "Development"
__support_discord__ = "https://discord.gg/9EAGVZUt2Y" # EDIT THIS
__invite_link__ = "https://discord.com/api/oauth2/authorize?client_id=883082974252384277&permissions=8&scope=bot" # EDIT THIS

# bot.py

#
# Note to self: DO NOT ADD COGS, they break EVERYTHING! It is NOT worth it, no matter what people say!
#

import asyncio
import json
import math
import time
import tkinter
import aiohttp

if __name__ == "__main__":
    pass

import random
import os
import sys
import discord
from discord import app_commands
import discord.ext
import discord.utils
from oracle import oracle as oraclewords
from oracle_german import oracle_de as oracle_de_words
import functools
from discord.ext import commands
from botToken import botToken
import eyed3
import datetime
from bs4 import BeautifulSoup
from discord.ext.commands import Context, Greedy
from typing import Optional, Literal
from datetime import datetime
import re
from pathlib import Path
import yt_dlp
from datetime import date
from importlib.metadata import version
import logging
import requests
from datetime import timedelta
import json
import subprocess
from datetime import timedelta
import defusedxml.ElementTree as ET
import settings

# Settings
is_phone = settings.is_phone
ping_delay = settings.ping_delay
enable_ascii = settings.enable_ascii
print_guilds_connected = settings.print_guilds_connected
is_debugging = settings.is_debugging
DISCORD_FILE_LIMIT = settings.file_size_limit
waifugame_enabled = settings.enable_waifugame

if is_debugging:
    logging.basicConfig(level=logging.DEBUG)
else:
    # User will still want good warnings.
    logging.basicConfig(level=logging.ERROR)

time_now = datetime.now().strftime("%H:%M:%S")
print(f"Bot Started at {time_now}")

client = commands.Bot(
    command_prefix="n!",
    description="A bot of the best character in DDLC!",
    status=discord.Status.online,
    case_insensitive=True,
    intents=discord.Intents.all()
    )

mp3_path = list(Path("D:\\Alles\\Alle Musik und Videos\\RR\\").rglob("*.mp3")) # <-- EDIT this to whatever folder your RR music is in.
folders = [
    "D:\\Alles\\Alle Musik und Videos\\RR under 8MB\\", # <-- EDIT this to your RR music. RR = Real Rock.
    ""
]

# For on_ready, so it only creates one single task.
has_started = False

@client.command()
@commands.guild_only()
@commands.is_owner()
@app_commands.default_permissions(manage_messages=True)
async def sync(
    interaction: discord.Interaction,
    ctx: Context,
    guilds: Greedy[discord.Object],
    spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    """
    Manually sync the bot (True Natsukian only command)
    """
    if not check_user_is_true_natsukian(interaction.user.id, load_longterm_lists()):
        interaction.channel.send(
            content = "Cannot use command, you are not a Bot Admin.",
            delete_after = 5
            )
        return
    
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

def shorten(string):
    """
    Replace spaces with underscores
    """
    return string.replace(" ", "_")

### Music

activity_json_file_path = "./activity_texts.json" # <-- EDIT this to your own path!

with open(activity_json_file_path, encoding = "utf8") as file:
    activity_text_data = json.load(file)

ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    'options': '-vn ',
}

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

def endSong(guild, path):
    os.remove(path)


def search(query):
    with yt_dlp.YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
        try: requests.get(query)
        except: info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        else: info = ydl.extract_info(query, download=False)
    return (info, info['url'], info['title'], info['duration'], info['thumbnail'])




### End of Music



print("Initializing...")

# Load blacklist data from a JSON file
def load_longterm_lists(filename="./longterm_lists.json"):
    '''Load data from a file.'''
    with open(filename, 'r') as file:
        return json.load(file)

# Check if user is in blacklist and return details
def check_user_in_blacklist(user_id, blacklist_data) -> str | bool:
    '''Returns user ID if found. Else returns a bool "False".'''
    for entry in blacklist_data['blacklist']:
        if entry['uid'] == user_id:
            return entry['uid'], entry['reason']
    return False

# Check if True Natsukian
def check_user_is_true_natsukian(userid : int, natsukian_data : json) -> str | bool:
    '''Returns user ID if found. Else returns a bool "False"'''
    for entry in natsukian_data['true_natsukians']:
        if str(entry) == str(userid):
            return str(entry)
    return False

# Save data to JSON file
def save_data(data, filename="./longterm_lists.json"):
    '''Save data to a JSON file.'''
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# For activity-related things. Discord shows "status" to users, despite it being Activities.
class NatsukiActivity:
    '''Represents a collection of activity-related things.'''
    
    async def set_random_activity(activity_text_data : str):
        '''Set a random activity, defaults to "Chilling" if "activity_text_data" is faulty.'''
        try:
            activity_text = random.choice(activity_text_data["default"])
            activity = discord.CustomActivity(
                type = discord.ActivityType.custom,
                name = "Custom Status", # Does nothing, but is required.
                state = activity_text,
            )
            await client.change_presence(
                activity = activity
            )
        except:
            activity = discord.CustomActivity(
                type = discord.ActivityType.custom,
                name = "Custom Status", # Does nothing, but is required.
                state = "Chilling",
            )
            await client.change_presence(
                activity = activity
            )
    
    async def set_voice_activity(activity_text_data : str):
        '''Sets a random voice-related activity'''
        try:
            activity_text = random.choice(activity_text_data["voice"])
            activity = discord.CustomActivity(
                type = discord.ActivityType.custom,
                name = "Custom Status", # Does nothing, but is required.
                state = activity_text,
            )
            await client.change_presence(
                activity = activity
            )
        except:
            activity = discord.CustomActivity(
                type = discord.ActivityType.custom,
                name = "Custom Status", # Does nothing, but is required.
                state = "Speaking",
            )
            await client.change_presence(
                activity = activity
            )
    
    async def set_streaming_activity(activity_text_data : str):
        '''Sets a random streaming-related (i.E. streaming music) activity'''
        try:
            activity_text = random.choice(activity_text_data["streaming"])
            activity = discord.CustomActivity(
                type = discord.ActivityType.custom,
                name = "Custom Status", # Does nothing, but is required.
                state = activity_text,
            )
            await client.change_presence(
                activity = activity
            )
        except:
            activity = discord.CustomActivity(
                type = discord.ActivityType.custom,
                name = "Custom Status", # Does nothing, but is required.
                state = "Streaming",
            )
            await client.change_presence(
                activity = activity
            )

# Because I often accidentally write the wrong name.
NatsukiStatus = NatsukiActivity

@client.tree.command(name="cute")                                                   # n!you_are_cute
async def you_are_cute(interaction: discord.Interaction) -> None:
    """ Tell me I'm cute """

    blacklist_data = load_longterm_lists()
    user_id = str(interaction.user.id)  # Convert user ID to string
    result = check_user_in_blacklist(user_id, blacklist_data)
    
    if result:
        uid, reason = result
        await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
    else:        
        await interaction.response.send_message("I'm NOT cute!!!")


@client.tree.command(name="ping")                                  # n!ping
async def ping(interaction: discord.Interaction) -> None:
    """ Get my Ping """
    await interaction.response.send_message(f"Pong! `{(client.latency * 100):.3f}ms`")



# These commands point to a local folder.
if not is_phone:
    @client.tree.command(name="img")                                   # Natsuki image from "Natsuki Worship" <-- Oh wow this is an old comment! Has to be from 2019! Thank God I don't store my images on Discord anymore :P.
    async def img(interaction: discord.Interaction) -> None:
        """ Send an image of Natsuki """

        blacklist_data = load_longterm_lists()
        user_id = str(interaction.user.id)  # Convert user ID to string
        result = check_user_in_blacklist(user_id, blacklist_data)

        if result:
            uid, reason = result
            await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
        else: 
            imgimg = "D:\\Alles\\Alle Bilder\\DDLC\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\DDLC")) # <-- EDIT this to any path with images you like.
            await interaction.response.send_message(file=discord.File(imgimg))


    @client.tree.command(name="shdf")                                   # Get image <-- Can ignore unless you find a meaning behind "shdf", I don't remember.
    async def shdf(interaction: discord.Interaction):
        """ Send an SHDF image """

        blacklist_data = load_longterm_lists()
        user_id = str(interaction.user.id)  # Convert user ID to string
        result = check_user_in_blacklist(user_id, blacklist_data)

        if result:
            uid, reason = result
            await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
        else: 
            shdfimg = "D:\\Alles\\Alle Bilder\\Anime People doing Wholesome Thing\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Anime People doing Wholesome Thing")) # <-- EDIT this to any path with images you like.
            await interaction.response.send_message(file=discord.File(shdfimg))
    
    @client.tree.command(name="fate")                           # Fate image
    async def fate(interaction: discord.Interaction):
        """ Get an image of the anime \"Fate\" """
        blacklist_data = load_longterm_lists()
        user_id = str(interaction.user.id)  # Convert user ID to string
        result = check_user_in_blacklist(user_id, blacklist_data)
        
        if result:
            uid, reason = result
            await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
        else:
            fateimg = "D:Alles\\Alle Bilder\\Fate\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Fate")) # <-- EDIT this if you have a folder for Fate images.
            await interaction.response.send_message(file=discord.File(fateimg))
    
    
    @client.tree.command(name="tanya")                           # Tanya image from
    async def tanya(interaction: discord.Interaction):
        """ Get an image of Tanya von Degurechaff """
        blacklist_data = load_longterm_lists()
        user_id = str(interaction.user.id)  # Convert user ID to string
        result = check_user_in_blacklist(user_id, blacklist_data)
        
        if result:
            uid, reason = result
            await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
        else:
            tanyaimg = "D:\\Alles\\Alle Bilder\\Tanya Degurechaff\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Tanya Degurechaff")) # <-- EDIT this if you have a folder for images of anything called "tanya".
            await interaction.response.send_message(file=discord.File(tanyaimg))


    @client.tree.command(name="tomboy")                                   # Get image
    async def tomboy(interaction: discord.Interaction):
        """Mmm tomboy abs yummy licky """
        blacklist_data = load_longterm_lists()
        user_id = str(interaction.user.id)  # Convert user ID to string
        result = check_user_in_blacklist(user_id, blacklist_data)

        if result:
            uid, reason = result
            await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
        else:
            tomboyimg = "D:\\Alles\\Alle Bilder\\Anime Tomboys\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Anime Tomboys")) # <-- EDIT this to your Anime Tomboys folder. I know you have one.
            await interaction.response.send_message(file=discord.File(tomboyimg))


    @client.tree.command(name="rem")
    async def rem(interaction: discord.Interaction):
        """ Get an image of Rem """
        blacklist_data = load_longterm_lists()
        user_id = str(interaction.user.id)  # Convert user ID to string
        result = check_user_in_blacklist(user_id, blacklist_data)

        if result:
            uid, reason = result
            await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
        else:
            remimg = "D:\\Alles\\Alle Bilder\\Rem\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Rem\\")) # <-- EDIT this to images of Rem.
            await interaction.response.send_message(file=discord.File(remimg))


    @client.tree.command(name="klk")
    async def klk(interaction: discord.Interaction):
        """ Get an image of Kill la Kill """
        blacklist_data = load_longterm_lists()
        user_id = str(interaction.user.id)  # Convert user ID to string
        result = check_user_in_blacklist(user_id, blacklist_data)

        if result:
            uid, reason = result
            await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
        else:
            klkimg = "D:\\Alles\\Alle Bilder\\Kill la Kill\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Kill la Kill\\")) # <-- EDIT this to Kill La Kill images.
            await interaction.response.send_message(file=discord.File(klkimg))


    @client.tree.command(name="rmeme")
    async def rmeme(interaction: discord.Interaction):
        """ Get one of Strawb's memes """
        blacklist_data = load_longterm_lists()
        user_id = str(interaction.user.id)  # Convert user ID to string
        result = check_user_in_blacklist(user_id, blacklist_data)

        if result:
            uid, reason = result
            await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
        else:
            await interaction.response.defer()
            try:
                mp4 = "D:\\Alles\\Alle Musik und Videos\\" + random.choice(os.listdir("D:\\Alles\\Alle Musik und Videos\\")) # <-- EDIT this to a path with video memes.
                await interaction.followup.send(file=discord.File(mp4))
            except discord.errors.HTTPException:
                await interaction.followup.send("File too large, try again.")
            except PermissionError:
                await interaction.followup.send("Permission denied; Folder was auto-blocked, please try again.")
    

    @client.tree.command(name="rr")                                       # EDIT this away if you don't have RR or NS music. RR here means Real Rock, and I forgot what NS stood for.
    async def rr(interaction: discord.Interaction):
        """ Get a NS song (Most likely German) """
        blacklist_data = load_longterm_lists()
        user_id = str(interaction.user.id)  # Convert user ID to string
        result = check_user_in_blacklist(user_id, blacklist_data)

        if result:
            uid, reason = result
            await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
        else:
            await interaction.response.defer()
            try:
                mp3 = random.choice(mp3_path)
                try:
                    audiofile = eyed3.load(mp3)
                    try:
                        audTitle = audiofile.tag.title
                    except AttributeError:
                        audTitle = "Unknown Title"
                    try:
                        audArt = audiofile.tag.artist
                    except AttributeError:
                        audArt = "Unknown Artist"
                    try:
                        audAlbum = audiofile.tag.album
                    except AttributeError:
                        audAlbum = "Unknown Album"
                    await interaction.followup.send(f"Song: {audTitle} | Artist: {audArt} | Album: {audAlbum}", file=discord.File(mp3))
                    print(f"RR music -- {mp3}")
                except discord.errors.HTTPException:
                    await interaction.followup.send("File too large, try again.")
                except PermissionError:
                    await interaction.followup.send("Permission denied; Folder was probably auto-blocked.")
            except OSError:
                await interaction.followup.send("An error occoured, please try again.")


    @client.tree.command(name="christ_chan")
    async def christ_chan(interaction: discord.Interaction):
        """ Get an image of Christ-Chan """
        blacklist_data = load_longterm_lists()
        user_id = str(interaction.user.id)  # Convert user ID to string
        result = check_user_in_blacklist(user_id, blacklist_data)

        if result:
            uid, reason = result
            await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
        else:
            chrImg = "D:\\Alles\\Alle Bilder\\Christ-chan\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Christ-chan\\")) # <-- EDIT this to a path with images of Christ Chan. Not to be confused with Chris Chan.
            await interaction.response.send_message(file=discord.File(chrImg))


    @client.tree.command(name="chan")
    async def chan(interaction: discord.Interaction):
        """ Get an image of another Chan """
        blacklist_data = load_longterm_lists()
        user_id = str(interaction.user.id)  # Convert user ID to string
        result = check_user_in_blacklist(user_id, blacklist_data)

        if result:
            uid, reason = result
            await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
        else:
            chanImg = "D:\\Alles\\Alle Bilder\\Other Chans\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Other Chans\\")) # <-- EDIT this to a path with images of other -chan characters.
            await interaction.response.send_message(file=discord.File(chanImg))


    @client.tree.command(name="megu")
    async def megu(interaction: discord.Interaction):
        """ Get an image of Megumin """
        blacklist_data = load_longterm_lists()
        user_id = str(interaction.user.id)  # Convert user ID to string
        result = check_user_in_blacklist(user_id, blacklist_data)

        if result:
            uid, reason = result
            await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
        else:
            chanImg = "D:\\Alles\\Alle Bilder\\Megumin\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Megumin\\")) # <-- EDIT this to a path with Megumin images.
            await interaction.response.send_message(file=discord.File(chanImg))


B = ":black_large_square:"
b = B
W = ":white_large_square:"
w = W
R = ":red_square:"
r = R


@client.tree.command(name="draw")
async def draw(
    interaction: discord.Interaction,
    drawmessage: str):
    """ Draw something with B, W, R, and . """
    blacklist_data = load_longterm_lists()
    user_id = str(interaction.user.id)  # Convert user ID to string
    result = check_user_in_blacklist(user_id, blacklist_data)
    
    if result:
        uid, reason = result
        await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
    else: 
        drawfinalmessage = []

        for char in drawmessage:
            if char == "B" or char == "b":
                drawfinalmessage.append(str(B))
            elif char == "W" or char == "w":
                drawfinalmessage.append(str(W))
            elif char == "R" or char == "r":
                drawfinalmessage.append(str(R))
            elif char == ".":
                drawfinalmessage.append("\n")
        finalmessage = ''.join(drawfinalmessage)

        if len(finalmessage) <= 2000:
            await interaction.response.send_message(finalmessage)
        else:
            await interaction.response.send_message("Message too long. It has to be ~100 characters or less.\nBecause Discord Emojis vary in string sizes, it may be more or less than 100.")


# Oracle
@client.tree.command(name="oracle")
async def oracle(
    interaction: discord.Interaction,
    amount_of_letters: int):
    """ Terry A. Davis' Oracle """
    blacklist_data = load_longterm_lists()
    user_id = str(interaction.user.id)  # Convert user ID to string
    result = check_user_in_blacklist(user_id, blacklist_data)
    
    if result:
        uid, reason = result
        await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
    else: 
        await interaction.response.send_message(functools.reduce(lambda line, word: line + f"{word} ", (random.choice(oraclewords) for _ in range(amount_of_letters)), str()))


# Oracle German
@client.tree.command(name="oracle_ger")
async def oracle_ger(
    interaction: discord.Interaction,
    amount_de: int):
    """ Terry A. Davis' Oracle but in German """
    blacklist_data = load_longterm_lists()
    user_id = str(interaction.user.id)  # Convert user ID to string
    result = check_user_in_blacklist(user_id, blacklist_data)
    
    if result:
        uid, reason = result
        await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
    else:
        await interaction.response.send_message(functools.reduce(lambda line, word: line + f"{word} ", (random.choice(oracle_de_words) for _ in range(amount_de)), str()))



@client.tree.command(name="safe")
@app_commands.describe(tags = "Enter tags in a `tag 1, tag 2 (series name), -banned tag, *wildcard` format")
async def safe(
    interaction: discord.Interaction,
    tags: str):
    """ Get an image from Safebooru """
    blacklist_data = load_longterm_lists()
    user_id = str(interaction.user.id)  # Convert user ID to string
    result = check_user_in_blacklist(user_id, blacklist_data)
    if result:
        uid, reason = result
        await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
    else:
        try:
            ctxtags1 = tags.replace(", ", "+")
            ctxtags = ctxtags1.replace(" ", "_")
            urlSafePre = "https://safebooru.org/index.php?page=dapi&s=post&q=index&tags=" + ctxtags + "rating:s"
            async with aiohttp.ClientSession() as session:
                async with session.get(urlSafePre) as response:
                    html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            file_urls = []
            file_urls_length = 0
            source = []
            for post in soup.find_all('post'):
                file_urls.append(post.get('file_url'))
                file_urls_length += 1
                source.append(post.get('id'))
            the_url_num = random.randint(0, file_urls_length - 1)
            the_url = file_urls[the_url_num]
            await interaction.response.send_message(str(the_url) + f"\nTags recorded: `{ctxtags}`\nID: {source[the_url_num]} | Found `{file_urls_length - 1}` other entries.")
            print(
                f"Someone has searched for \"{tags}\"\nThis has resulted in the bot sending this link: [ {urlSafePre} ]")
        except IndexError:
            await interaction.response.send_message(f"No results found for {tags}.")


@client.tree.command(name="gelbooru")
@app_commands.describe(tags = "Enter tags in a `tag 1, tag 2 (series name), -banned tag, *wildcard` format")
@app_commands.describe(nsfw = "Filter ratings. Default: `Safe`")
@app_commands.describe(gendered = "Filter `Female Only`, `Male Only`, or `Any` images. Default: `Any`")
async def gel(
    interaction: discord.Interaction,
    tags: str,
    nsfw: Literal['safe', 'safe and questionable', 'questionable', 'explicit only', 'all'] = 'safe',
    gendered: Literal['Female Only', 'Male Only', 'Any'] = 'Any'):
    """ Get an image from Gelbooru (SFW only) """
    blacklist_data = load_longterm_lists()
    user_id = str(interaction.user.id)  # Convert user ID to string
    result = check_user_in_blacklist(user_id, blacklist_data)
    if result:
        uid, reason = result
        await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
        return
    elif not interaction.channel.nsfw and nsfw.lower() in ['questionable', 'explicit only', 'all']:
        await interaction.response.send_message(f"Could not run command! This command is for channels marked NSFW only!")
        return
    else:
        urlSafePre = ""
        try:
            print(tags)
            await interaction.response.defer()
            ctxtags3 = tags.replace(", ", "+")
            ctxtags2 = ctxtags3.replace(" ", "_")
            print(ctxtags2)
            if nsfw == 'safe':  # Safe only
                urlSafePre = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=" + ctxtags2 + "+-transgender+-transgender_flag+-transgender_colors+-transsexual+-rating:questionable+-rating:explicit"
            elif nsfw == 'safe and questionable':  # All except explicit
                urlSafePre = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=" + ctxtags2 + "+-transgender+-transgender_flag+-transgender_colors+-transsexual+-rating:explicit"
            elif nsfw == 'all':  # All
                urlSafePre = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=" + ctxtags2 + "+-transgender+-transgender_flag+-transgender_colors+-transsexual"
            elif nsfw == 'explicit only':  # Explicit only
                urlSafePre = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=" + ctxtags2 + "+-transgender+-transgender_flag+-transgender_colors+-transsexual+rating:explicit"
            elif nsfw == 'questionable':  # Questionable only
                urlSafePre = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=" + ctxtags2 + "+-transgender+-transgender_flag+-transgender_colors+-transsexual+rating:questionable"
            if gendered == 'Female Only':
                urlSafePre += "+-1boy+-2boys+-3boys+-4boys+-5boys+-6%2bboys+-penis+-multiple_penises+-muscular_male+-male_focus+-multiple_boys+-futanari+-futa_only+-yaoi"
            elif gendered == 'Male Only':
                urlSafePre += "+-1girl+-2girls+-3girls+-4girls+-5girls+-6%2bgirls+-vagina+-futanari"
            else:
                pass
            async with aiohttp.ClientSession() as session:
                async with session.get(urlSafePre) as response:
                    html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            gel_file_urls = []
            gel_file_ratings = []
            source = []
            gel_file_urls_length = 0
            for post in soup.find('posts').find_all('post'):
                # if post.find('rating').get_text().strip().lower() == "general":
                gel_file_urls.append(post.find('file_url').get_text())
                gel_file_ratings.append(post.find('rating').get_text())
                source.append(post.find('id').get_text())
                gel_file_urls_length += 1
            the_url_num = random.randint(0, gel_file_urls_length - 1)
            the_url = gel_file_urls[the_url_num]
            if gel_file_ratings[the_url_num] == 'explicit' or gel_file_ratings[the_url_num] == 'questionable':
                await interaction.followup.send("|| " + str(the_url) + f" ||\nTags recorded: `{ctxtags2}`\nUser searched for: `{nsfw}`\nID: `{source[the_url_num]}`\nFound `{gel_file_urls_length - 1}` other entries.")
            else:
                await interaction.followup.send(str(the_url) + f"\nTags recorded: `{ctxtags2}`\nUser searched for: `{nsfw}`\nID: `{source[the_url_num]}`\nFound `{gel_file_urls_length - 1}` other entries.")
            print(
                f"Someone has searched for \"{tags}\"\nThis has resulted in the bot sending this link: [ {urlSafePre} ]\nThe ID of the post is `{source[the_url_num]}`\n"
                f"This is the link sent: -# {the_url} #-")
        except IndexError or discord.app_commands.errors.CommandInvokeError:
            await interaction.followup.send(f"No results found for `{tags}`.")
        except ValueError:
            await interaction.followup.send(f"Something went wrong. Please check the spelling of each tag and try again.\nPlease check Gelbooru if it s down or if it shows results at all.\nTags used: `{tags.replace('+', ', ')}`")


@client.tree.command(name="rule34xxx")
@app_commands.describe(tags = "Enter tags in a `tag 1, tag 2 (series name), -banned tag, *wildcard` format")
@app_commands.describe(gendered = "Filter `Female Only`, `Male Only`, or `Any` images. Default: `Any`")
@app_commands.describe(blacklists = "Preset Blacklists for various tags considered NSFL or disgusing. Default: Use All Presets")
@app_commands.describe(allow_ai = "Dis/Allow images generated by AI. Default: `False`")
@app_commands.describe(allow_3d = "Dis/Allow '3d' images. Default: `False`")
async def rule34xxx(
    interaction: discord.Interaction,
    tags: str,
    gendered: Literal['Female Only', 'Male Only', 'Any'] = 'Any',
    blacklists: Literal['Guro', 'Futa', 'Scat', 'Guro and Futa', 'Guro and Scat', 'Scat and Futa', 'Guro, Scat and Futa', 'None'] = 'Guro, Scat and Futa',
    allow_lolis: bool = True,
    allow_obesity: bool = False,
    allow_ai: bool = False,
    allow_3d: bool = False):
    """
    Get an image from rule34.xxx (NSFW very likely)\n
    `tags` defines tags. Follow this format: `tag_1, tag_2, -banned_tag, *wild_card`
    """
    blacklist_data = load_longterm_lists()
    user_id = str(interaction.user.id) # Convert user ID to string
    result = check_user_in_blacklist(user_id, blacklist_data)

    female_only = "+-1boy+-2boys+-3boys+-4boys+-5boys+-6%2bboys+-penis+-multiple_penises+-muscular_male+-male_focus+-multiple_boys+-yaoi"
    male_only = "+-1girl+-2girls+-3girls+-4girls+-5girls+-6%2bgirls+-vagina"
    guro = "+-guro+-gore+-death+-murder+-beaten+-decapitated_head+-decapitation+-female_death+-necrophilia+-ryona+-severed_head+-skullfuck+-skull_fucking+-snuff"
    futa = "+-futa+-futadom+-dickgirl+-shemale+-newhalf+-gynomorph+-cuntboy+-hermaphrodite+-intersex+-futa_only"
    scat = "+-scat+-shit+-scat_inflation+-poop+-pooping+-defecating+-shitting_self+-fart+-farting+-fart_cloud+-fart_fetish+-hyper_fart"
    loli = "+-loli+-shota+-lolicon+-shotacon"
    obesity = "+-huge_ass+-hyper_ass+-giant_ass+-gigantic_breasts+-enormous_breasts+-massive_breasts+-colossal_breasts+-astronomical_breasts+-obese+-fat+-fat_man+-fat_woman+-plump"
    ai_tags = "+-ai_generated+-ai_*"
    tags_3d = "+-3d+-3d_(artwork)+-3d_(gif)+-3d_(animation)+-3d_artwork+-3d_background+-3d_custom_girl"

    if result:
        uid, reason = result
        await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
        return
    elif not interaction.channel.nsfw:
        await interaction.response.send_message(f"Could not run command! This command is for channels marked NSFW only!")
        return
    else:
        pass
    
    #try:
    print(tags)
    await interaction.response.defer()
    ctxtags3 = tags.replace(", ", "+")
    ctxtags2 = ctxtags3.replace(" ", "_")
    print(ctxtags2)
    r34xxx_url_pre = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&tags=' + ctxtags2
    
    #Gender Tags
    if gendered == 'Female Only':
        r34xxx_url_pre = r34xxx_url_pre + female_only
    elif gendered == 'Male Only':
        r34xxx_url_pre = r34xxx_url_pre + male_only

    # Disgusting Tags
    if blacklists == 'Guro':
        r34xxx_url_pre = r34xxx_url_pre + guro
    elif blacklists == 'Futa':
        r34xxx_url_pre = r34xxx_url_pre + futa
    elif blacklists == 'Scat':
        r34xxx_url_pre = r34xxx_url_pre + scat
    elif blacklists == 'Guro and Futa':
        r34xxx_url_pre = r34xxx_url_pre + guro + futa
    elif blacklists == 'Guro and Scat':
        r34xxx_url_pre = r34xxx_url_pre + guro + scat
    elif blacklists == 'Scat and Futa':
        r34xxx_url_pre = r34xxx_url_pre + scat + futa
    elif blacklists == 'Guro, Scat and Futa':
        r34xxx_url_pre = r34xxx_url_pre + guro + scat + futa
    
    # Other tags
    if not allow_lolis:
        r34xxx_url_pre = r34xxx_url_pre + loli
    if not allow_obesity:
        r34xxx_url_pre = r34xxx_url_pre + obesity
    if not allow_ai:
        r34xxx_url_pre = r34xxx_url_pre + ai_tags
    if not allow_3d:
        r34xxx_url_pre = r34xxx_url_pre + tags_3d
    
    async with aiohttp.ClientSession() as session:
        async with session.get(r34xxx_url_pre) as response:
            xml_data = await response.text()
    
    r34xxx_file_urls = []
    source = []
    r34xxx_file_urls_length = 0

    root = ET.fromstring(xml_data)
    for post in root.findall('post'):
        r34xxx_file_urls.append(post.get('file_url'))
        source.append(post.get('id'))
        r34xxx_file_urls_length += 1

    the_url_num = random.randint(0, r34xxx_file_urls_length - 1)
    the_url = r34xxx_file_urls[the_url_num]
    await interaction.followup.send(str(the_url) + f"\nTags recorded: `{ctxtags2}`\nID: `{source[the_url_num]}`\nFound `{r34xxx_file_urls_length - 1}` other entries.")
    print(
        f"Someone has searched for \"{tags}\"\nThis has resulted in the bot sending this link: [ {r34xxx_url_pre} ]\nThe ID of the post is `{source[the_url_num]}`\n"
        f"This is the link sent: -# {the_url} #-")


    #except IndexError or discord.app_commands.errors.CommandInvokeError:
    #        await interaction.followup.send(f"No results found for `{tags}`.")
    #except ValueError:
    #    await interaction.followup.send(f"Something went wrong. Please check the spelling of each tag and try again.\nPlease check Rule34.xxx if it s down or if it shows results at all.\nTags used: `{tags.replace('+', ', ')}`")


@client.tree.command(name="bleachbooru")
@app_commands.describe(tags = "Enter tags in a `tag 1, tag 2 (series name), -banned tag, *wildcard` format")
@app_commands.describe(nsfw = "Filter ratings. Default: `Safe`. **WARNING** Even `Safe` will often result in NSFW artwork! Fault: Website Moderation.")
async def bleach(interaction: discord.Interaction, tags: str, nsfw: Literal['safe', 'questionable and safe (high filter)', 'questionable and safe (low filter)', 'all', 'explicit only'] = 'safe'): # <-- This site sucks btw, horrid API, barely any documentation, not even filtered correctly. Be careful, even "safe" will often return porn.
    """ Get an image from Bleachbooru (Severe NSFW warning) """
    blacklist_data = load_longterm_lists()
    user_id = str(interaction.user.id)  # Convert user ID to string
    result = check_user_in_blacklist(user_id, blacklist_data)
    if result:
        uid, reason = result
        await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
        return
    elif not interaction.channel.nsfw:
        await interaction.response.send_message(f"Could not run command! This command is for channels marked NSFW only!")
        return
    else:
        urlSafePreBleach = ""
        try:
            print(tags)
            await interaction.response.defer()
            ctxtags6 = tags.replace(", ", "+")
            ctxtags7 = ctxtags6.replace(" ", "_")
            print(ctxtags7)
            if nsfw == 'safe':  # Safe only
                urlSafePreBleach = "https://bleachbooru.org/post.xml?limit=100?tags=" + ctxtags7 + "+-sex+-nipples+-penis+-vaginal_penetration+rating%3As"
            elif nsfw == 'questionable and safe (high filter)':
                urlSafePreBleach = "https://bleachbooru.org/post.xml?limit=100?tags=" + ctxtags7 + "+-sex+-nipples+-penis+-vaginal_penetration+-rating%3Aexplicit"
            elif nsfw == 'questionable and safe (high filter)':
                urlSafePreBleach = "https://bleachbooru.org/post.xml?limit=100?tags=" + ctxtags7 + "+-rating%3Aexplicit"
            elif nsfw == 'all':
                urlSafePreBleach = "https://bleachbooru.org/post.xml?limit=100?tags=" + ctxtags7
            elif nsfw == 'explicit only':
                urlSafePreBleach = "https://bleachbooru.org/post.xml?limit=100?tags=" + ctxtags7 + "+rating%3Aexplicit"
            async with aiohttp.ClientSession() as session:
                async with session.get(urlSafePreBleach) as response:
                    html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            bleach_file_urls = []
            bleach_file_urls_length = 0
            source = []
            for post in soup.find('posts').find_all('post'):
                bleach_file_urls.append(post.attrs["file_url"])
                bleach_file_urls_length += 1
                source.append(post.attrs["id"])
            print("I arrived at line 363")
            the_url_num = random.randint(0, bleach_file_urls_length - 1)
            the_url = "https://bleachbooru.org" + bleach_file_urls[the_url_num]
            await interaction.followup.send(the_url + f"\nTags recorded: `{tags}`\nUser searched for: `{nsfw}`  |  ID: `{source[the_url_num]}`\nFound {bleach_file_urls_length - 1} other entries (Max. 39 others).")
            print("I arrived at line 367")
            print(
                f"Someone has searched for \"{tags}\"\nThis has resulted in the bot sending this link: [ {urlSafePreBleach} ]\nThe ID of the post is `{source[the_url_num]}`\n"
                f"This is the link sent: -# {the_url} #-")
        except IndexError or discord.app_commands.errors.CommandInvokeError:
            await interaction.followup.send(f"No results found for `{tags}`.")




@client.tree.command(name="roll")
@app_commands.describe(sides = "How many sides your dice should have")
@app_commands.describe(rolls = "How many dices you want to roll")
@app_commands.describe(highlight_number = "Highlight the x-th roll (counts from 1 upwards)")
async def roll(interaction: discord.Interaction, sides: int, rolls: int = 1, highlight_number: int = None):
    """ Roll a die """
    blacklist_data = load_longterm_lists()
    user_id = str(interaction.user.id)  # Convert user ID to string
    result = check_user_in_blacklist(user_id, blacklist_data)
    
    if result:
        uid, reason = result
        await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
    else:
        result = []
        response = ""
        if sides <= 0:
            await interaction.response.send_message("Please enter a positive, non-zero number when choosing sides.", ephemeral = True)
        elif rolls <= 0:
            await interaction.response.send_message("Please enter a positive, non-zero number when choosing how many rolls you want to make.", ephemeral = True)
        elif sides >= sys.maxsize:
            await interaction.response.send_message("Please enter a smaller number for how many sides your roll has.", ephemeral = True)
        elif rolls >= sys.maxsize:
            await interaction.response.send_message("Please enter a smaller number for how many roll you want to make.", ephemeral = True)
        else:
            try:
                for roll in range(rolls):
                    result.append(random.randint(1, sides))
                response = f"Input: `{rolls}d{sides}`\nResult: " + ", ".join(map(str, result))
                if highlight_number:
                    if highlight_number <= 0:
                        await interaction.response.send_message("Please enter a positive, non-zero number when choosing the highlighted roll.", ephemeral = True)
                    if highlight_number >= rolls + 2:
                        await interaction.response.send_message("Please ensure that the number you want to highlight is not higher than the number of rolls.", ephemeral = True)
                    else:
                        response = response + f"\nHighlighted Roll: {result[highlight_number - 1]}"
                await interaction.response.send_message(response)
            except Exception as e:
                await interaction.response.send_message(f"Error rolling die: {e}", ephemeral = True)


list_ = [
    "cunny",
    "kani",
    "loli",
    "lolicon",
    "shota",
    "shotacon",
    "uoh", "uooh", "uoooh", "uooooh",
    "correction",
    "coney",
    "coni",
    "koney",
    "koni",
    "kuni",
    "cnnuy"
]


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        try:
            await message.add_reaction(trash_emoji)
        except:
            print("Couldn't add emoji to own message :/")
            pass
        return

    # Load blacklist only if necessary
    if check_user_in_blacklist(user_id=message.author.id, blacklist_data=load_longterm_lists()):
        return

    message_lowsplit = message.content.lower().split()
    message_set = set(message_lowsplit)  # Convert to set for fast lookup

    if any(substring in message_set for substring in list_):
        await message.add_reaction('😭')
        return

    for word in message_lowsplit:
        if word.startswith('u') and word.endswith('h') and 'o' in word and not re.search('[a-gi-np-tv-z]', word):
            await message.add_reaction('😭')
            return  # Exit immediately after adding reaction



    ### Twitter Renamer ###

    # List of domains to exclude from processing
    excluded_domains = [
        
    ]

    links = re.findall(r"https?://(?:www\.)?[\w.-]+/[\S]*", message.content)
    has_embed = False

    if links:
        tiktok_alt = "https://vxtiktok.com"
        instagram_alt = "https://www.kkinstagram.com"
        pixiv_alt = "https://phixiv.net"
        youtube_alt = "https://youtube.com/watch?v="

        
        try:
            with open("twitter_embedder_settings.json") as twtfile:
                data = json.load(twtfile)
            
            id = message.guild.id

            if id in data.get("vxtwitter", []):
                twitter_alt = "https://vxtwitter.com"
            elif id in data.get("fxtwitter", []):
                twitter_alt = "https://fxtwitter.com"
            elif id in data.get("niggerx", []):
                twitter_alt = "https://niggerx.com"
            else: # default
                twitter_alt = "https://niggerx.com"
        except:
            twitter_alt = "https://niggerx.com"

        ###
        ### Quick info
        ###
        ### VXTwitter now adds garbage political data to
        ### the stuff it processes. E.g. you can see someone
        ### say the hard-R N-Word, and have a happy little
        ### 41-er emoji added to it.
        ###
        ### As of March 31st, 2025, VXTiktok is not
        ### compromised.
        ###
        ### - - - UPDATE 03/04/2025 - - -
        ###
        ### VXTwitter seemingly removed the political data.
        ###

        replacements = {
            "https://x.com": twitter_alt,
            "https://www.x.com": twitter_alt,
            "https://twitter.com": twitter_alt,
            "https://www.twitter.com": twitter_alt,
            #"https://fxtwitter.com": twitter_alt,
            #"https://www.fxtwitter.com": twitter_alt,  # ALLEGEDLY the creator of fxTwitter has/had report bots
            #"https://vxtwitter.com": twitter_alt,
            #"https://www.vxtwitter.com": twitter_alt,  # Creator of vxTwitter added garbage political data to posts - as of 03/April/2025, the political stuff is gone.
            #"https://niggerx.com": twitter_alt,
            #"https://www.niggerx.com": twitter_alt, # NiggerX is missing a lot of posts.
            "https://girlcockx.com": twitter_alt,
            "https://www.girlcockx.com": twitter_alt, # No. Just, no.
            "https://tiktok.com": tiktok_alt,
            "https://www.tiktok.com": tiktok_alt,
            "https://instagram.com": instagram_alt,
            "https://www.instagram.com": instagram_alt,
            "https://pixiv.net": pixiv_alt,
            "https://www.pixiv.net": pixiv_alt,
            "https://youtube.com/shorts/": youtube_alt,
            "https://www.youtube.com/shorts/": youtube_alt,
            "https://youtu.be/": youtube_alt,
            "https://www.youtu.be/": youtube_alt,
        }

        final_list = []
        for link in links:
            # Perform replacements
            for original, replacement in replacements.items():
                if link.startswith(original):
                    final_list.append(link.replace(original, replacement, 1))  # Replace only the first occurrence
                    has_embed = True
                    break

        # Remove embeds from the original message
        if has_embed:
            await asyncio.sleep(0.25) # SLOWDOWN to let embeds load. Default is 1, but testing with lower values.
            message = await message.channel.fetch_message(message.id)
            await message.edit(suppress=True)

        # Only send the first post
        if final_list:
            await message.channel.send(final_list[0])
    

    ### Webm Converter ###

    # Check if it has *any* attachments
    if message.attachments:
        Converter = WebmConverter()
        await Converter.check_for_webm_attachment(discord_message = message, channel_id = message.channel.id)

        


class WebmConverter(commands.Cog):
    def __int__(self, bot):
        self.bot = bot
        self._last_member = None
    DOWNLOAD_DIR = "webm_downloads"
    try:
        channelID # type: ignore
    except:
        channelID = 123

    ### Basic things, these will be called on an already running subprocess.to_thread() thread instead of the main thread
    # Get the video framerate
    async def get_video_frame_rate(file_path: str):
        """
        Extracts framerate as `int` from a video\n
        `file_path` defines the path to the video as a `str`.\n
        Returns `-1` on error
        """
        command = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "json", file_path]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            data = json.loads(result.stdout)
            frame_rate = data['streams'][0]['r_frame_rate']
            numerator, denominator = frame_rate.split('/')
            return int(numerator) / int(denominator)
        else:
            print(f"Error: Unable to get video frame rate. Return Code: {result.returncode}")
            return -1

    # Check if the video size is under the file limit as defined under DISCORD_FILE_LIMIT and returns a bool
    def is_file_under_limit(file_path, file_limit = DISCORD_FILE_LIMIT):
        """
        Checks if the file is under the defined file limit and returns `bool`.\n
        `file_limit` defines the file limit in megabytes as an `int`. By default slightly lower than the actual file limit, defined under `DISCORD_FILE_LIMIT`.
        """
        max_size = DISCORD_FILE_LIMIT * 1024 * 1024
        file_size = os.path.getsize(file_path)
        return file_size < max_size

    def get_video_resolution(video_path):
        """
        Gets the video resolution and returns a touple `width, height`: `int, int`.\n
        `video_path` defined the path to the video as a `str`.
        """
        # Run FFprobe to get video stream info
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", 
             "stream=width,height", "-of", "csv=s=x:p=0", video_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        # Parse the result
        resolution = result.stdout.decode('utf-8').strip()
        width, height = map(int, resolution.split('x'))

        return width, height

    def video_is_divisible_by_2(video_path):
        """
        Checks if the video width and height are divisible by 2 and returns a `bool`.\n
        `video_path` defines the path to the video as a `str`.
        """
        width, height = WebmConverter.get_video_resolution(video_path)
        return width % 2 == 0 and height % 2 == 0

    async def download_attachment(attachment: discord.Attachment):
        """
        Downloads an attachment to the folder defined in `WebmConverter.DOWNLOAD_DIR` and returns `file_path` as `str`, and `None` in case of an error.\n
        `attachment` is a `discord.Attachment`.
        """
        # Ensure the download directory exists
        if not os.path.exists(WebmConverter.DOWNLOAD_DIR):
            os.makedirs(WebmConverter.DOWNLOAD_DIR)

        # Define the path where the file will be saved
        file_path = os.path.join(WebmConverter.DOWNLOAD_DIR, attachment.filename)

        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as response:
                if response.status == 200:
                    with open(file_path, 'wb') as f:
                        f.write(await response.read())
                    print(f'Successfully downloaded {attachment.filename} to {file_path}')
                    return file_path
                else:
                    print(f'Failed to download {attachment.filename}, status code: {response.status}')
                    return None

    async def check_for_webm_attachment(self, discord_message: discord.Message, channel_id: int, return_result: bool = False):
        """
        Takes a message and checks if there are any webm videos.\n
        `message` is a `discord.Message`. Should be called after a `if message.attachments` check.\n
        `return_result` (default: False) checks whether it should return webm videos as a `touple list` with each touple consisting of the `command` and a `video_file_path` pointing to the final video location, or if it should call `WebmConverter.Convert_Webm`.
        """
        webm_video_list = []
        # Check for attachments in the message
        for attachment in discord_message.attachments:
            if attachment.filename.lower().endswith('.webm'):
                print(f'Found a WebM attachment: {attachment.filename}')
                # Download the WebM file
                file_path = await WebmConverter.download_attachment(attachment) # Await to wait until it is finished. Necessary.
                file_name, ext = os.path.splitext(file_path)
                output_name = f"{file_name}.mp4"
                framerate = await WebmConverter.get_video_frame_rate(file_path) # Await to wait until it is finished. Necessary.

                if WebmConverter.video_is_divisible_by_2(file_path):
                    command = [
                        "ffmpeg",
                        "-y",
                        "-fflags",
                        "+genpts",
                        "-i",
                        file_path,
                        "-r",
                        str(framerate),
                        output_name
                    ]
                else:
                    width, height = WebmConverter.get_video_resolution(file_path)
                    new_width = math.ceil(width / 2) * 2
                    new_height = math.ceil(height / 2) * 2
                    command = [
                        "ffmpeg",
                        "-y",
                        "-fflags",
                        "+genpts",
                        "-i",
                        file_path,
                        "-vf",
                        f"scale={new_width}:{new_height},pad={new_width}:{new_height}:(ow-iw)/2:(oh-ih)/2",
                        "-r",
                        str(framerate),
                        output_name
                    ]
                # Append the command and location as a touple to the webm_video_list
                webm_video_list.append((command, output_name))
        if return_result:
            return webm_video_list
        else:
            ConvertWebms = WebmConverter()
            await ConvertWebms.ConvertWebms(video_touple_list = webm_video_list, channel_id = channel_id)

    async def ConvertWebms(self, video_touple_list: list, channel_id):
        """
        Converts all videos to mp4 with compression to fit under Discord's File Size Limit.
        `video_touple_list` is a touple list structured as `(command, video_file_path)`.
        """
        interaction = discord.Interaction
        # Ensure all items in the list are tuples
        if all(isinstance(item, tuple) for item in video_touple_list):
            # Prepare a list to store running tasks
            conversion_tasks = []
            
            # Loop through all video command tuples
            for i, (command, video_file_path) in enumerate(video_touple_list):
                # Use asyncio's subprocess for non-blocking conversion
                conversion_tasks.append(self.run_ffmpeg_command(command, video_file_path))

            # Wait for all the conversions to finish
            await asyncio.gather(*conversion_tasks)

            channel_obj = client.get_channel(channel_id)

            # Send the converted videos after all are processed
            for _, video_file_path in video_touple_list:
                # Make sure the file exists before sending
                if os.path.exists(video_file_path):
                    await channel_obj.send(file=discord.File(video_file_path))
                    os.remove(video_file_path)
                    print(f"Successfully deleted {video_file_path}")
                    webm_path = Path(video_file_path).with_suffix('.webm')
                    if os.path.exists(webm_path):
                        os.remove(webm_path)
                        print(f"Successfully deleted {webm_path}")
                else:
                    print(f"Failed to locate converted file {video_file_path}")

        else:
            raise WebmConverter.WebmFailures.NotAToupleList(
                "The parameter `video_touple_list` does not consist exclusively of tuples. "
                "List consisting of tuples required."
            )

    async def run_ffmpeg_command(self, command, video_file_path):
        """
        Runs an individual ffmpeg command asynchronously.

        `command` is the list of ffmpeg command arguments.

        `video_file_path` is the output file path.
        """

        # Start the ffmpeg process
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Wait for the process to complete and capture stdout/stderr
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            print(f"Successfully converted {video_file_path}")
        else:
            print(f"Failed to convert {video_file_path}. Error: {stderr.decode()}")
    
    class WebmFailures:
        class NotAToupleList:
            """
            Generally raised if a touple list was expected but not received.
            """
            pass
        



@client.tree.command(name="doompilled")
async def doom(interaction: discord.Interaction):
    """ Send when someone is doompilling again """
    await interaction.response.send_message("You have no receding hairline, you have no negative chin, you have no bad physiognomy."
        "\n\nYou are a heterosexual man twisted by goyslob and kabbalah magic into a self-hating mockery of what you really are."
        "\n\nAll the “hate” you get is two-faced and half-hearted. Behind your back people love"
        " you. Your parents are happy and proud of you, your “friends” are worried about your depressed appearance"
        " behind closed doors."
        "\n\nMen are utterly jealous of you. Thousands of years of evolution have allowed men to sniff out competitors"
        " with incredible efficiency. Even incels who “doom” look retarded and pathetic to a man. Your bone structure is"
        " a dead giveaway of your superiority. And even if you manage to get a drunk guy to agree with you, he’ll turn tail"
        " and bolt the second he gets a look of your supreme, unrivaled physiognomy."
        "\n\nYou will be happy. You wrench out a fake frown every single morning and tell yourself it’s never going to be"
        " ok, but deep inside you feel the happiness creeping up like a flower, ready to lift you from the unbearable weight."
        "\n\nEventually it’ll be too much to bear - you’ll get a girlfriend, marry her, have a family, and plunge into the"
        " warm embrace of God. Your parents will love you, heartbroken but reliefed that they no longer have to live with the"
        " unbearable shame and disappointment of being inferior to you. They’ll bury you with a headstone marked with"
        " the millions of flowers of all who love you, and every passerby for the rest of eternity will know a legend is buried"
        " there. Your body will decay and go back to the dust, and all that will remain of your legacy is a family that"
        " is unmistakably yours.")

songs_list = []
songs_title = []
song_requester = []
song_length = []
song_urls = []
song_img = []
queue_v = ""
source_title = ""
playnow_requester = ""
playnow_img = ""
playnow_title = ""
playnow_length = 0
playnow_url = ""
firstsong = True

# IMPORTANT:
#
# If this bot starts acting up, examples
# include showing the wrong title, length,
# or thumbnail, you will have to restart
# the bot. That means the queue messed up
# and will inevitably start playing the
# wrong songs.
# Avoid requesting multiple songs
# at the same time. Queue command is
# slightly bugged, skip command *should*
# work. Please be aware that this is a
# rudamentary solution to play YT stuff
# after all big bots removed the feature.
# Stay safe and backup your fave vids!
#
# If you manage to fix the bugs, send
# me a message and I'll push it to main!
#
# ~ Strawb ^-^

class AloneInVoiceChatException(Exception): ...
class NotInVoiceChatException(Exception): ...

@client.tree.command(name="play")
async def _play(interaction: discord.Interaction, url: str):
    '''
    Play a song (must have URL)
    
    url: A string of the URL to the song. Example: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
    '''
    await interaction.response.defer()
    try:
        # Make sure the User is in a voice channel
        if interaction.user.voice == None:
            await interaction.edit_original_response(content = "You're not in a voice channel!")
            return

        if not "?v=" in url:
            await interaction.edit_original_response(content = "I cannot play playlists. Apologies :(")
            return
    
        vc: discord.VoiceClient
        vc = interaction.guild.voice_client

        if vc == None:
            await interaction.user.voice.channel.connect()
            vc = interaction.guild.voice_client

        print("DEBUG - Starting PLAY command!")
        if not vc.is_playing():
            print("DEBUG - Not playing.")
            if not songs_list:
                print("DEBUG - No playlist. Playing immediately...")
                file = search(url)[1]

                cur_songs_info = get_video_info(url)

                embed = discord.Embed(
                    title = "Natsukibot - Playlist",
                    color = discord.Color.from_rgb(r = 255, g = 0, b = 200)
                )
                embed.set_thumbnail(url = cur_songs_info[2])
                embed.add_field(
                    name = f"Now playing:",
                    value = f"[{cur_songs_info[0]}]({url})\nTotal Length: {timedelta(seconds = cur_songs_info[1])}"
                )

                # If bot is the only one in the voice channel, it will not play.
                if vc.channel.members == 1:
                    raise AloneInVoiceChatException
                # If the bot is not in a voice channel, it will not play either.
                if [ member.id for member in vc.channel.members ] == [ client.user.id ]:
                    raise NotInVoiceChatException
                
                await interaction.edit_original_response(embed = embed)

                playnow = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file, executable='ffmpeg', **ffmpeg_options))

                # In the case that the user disconnects while starting the play command, the bot will gracefully handle the exception.
                try:
                    await NatsukiActivity.set_streaming_activity(activity_text_data)
                    vc.play(playnow, after = lambda x: asyncio.run(NatsukiActivity.set_voice_activity(activity_text_data)))
                except discord.errors.ClientException:
                    asyncio.run(NatsukiActivity.set_voice_activity(activity_text_data))
                    await interaction.edit_original_response(content="Not connected to voice.")
                
                while vc.is_playing():
                    await asyncio.sleep(0.5)
                await play_next(interaction)
            else:
                embed = discord.Embed(
                    title = "Natsukibot - Playlist",
                    color = discord.Color.from_rgb(r = 255, g = 0, b = 200)
                )
                embed.add_field(
                    name = "Added to playlist:",
                    value = f"[{cur_songs_info[0]}]({url})\nTotal Length: {timedelta(seconds = cur_songs_info[1])}"
                )
                await interaction.edit_original_response(embed = embed)
                add_to_playlist(songs_list, url)
        else:
            cur_songs_info = get_video_info(url)
            embed = discord.Embed(
                title = "Natsukibot - Playlist",
                color = discord.Color.from_rgb(r = 255, g = 0, b = 200)
            )
            embed.add_field(
                name = "Added to playlist:",
                value = f"[{cur_songs_info[0]}]({url})\nTotal Length: {timedelta(seconds = cur_songs_info[1])}"
            )
            await interaction.edit_original_response(embed = embed)
            add_to_playlist(songs_list, url)



    #except discord.errors.HTTPException:
    #    await interaction.edit_original_response(content = "File too large, try again.")
    except PermissionError:
        await interaction.edit_original_response(content = "Permission err- wait what? Yea... \"Permission Error\". Huh.")
    except yt_dlp.DownloadError:
        await interaction.edit_original_response(content = "Video unavailable. Most likely because this content is age-restricted or not available in the host country.\nComplain to YouTube about this, I cannot fix this.")
    except AloneInVoiceChatException:
        await interaction.edit_original_response(content = "I'm alone in the voice channel. I'm not playing for myself.")
    except NotInVoiceChatException:
        await interaction.edit_original_response(content = "I'm not in a voice channel. *Where* do you expect me to play anything?")
    except OSError:
        await interaction.edit_original_response(content = "An error occoured, please try again.")

def add_to_playlist(playlist: list, url: str):
    playlist.append(url)

def remove_from_playlist(playlist: list, entry: int):
    try:
        playlist.remove(entry)
    except:
        pass

def get_video_info(url: str) -> tuple[str, int, bool]:
    """
    Get information about the video linked

    Arguments:
    @param url      URL to check

    @param Touple Index 0: Video Title
    @param Touple Index 1: Video Duration in Seconds
    @param Touple Index 2: Thumbnail
    """
    with yt_dlp.YoutubeDL(ytdl_format_options) as ydl:
        info_dict = ydl.extract_info(url, download = False)
        title = info_dict.get("title", None)
        length = info_dict.get("duration", None) # Duration in seconds
        thumbnail = info_dict.get("thumbnail", None)
        return title, length, thumbnail

@client.tree.command(name="remove")
async def remove(interaction: discord.Interaction, entry: int):
    ''' Remove entry from Playlist. Entry starts at 0 for the first entry, 1 for the second, and so on! '''
    await interaction.response.defer()

    if entry == 0:
        entry = 1
        dev_checker = True

    if songs_list.index(entry - 1):
        songs_list.remove(entry - 1) # Make up that Python counts from 0. This way, if you want the 5th song gone, and type in "5", it correctly removed the fifth song, which is at Python position 4 (0, 1, 2, 3, 4).
        if dev_checker:
            await interaction.edit_original_response(content = "Removed! By the way, I saw you're a programmer (or mistyped), so do note that the playlist starts at 1, not at 0.")
        else:
            await interaction.edit_original_response(content = "Removed!")

    elif songs_list.index(entry):
        await interaction.edit_original_response(content = f"There is no song at spot {entry}.")
    else:
        await interaction.edit_original_response(content = f"Sorry, I didn't find anything at the {entry}. position. I didn't find any at {entry + 1} either.")

@client.tree.command(name="playlist")
async def playlist(interaction: discord.Interaction):
    ''' Show the current playlist '''
    await interaction.response.defer()
    if not songs_list:
        await interaction.edit_original_response(content = f"The playlist is empty.")
    else:
        embed = discord.Embed(
            title = "Natsukibot - Playlist",
            color = discord.Color.from_rgb(r = 255, g = 0, b = 200)
        )

        i = 0
        for song in songs_list:
            if i < 10:
                
                cur_songs_info = get_video_info(song)

                embed.add_field(
                    name = f"{i + 1}. {cur_songs_info[0]}", # Title
                    value = f"[Link]({song})\nLength: {timedelta(seconds = cur_songs_info[1])}", # Link
                    inline  = False
                )
                i += 1
            else:
                pass
        embed.set_footer(text = f"Running on Germany's best internet at {(client.latency * 100):.3f}ms ping!")
        await interaction.edit_original_response(embed = embed)



@client.tree.command(name="stop")
async def stop(interaction : discord.Interaction):
    ''' Stop playing and clear the playlist '''
    await interaction.response.defer()
    voice: discord.VoiceClient
    voice = interaction.guild.voice_client
    if voice != None:
        await interaction.edit_original_response(content = "Cleared!")
        voice.stop()
        songs_list.clear()
    else:
        await interaction.edit_original_response(content = "I'm not connected to anything, dummy!")

@client.tree.command(name="disconnect")
async def _disconnect(interaction: discord.Interaction):
    ''' Disconnect from current VC '''
    await interaction.response.defer()
    vc: discord.VoiceClient
    vc = interaction.guild.voice_client
    if vc != None:
        await vc.disconnect(force=True)
        if interaction.guild.voice_client == None:
            await interaction.edit_original_response(content = "Disconnected. See you next time! :D")
        else:
            await interaction.edit_original_response(content = "Something unexpected happened, please disconnect me manually =)")
    else:
        await interaction.edit_original_response(content = "I'm not in a voice channel, dummy :P")



#@client.tree.command(name="right_now")
#async def right_now(interaction : discord.Interaction):
#    ''' See the currently playing song '''
#    await interaction.response.defer()
#    if interaction.guild.voice_client.is_playing() and playnow_title and playnow_requester and playnow_img:
#        embed = discord.Embed(color=0xff00cc)
#        embed.add_field(name="Playing:", value=f"`{playnow_title}` - Requested by `{playnow_requester}`")
#        embed.set_thumbnail(url=playnow_img)
#
#
#        await interaction.edit_original_response(embed=embed)
#    else:
#        await interaction.edit_original_response(content="I'm not playing anything right now, dummy!")



is_playing = False
skipped = False

async def play_next(interaction : discord.Interaction):
    try:
        vc: discord.VoiceClient
        vc = interaction.guild.voice_client
        if songs_list:
            if vc.is_playing():
                vc.stop()
            playnow = songs_list[0]
            file = search(playnow)[1]

            cur_songs_info = get_video_info(playnow)

            embed = discord.Embed(
                title = "Natsukibot - Playlist",
                color = discord.Color.from_rgb(r = 255, g = 0, b = 200)
            )
            embed.set_thumbnail(url = cur_songs_info[2])
            embed.add_field(
                name = f"Now playing:",
                value = f"[{cur_songs_info[0]}]({playnow})\nTotal Length: {timedelta(seconds = cur_songs_info[1])}"
            )

            # If bot is the only one in the voice channel, it will not play.
            if vc.channel.members == 1:
                raise AloneInVoiceChatException
            # If the bot is not in a voice channel, it will not play either.
            if [ member.id for member in vc.channel.members ] == [ client.user.id ]:
                raise NotInVoiceChatException

            await interaction.channel.send(embed = embed)

            remove_from_playlist(songs_list, songs_list[0])
            playnow = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file, executable='ffmpeg', **ffmpeg_options))

            # In the case that the user disconnects while starting the play command, the bot will gracefully handle the exception.
            try:
                vc.play(playnow)
                if not is_playing:
                    await NatsukiActivity.set_streaming_activity(activity_text_data)
            except discord.errors.ClientException:
                await interaction.edit_original_response(content="Not connected to voice.")
                return

            while vc.is_playing():
                await asyncio.sleep(0.5)
            await play_next(interaction)
        else:
            await interaction.channel.send(content = "Finished playing.")
            await NatsukiActivity.set_voice_activity(activity_text_data)

    except discord.errors.HTTPException:
        await interaction.channel.send(content = "File too large, try again.")
    except PermissionError:
        await interaction.channel.send(content = "Permission error... Weird.")
    except yt_dlp.DownloadError:
        await interaction.channel.send(content = "Video unavailable. Most likely because this content is age-restricted or not available in the host country.\nComplain to YouTube about this, I cannot fix this.")
    except AloneInVoiceChatException:
        await interaction.channel.send(content = "I'm alone in the voice channel. I'm not playing for myself.")
    except NotInVoiceChatException:
        await interaction.channel.send(content = "I'm not in a voice channel. *Where* do you expect me to play anything?")
    except OSError:
        await interaction.channel.send(content = "An error occoured, please try again.")



@client.tree.command(name="debugplay")
async def debugplay(interaction : discord.Interaction):
    await interaction.response.defer()

    await interaction.edit_original_response(content=
        f"|| DEBUG || - songs_list: {songs_list} \n" +
        f"|| DEBUG || - songs_title: {songs_title} \n" +
        f""
    )
        


@client.tree.command(name="skip")
async def skip(interaction : discord.Interaction):
    ''' Skip the currently playing song '''
    await interaction.response.defer()
    try:
        vc: discord.VoiceClient
        vc = interaction.guild.voice_client
        if vc.is_playing():
            vc.stop()
            await NatsukiActivity.set_voice_activity(activity_text_data)
    except Exception as e:
        await interaction.followup.send(content = "Error! Something happened!\n" + str(e))










et_names = ['User 1', 'User 2', 'User 3']
et_links = ['https://www.youtube.com/', 'https://www.google.com/', 'https://www.twitter.com/']
et_titles = ['Video 1', 'Video 2', 'Video 3']

@client.tree.command(name="embedtest")
async def embedtest(interaction : discord.Interaction):
    ''' Sends a testing embed. '''
    await interaction.response.defer()
    embed = discord.Embed(title = "YouTube Player", color = 0xff00cc)
    embed.set_author(name=interaction.client.user.display_name, icon_url=interaction.client.user.avatar, url="https://github.com/Wehrmachtserdbeere/Natsuki-Bot")
    j = 0
    for _ in et_names:
        embed.add_field(name=et_names[j], value=f"[{et_titles[j]}]({et_links[j]})", inline=False)
        j += 1
    embed.set_footer(text=f"Bot Version: {__version__} - Running on Germany's best internet connection!")

    await interaction.followup.send(embed=embed)



@client.tree.command(name="rr_play")
async def rr_play(interaction : discord.Interaction):
    ''' Play a song from my private collection ''' # <-- EDIT with your flavor text
    blacklist_data = load_longterm_lists()
    user_id = str(interaction.user.id)  # Convert user ID to string
    result = check_user_in_blacklist(user_id, blacklist_data)
    
    if result:
        uid, reason = result
        await interaction.response.send_message(f"Could not run command! User <@{user_id}> is blacklisted.\nReason: {reason}.")
    else:
        await interaction.response.defer()
        try:
            channel = interaction.user.voice.channel
            if interaction.guild.voice_client == None:
                await channel.connect(self_mute = False, self_deaf = True)
            vc = interaction.guild.voice_client
            if interaction.user.voice is None:
                interaction.edit_original_response(content = 'Hey, doofus, you\'re not in a voice channel! Join one first and *ten* ask me to play something!')
            mp3 = random.choice(mp3_path)
            try:
                print("Arrived here 1")
                audiofile = eyed3.load(mp3)
                try:
                    audTitle = audiofile.tag.title
                except AttributeError:
                    audTitle = "Unknown Title"
                try:
                    audArt = audiofile.tag.artist
                except AttributeError:
                    audArt = "Unknown Artist"
                try:
                    audAlbum = audiofile.tag.album
                except AttributeError:
                    audAlbum = "Unknown Album"

                process = await asyncio.create_subprocess_shell(
                    f'ffmpeg -i "{mp3}" -f s16le -ar 48000 -ac 2 pipe:1',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                stdout, stderr = await process.communicate()

                await interaction.edit_original_response(content = f"Song: {audTitle} | Artist: {audArt} | Album: {audAlbum}")

                song = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(mp3))

                await NatsukiActivity.set_streaming_activity(activity_text_data)
                vc.play(song, after=lambda x: asyncio.run(NatsukiActivity.set_voice_activity(activity_text_data)))

            except discord.errors.HTTPException:
                await interaction.edit_original_response(content = "File too large, try again.")
            except PermissionError:
                await interaction.edit_original_response(content = "Permission denied; Folder was probably auto-blocked, please try again.")
        except OSError:
            await interaction.edit_original_response(content = "An error occoured, please try again.")




@client.tree.command(name="about_me")
async def about_me(interaction : discord.Interaction, complexity : Literal['Simplified', 'Complex'] = 'Simplified'):
    '''Show general info about me'''
    embed = discord.Embed(colour = 0xff00cc, title = "Natsuki Bot", timestamp = datetime.now())
    embed.set_thumbnail(url = "https://img3.gelbooru.com/images/dc/b0/dcb07993482d9b81ab3d521c7d0d504a.jpg") # <-- EDIT this to your desired thumbnail
    embed.add_field(name = "Author:", value = f"[{__author__}](https://wehrmachtserdbeere.github.io/)", inline = False) # <-- EDIT this to your website
    embed.add_field(name = "Support:", value = f"[Support Server]({__support_discord__})", inline = False)
    embed.add_field(name = "Invite:", value = __invite_link__, inline = False)
    if complexity == 'Complex':
        embed.add_field(name = "Python Version:", value = f"`{sys.version}`", inline = False)
        embed.add_field(name = "Discord.py Version:", value = f"`{version('discord')}`", inline = False)
        embed.add_field(name = "FFMPEG Version:", value = f"`{version('ffmpeg')}`", inline = False)
    embed.set_footer(text = f"Bot Version: v{__version__}")
    await interaction.response.send_message(embed = embed)



@client.tree.command(name="neet_ai")
async def neet_ai(interaction : discord.Interaction, chat_message : str):
    ''' Chat with NEET Natsuki '''
    await interaction.response.defer(ephemeral = False, thinking = True)
    await asyncio.sleep(3)
    if random.randint(0,10) > 7:
        await interaction.followup.send(content = "Can you repeat that?")
    elif random.randint(0,10) > 7:
        await interaction.followup.send(content = "Huh?")
    else:
        await interaction.followup.send(content = "*She's not responding...*")



# The "-> dict" part is the return type. It's not necessary, but it's apparently good practice.
def waifugame_get_data(link : str) -> dict:
    '''
    Get gelbooru data of a card from WaifuGame because they block non-logged in users from accessing their API.
    
    As a side effect, this requires several unnecessary steps just to be able to find the actual source, which is fairly evil in my opinion, because it makes it harder to find the original artist while still using their copyrighted art.
    '''

    response = requests.get(link)

    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    image_html = soup.find("img", {"id": "cardInfoImg"})
    image_src = image_html["src"]

    print(f"Image source: {image_src}")

    # Turn Waifugame image link to Gelbooru API link
    match = re.search(r'G-(\d+)@', image_src)
    if match:
        image_id = match.group(1)
        new_url = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&id={image_id}"
        print(f"New URL: {new_url}")
    else:
        print("ID not found in the URL.")
        return None
    
    # Get XML
    response = requests.get(new_url)

    if response.status_code != 200:
        print("No Gelbooru data :(")
        return None
    
    # Request to String
    gelbooru_xml = response.text

    # Parse the XML
    root = ET.fromstring(gelbooru_xml)

    # Find the first post element
    post = root.find("post")

    # Convert it to a dictionary
    post_dict = {child.tag: child.text.strip() if child.text else "" for child in post}

    # Print the resulting dictionary
    print(post_dict)

    return post_dict

banned_tags = [ # <-- EDIT this with tags you want to BAN (i.E. no image shown, warning added)
    "transgender",
    "transgender_flag",
    "transgender_colors",
    "transsexual",
    "guro",
    "gore",
    "death",
    "murder",
    "beaten",
    "decapitated_head",
    "decapitation",
    "female_death",
    "necrophilia",
    "ryona",
    "severed_head",
    "skullfuck",
    "skull_fucking",
    "snuff",
    "scat",
    "shit",
    "scat_inflation",
    "poop",
    "pooping",
    "defecating",
    "shitting_self",
    "fart",
    "farting",
    "fart_cloud",
    "fart_fetish",
    "hyper_fart",
]

blocked_tags = [ # <-- EDIT this with tags you want to block (i.E. no image preview).
    "penis",
    "multiple_penises",
    "futanari",
    "futa_only",
    "yaoi",
    "hyper_ass",
    "giant_ass",
    "gigantic_breasts",
    "enormous_breasts",
    "massive_breasts",
    "colossal_breasts",
    "astronomical_breasts",
    "obese",
    "fat",
    "fat_man",
    "fat_woman",
    "plump"
]

if waifugame_enabled:
    @client.tree.command(name="waifugame_id_grabber")
    async def waifugame_id_grabber(interaction : discord.Interaction, card_id : int = -1, message_link : str = None):
        ''' Check a Waifugame Card's ID (currently non-functional due to Waifugame incompetency) '''
        await interaction.response.defer()

        result = check_user_in_blacklist(interaction.user.id, load_longterm_lists())
        if result:
            uid, reason = result
            await interaction.response.send_message(f"Could not run command! User <@{uid}> is blacklisted.\nReason: {reason}.")
            return

        # Prepare embed
        embed = discord.Embed()

        embed.title = "Waifugame Card Checker"

        if message_link:
            message_link_parts = message_link.split('/')
            channel_id = message_link_parts[-2]
            message_id = message_link_parts[-1]

            # Get the message
            message = await client.get_channel(int(channel_id)).fetch_message(int(message_id))

            # Get the first embed of the message
            message_embed = message.embeds[0]

            # Get the description of the embed
            message_description = str(message_embed.description)

            # Search for the card ID in the description
            match = re.search(r"№ (\d+)", message_description)

            card_id = int(match.group(1)) # Get the card ID


        if card_id != -1:
            link_to_card = f"https://waifugame.com/c/{card_id}"
            data = waifugame_get_data(link_to_card)
        else:
            await interaction.edit_original_response("Invalid Card ID. Please spam ping the developer to fix this.") # <-- EDIT this if you don't like to be notified of errors.



        nsfw = {
            "general": False,
            "questionable": True,
            "explicit": True
        }

        # Check if NSFW. By default, assume it is.
        isNSFW = nsfw.get(data["rating"], True)

        tags : str
        tags = data["tags"]
        tags = tags.split()

        isBanned = False
        isBlocked = False

        for tag in tags:
            if tag in banned_tags:
                isBanned = True
                break
            elif tag in blocked_tags:
                isBlocked = True
                break

        # Math that I am too stupid to understand
        gcd = math.gcd(int(data['width']), int(data['height']))
        ratio = f"{int(data['width']) // gcd}:{int(data['height']) // gcd}"

        # Source image, height and width, and ratio
        embed.add_field(
            name = "",
            value = f"Source: <{data['source']}>\n" +
                f"-# Width x Height: {data['width']} x {data['height']} ; Ratio: {ratio}",
        )

        # Rating
        embed.add_field(
            name = "",
            value = f"Rating: {str.capitalize(data['rating'])}",
            inline = False
        )

        # Hide image preview if NSFW in a non-NSFW channel
        if isBanned:
            embed.add_field(
                name = "",
                value = "Image: Not provided due to banned tags.",
                inline = False
            )
        elif isNSFW and not (interaction.channel.is_nsfw or isBlocked):
            embed.add_field(
                name = "",
                value = f"Image: (NSFW!) <{data['file_url']}>",
                inline = False
            )
        else:
            if isBlocked:
                embed.add_field(
                    name = "",
                    value = f"Image: (Blocked tags!) <{data['file_url']}>",
                    inline = False
                )
            else:
                embed.add_field(
                    name = "",
                    value = f"Image: {data['file_url']}",
                    inline = False
                )
                embed.set_image(
                    url = data['file_url']
                )

        # Basic Information
        embed.set_footer(
            text = f"Card ID: {card_id} ; Gelbooru ID: {data['id']} ; Uploader: {data['owner']}"
        )


        message = await interaction.edit_original_response(embed = embed)


trash_emoji = "🗑️"

@client.event
async def on_raw_reaction_add(payload : discord.RawReactionActionEvent):
    """ Handles reactions on messages even if the bot wasn't running when the message was sent. """
    if payload.emoji.name == trash_emoji:
        channel : discord.TextChannel
        channel = client.get_channel(payload.channel_id)
        message : discord.Message
        message = await channel.fetch_message(payload.message_id)

        if message.author.id == client.user.id and payload.user_id != client.user.id:
            print("User is not bot!")
            await message.delete()
            print("Deleted message!")















@client.tree.command(name="privacy")
async def privacy(interaction : discord.Interaction):
    '''See the Privacy Policy of the bot'''
    await interaction.response.send_message(file = discord.File("./privacypolicy.txt")) # <-- EDIT this to your privacy policy location.

bot_info = (
    "About me --- " + str(date.today()) + "\n" +
    "Running on Python: " + sys.version + "\n" +
    "Discord.py version: " + version('discord') + "\n" +
    "ffmpeg version: " + version('ffmpeg') + "\n" +
    "Bot version: " + __version__
)


@client.tree.command(name="bug_report")
async def bug_report(interaction : discord.Interaction, short_desc : str, steps_to_repeat : str, urgent : Literal['Yes', 'No'] = 'No'):
    blacklist_data = load_longterm_lists()
    user_id = str(interaction.user.id)  # Convert user ID to string
    result = check_user_in_blacklist(user_id, blacklist_data)
    
    if result:
        uid, reason = result
        await interaction.response.send_message(f"Could not run command! User <@{uid}> is blacklisted.\nReason: {reason}.")
    else:
        await interaction.response.defer()
        embed = discord.Embed(title="Bug Report")
        embed.set_thumbnail(url="https://i.imgur.com/W7FtFry.png")
        embed.add_field(name="**Short Description**", value="**"+short_desc+"**", inline=False)
        embed.add_field(name="Steps to Repeat", value=steps_to_repeat, inline=False)
        embed.add_field(name="Urgent?", value=urgent, inline=False)
        embed.set_footer(text=bot_info)
        channel = interaction.client.get_channel(1124728423810596914) # <-- EDIT this to the your own dev channel if you have one.
        user = interaction.user.name
        userid = interaction.user.id
        if urgent == "Yes":
            await channel.send(content=f"***__!!! URGENT !!!__***\nUser `{user}` - ID `{userid}` has sent a bug report!\n<@883054741263888384>", embed=embed)
        else:
            await channel.send(content=f"User `{user}` - ID `{userid}` has sent a bug report!", embed=embed)
        await interaction.followup.send("Sent bug report:", embed=embed)


@client.tree.command(name="blacklist_add")
async def blacklist_add(interaction: discord.Interaction, user_id: discord.Member, reason: str):
    ''' Bot Owner only command - Adds someone to blacklist using their UserID '''
    await interaction.response.defer()
    user_id_str = str(user_id.id)
    owner_id = 883054741263888384  # Replace with your user ID
    
    # Load the blacklist and whitelist data
    data: dict
    whitelist: list
    blacklist: list
    data = load_longterm_lists()
    admins = data.get("true_natsukians", [])
    whitelist = data.get("whitelist", [])
    blacklist = data.get("blacklist", [])

    if str(interaction.user.id) in admins:
        # Check if whitelist exists and if the user is in it
        if user_id_str in whitelist:
            await interaction.followup.send("User is in the whitelist and cannot be added to the blacklist.")
            return

        if user_id.id == owner_id:
            await interaction.followup.send("You cannot add the Owner to the blacklist. Nice try.")

        if user_id.id == client.user.id:
            await interaction.followup.send("You cannot add the Bot to the blacklist. Nice try.")

        # Add to blacklist if not already present
        if user_id_str not in blacklist:
            blacklist.append({"uid": user_id_str, "reason": reason})
            data["blacklist"] = blacklist
            save_data(data)
            await interaction.followup.send("Added to blacklist!")
        else:
            await interaction.followup.send("User is already in the blacklist.")
    else:
        await interaction.followup.send("You're not recognized as a Natsukian. You can't add people to the blacklist.")


#@client.tree.command(name="blacklist")
#async def blacklist(interaction : discord.Interaction):
#    ''' Show the Blacklist '''
#    await interaction.response.defer()
#
#    with open("longterm_lists.yaml", "r") as file:
#        data = yaml.safe_load(file)
#
#    embed = discord.Embed(title="Blacklist")
#
#    if "blacklist" in data and data["blacklist"]:
#        blacklist = data["blacklist"]
#
#        i = 0
#        for _ in blacklist:
#            username = interaction.client.get_user(blacklist[i])
#            if username == "None":
#                embed.add_field(name=f"Username: {username}", value=f"User ID: {blacklist[i]}", inline=False)
#            else:
#                embed.add_field(name=f"Unknown Username", value=f"User ID: {blacklist[i]}", inline=False)
#            i += 1
#    else:
#        embed.add_field(name=f"Empty Blacklist", value="Looks like the blacklist is empty. Awesome!", inline=False)
#    
#    await interaction.followup.send(embed=embed)


@client.tree.command(name="blacklist_remove")
async def blacklist_remove(interaction: discord.Interaction, user_id: discord.Member):
    ''' Bot Owner only command - Removes someone from blacklist using their UserID '''
    await interaction.response.defer()
    user_id_str = str(user_id.id)

    # Load the blacklist and whitelist data
    data: dict
    whitelist: list
    blacklist: list
    data = load_longterm_lists()
    admins = data.get("true_natsukians", [])
    whitelist = data.get("whitelist", [])
    blacklist = data.get("blacklist", [])

    if str(interaction.user.id) in admins:
        # Check if the user is in the whitelist
        if user_id_str in whitelist:
            await interaction.followup.send("User is in the whitelist and cannot be removed from the blacklist.")
            return

        # Remove from blacklist if present
        updated_blacklist = [entry for entry in blacklist if entry['uid'] != user_id_str]

        if len(updated_blacklist) < len(blacklist):
            data["blacklist"] = updated_blacklist
            save_data(data)
            await interaction.followup.send(f"Removed user {user_id_str} from the blacklist.")
        else:
            await interaction.followup.send("User not found in the blacklist.")
    else:
        await interaction.followup.send("You're not recognized as a Natsukian. You can't add people to the blacklist.")
        

async def print_latency(client):
    while True:
        print(f"Current ping: {(client.latency * 100):.3f}")
        await asyncio.sleep(ping_delay)


@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    await client.wait_until_ready()

    if member.id == client.user.id:
        return

    # Check if the bot is in a voice channel
    if before.channel is not None:
        vc_channel: discord.VoiceChannel = before.channel
    else:
        vc_channel: discord.VoiceChannel = after.channel

    # If the bot is in the voice channel (if client's user ID is in the list of member IDs)
    if client.user.id in [member.id for member in vc_channel.members]:
        # If there are no members in the voice channel apart from the bot. BOT IS COUNTED! Aka. size is "1" if bot is still in.
        if len(vc_channel.members) < 2:
            vc: discord.VoiceClient = vc_channel.guild.voice_client
            if vc is None:
                await NatsukiActivity.set_random_activity(activity_text_data)
                return  # Bot is not connected to a voice channel

            if vc.is_playing():
                # Run a loop until the bot finishes playing
                while vc.is_playing():
                    await asyncio.sleep(1)
                await NatsukiActivity.set_random_activity(activity_text_data)
                await vc.disconnect()
            else:
                # Disconnect the bot immediately
                await NatsukiActivity.set_random_activity(activity_text_data)
                await vc.disconnect()


@client.event
async def on_ready():      # Check if it runs
    
    global has_started

    # Print Guilds connected
    if print_guilds_connected:
        num = 0
        await client.tree.sync()
        print(f'{client.user} is connected to the following guilds:\n')
        for _ in client.guilds:
            guild = client.guilds[num]
            print(
                f'{num} - {guild.name} (id: {guild.id})'
            )
            num += 1
    
    if (has_started := has_started) is None:
        has_started = False

    # Print latency every 30 seconds
    # Don't do if disabled (set to -1)
    if not has_started:
        await NatsukiActivity.set_random_activity(activity_text_data)
        if not ping_delay == -1:
            asyncio.create_task(print_latency(client))
            has_started = True

    # Print ASCII image of Natsuki
    if enable_ascii:
        with open("./natsukis.json", encoding = "utf8") as file:
            image_data = json.load(file)
        image = random.choice(image_data["natsukis"])
        image_id = image["id"]
        image_ascii = image["image"]
        print(f"Choose image <<{image_id}>>")
        print(image_data["logo"])
        print(f"{image_ascii}")
    
    if not os.path.isfile("twitter_embedder_settings.json"):
        with open("twitter_embedder_settings.json", "w") as twitter_embedder_file:
            twitter_embedder_file.write(
                "{\n"
                "   \"vxtwitter\": [],\n"
                "   \"fxtwitter\": [],\n"
                "   \"niggerx\": []\n"
                "}"
            )


print("Please wait a few seconds for the bot to connect")

if is_debugging:
    client.run(botToken)
else:
    client.run(botToken, log_handler=None)