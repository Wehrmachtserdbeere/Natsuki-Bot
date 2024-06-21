# bot.py

import asyncio
import json
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
import yt_dlp # Yes, trying to add music streaming
from datetime import date
from importlib.metadata import version
import logging
import requests
from datetime import timedelta
import yaml
import subprocess

__author__ = "Strawberry Software"
__copyright__ = "Copyright 2019-2024"
__credits__ = [ "Strawberry", "An old Friend of Strawberry's" ]
__license__ = "MIT+NIGGER"
__version__ = "2.2.6"
__maintainer__ = "Strawberry"
__status__ = "Development"

__support_discord__ = "https://discord.gg/S8zDGPmXYv"

logging.basicConfig(level=logging.DEBUG)

print("Bot Started at " + datetime.now().strftime("%H:%M:%S"))

client = commands.Bot(command_prefix="n!", case_insensitive=True, intents=discord.Intents.all())

mp3_path = list(Path("D:\\Alles\\Alle Musik und Videos\\RR\\").rglob("*.mp3")) # <-- EDIT this to whatever folder your music is in.

@client.command()
@commands.guild_only()
@commands.is_owner()
@app_commands.default_permissions(manage_messages=True)
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
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
    return string.replace(" ", "_")

### Music

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


@client.tree.command(name="cute")                                                   # n!you_are_cute
async def you_are_cute(interaction: discord.Interaction) -> None:
    """ Tell me I'm cute """
    await interaction.response.send_message("I'm NOT cute!!!")


@client.tree.command(name="ping")                                  # n!ping
async def ping(interaction: discord.Interaction) -> None:
    """ Get my Ping """
    await interaction.response.send_message("Pong! `" + str(client.latency * 100) + "ms`")


@client.tree.command(name="img")                                   # Natsuki image from "Natsuki Worship" <-- Oh wow this is an old comment! Has to be from 2019! Thank God I don't store my images on Discord anymore :P.
async def img(interaction: discord.Interaction) -> None:
    """ Send an image of Natsuki """
    imgimg = "D:\\Alles\\Alle Bilder\\DDLC\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\DDLC")) # <-- EDIT this to any path with images you like.
    await interaction.response.send_message(file=discord.File(imgimg))


@client.tree.command(name="shdf")                                   # Get image <-- Can ignore unless you find a meaning behind "shdf".
async def shdf(interaction: discord.Interaction):
    """ Send an SHDF image """
    shdfimg = "D:\\Alles\\Alle Bilder\\Anime People doing Wholesome Thing\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Anime People doing Wholesome Thing")) # <-- EDIT this to any path with images you like.
    await interaction.response.send_message(file=discord.File(shdfimg))

B = ":black_large_square:"
b = B
W = ":white_large_square:"
w = W
R = ":red_square:"
r = R


@client.tree.command(name="draw")
async def draw(interaction: discord.Interaction, drawmessage: str):
    """ Draw something with B, W, R, and . """
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
async def oracle(interaction: discord.Interaction, amount_of_letters: int):
    """ Terry A. Davis' Oracle """
    await interaction.response.send_message(functools.reduce(lambda line, word: line + f"{word} ", (random.choice(oraclewords) for _ in range(amount_of_letters)), str()))


# Oracle German
@client.tree.command(name="oracle_ger")
async def oracle_ger(interaction: discord.Interaction, amount_de: int):
    """ Terry A. Davis' Oracle but in German """
    await interaction.response.send_message(functools.reduce(lambda line, word: line + f"{word} ", (random.choice(oracle_de_words) for _ in range(amount_de)), str()))


@client.tree.command(name="fate")                           # Fate image
async def fate(interaction: discord.Interaction):
    """ Get an image of the anime \"Fate\" """
    fateimg = "D:Alles\\Alle Bilder\\Fate\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Fate")) # <-- EDIT this if you have a folder for Fate images.
    await interaction.response.send_message(file=discord.File(fateimg))


@client.tree.command(name="tanya")                           # Tanya image from
async def tanya(interaction: discord.Interaction):
    """ Get an image of Tanya von Degurechaff """
    tanyaimg = "D:\\Alles\\Alle Bilder\\Tanya Degurechaff\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Tanya Degurechaff")) # <-- EDIT this if you have a folder for images of anything called "tanya".
    await interaction.response.send_message(file=discord.File(tanyaimg))


@client.tree.command(name="tomboy")                                   # Get image
async def tomboy(interaction: discord.Interaction):
    """Mmm tomboy abs yummy licky """
    tomboyimg = "D:\\Alles\\Alle Bilder\\Anime Tomboys\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Anime Tomboys")) # <-- EDIT this to your Anime Tomboys folder. I know you have one.
    await interaction.response.send_message(file=discord.File(tomboyimg))


@client.tree.command(name="fap")
async def fap(interaction: discord.Interaction):
    """ Send this if someone mentions porn """
    await interaction.response.send_message(
    "\n☝️ أيها الإخوة ، لا تشاهدوا الإباحية. إنه يخيب آمال الرب. ☝"
    "\n☝️وروsو ، فحش مه ګورئ. دا څښتن مایوسه کوي. ☝️\n"
    "☝️Αδέλφια, μην βλέπετε πορνό. Απογοητεύει τον Κύριο. ☝\n"
    "☝️Fratres, nolite vigilare sex. Decipit Dominum. ☝️\n"
    "☝️Братья, не смотрите порно. Это разочаровывает Господа. ☝\n️"
    "☝️Brothers, do not watch porn. It disappoints the Lord.☝️\n"
    )


@client.tree.command(name="rem")
async def rem(interaction: discord.Interaction):
    """ Get an image of Rem """
    remimg = "D:\\Alles\\Alle Bilder\\Rem\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Rem\\")) # <-- EDIT this to images of Rem.
    await interaction.response.send_message(file=discord.File(remimg))


@client.tree.command(name="klk")
async def klk(interaction: discord.Interaction):
    """ Get an image of Kill la Kill """
    klkimg = "D:\\Alles\\Alle Bilder\\Kill la Kill\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Kill la Kill\\")) # <-- EDIT this to Kill La Kill images.
    await interaction.response.send_message(file=discord.File(klkimg))


@client.tree.command(name="rmeme")
async def rmeme(interaction: discord.Interaction):
    """ Get one of Strawb's memes """
    await interaction.response.defer()
    try:
        mp4 = "D:\\Alles\\Alle Musik und Videos\\" + random.choice(os.listdir("D:\\Alles\\Alle Musik und Videos\\")) # <-- EDIT this to a path with video memes.
        await interaction.followup.send(file=discord.File(mp4))
    except discord.errors.HTTPException:
        await interaction.followup.send("File too large, try again.")
    except PermissionError:
        await interaction.followup.send("Permission denied; Folder was auto-blocked, please try again.")


folders = [
    "D:\\Alles\\Alle Musik und Videos\\RR under 8MB\\", # <-- EDIT this to your RR music. Feel free to find meaning behind "RR".
    ""
]

@client.tree.command(name="rr")
async def rr(interaction: discord.Interaction):
    """ Get a NS song (Most likely German) """
    await interaction.response.defer()
    try:
        #mp3 = "D:\\Alles\\Alle Musik und Videos\\RR under 8MB\\" + random.choice(os.listdir("D:\\Alles\\Alle Musik und Videos\\RR under 8MB\\"))
        mp3 = random.choice(mp3_path)
        #print(f'RR Requested | Song: {mp3}')
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
            #await interaction.followup.send(f"Song: {audTitle} | Artist: {audArt} | Album: {audAlbum}")
            print(f"RR music -- {mp3}")
        except discord.errors.HTTPException:
            await interaction.followup.send("File too large, try again.")
        except PermissionError:
            await interaction.followup.send("Permission denied; Folder was probably auto-blocked because of lewdness, please try again.")
    except OSError:
        await interaction.followup.send("An error occoured, please try again.")


@client.tree.command(name="christ_chan")
async def christ_chan(interaction: discord.Interaction):
    """ Get an image of Christ-Chan """
    chrImg = "D:\\Alles\\Alle Bilder\\Christ-chan\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Christ-chan\\")) # <-- EDIT this to a path with images of Christ Chan. Not to be confused with Chris Chan.
    await interaction.response.send_message(file=discord.File(chrImg))


@client.tree.command(name="chan")
async def chan(interaction: discord.Interaction):
    """ Get an image of another Chan """
    chanImg = "D:\\Alles\\Alle Bilder\\Other Chans\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Other Chans\\")) # <-- EDIT this to a path with images of other -chan characters.
    await interaction.response.send_message(file=discord.File(chanImg))


@client.tree.command(name="megu")
async def megu(interaction: discord.Interaction):
    """ Get an image of Megumin """
    chanImg = "D:\\Alles\\Alle Bilder\\Megumin\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Megumin\\")) # <-- EDIT this to a path with Megumin images.
    await interaction.response.send_message(file=discord.File(chanImg))


@client.tree.command(name="safe")
async def safe(interaction: discord.Interaction, tags: str):
    """ Get an image from Safebooru """
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
async def gel(interaction: discord.Interaction, tags: str, nsfw: Literal['safe', 'safe and questionable', 'questionable', 'explicit only', 'all'] = 'safe', gendered: Literal['Female Only', 'Male Only', 'Any'] = 'Any'):
    """ Get an image from Gelbooru (SFW only) """
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










@client.tree.command(name="bleachbooru")
async def bleach(interaction: discord.Interaction, tags: str, nsfw: Literal['safe', 'questionable and safe (high filter)', 'questionable and safe (low filter)', 'all', 'explicit only'] = 'safe'): # <-- This site sucks btw, horrid API, barely any documentation, not even filtered correctly. Be careful, even "safe" will often return porn.
    """ Get an image from Bleachbooru (Severe NSFW warning) """
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
    #try:
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
async def on_message(message):
    if message.author == client.user:
        return

    flag = False
    message_lowsplit = message.content.lower().split()

    flag = any(substring in message_lowsplit for substring in list_)

    for word in message_lowsplit:
        if word.startswith('u'):
            if word.endswith('h'):
                if re.search('o', word):
                    if not re.search('[a-gi-np-tv-z]', word):
                        await message.add_reaction('😭')

    if flag:
        await message.add_reaction('😭')

DOWNLOAD_DIR = ".\\webm_downloads"

def get_video_frame_rate(file_path):
    command = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "json", file_path]
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        data = json.loads(result.stdout)
        frame_rate = data['streams'][0]['r_frame_rate']
        numerator, denominator = frame_rate.split('/')
        return int(numerator) / int(denominator)
    else:
        print("Error: Unable to get video frame rate.")
        return None

def is_file_under_25mb(file_path):
    # 25MB in bytes
    max_size = 25 * 1024 * 1024  # 25 * 1024 * 1024 = 26214400 bytes
    file_size = os.path.getsize(file_path)
    return file_size < max_size

@client.event
async def on_message(message):
    # Avoid responding to the bot's own messages
    if message.author == client.user:
        return

    has_webm_flag = False
    has_file_too_large = False
    conversion_errors = []
    attachment_list = []
    files_list = []

    # Check for attachments in the message
    for attachment in message.attachments:
        if attachment.filename.lower().endswith('.webm'):
            has_webm_flag = True
            print(f'Found a WebM attachment: {attachment.filename}')
            # Download the WebM file
            file_path = await download_attachment(attachment)
            file_name, ext = os.path.splitext(file_path)
            output_name = f"{file_name}.mp4"
            framerate = get_video_frame_rate(file_path)

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

            try:
                subprocess.run(command, check = True)
                os.remove(file_path) # Delete original file

                files_list.append(output_name)
                
                if is_file_under_25mb(output_name):
                    attachment_list.append(discord.File(fp = f"{output_name}", spoiler = attachment.is_spoiler()))
                else:
                    if not has_file_too_large:
                        has_file_too_large = True
                    conversion_errors.append(f"{output_name}")
                    print(f"File too large: {output_name}")
            except subprocess.CalledProcessError as e:
                print(f"ERROR: {e}")

    if has_webm_flag:
        if not has_file_too_large:
            await message.channel.send("Converted your webms!", files = attachment_list)
            for _ in files_list:
                os.remove(f"{_}")
        elif has_file_too_large:
            if attachment_list:
                await message.channel.send(f"Converted your webms, but there were some problems. The following file(s) were too large to send: {conversion_errors}", files = attachment_list)
                for _ in files_list:
                    os.remove(f"{_}")
            else:
                await message.channel.send(f"No webms were converted, whatever you sent was too large. You still don't compare with Strawb :P\nThe following file(s) were too large: {conversion_errors}")
        else:
            await message.channel.send("Error")


def download_video(url, download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    # Extracting the filename from the URL to use as the file name
    filename = url.split('/')[-1]
    file_path = os.path.join(download_folder, filename)
    
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Download of video completed: {file_path}")
        return file_path
    else:
        print(f"Failed to retrieve video. Status code: {response.status_code}")
        return None

@client.tree.command(name="convert_webm")
async def convert_webm(interaction: discord.Interaction, video_url : str, silent : bool = False, format : Literal['mp4', 'gif'] = 'mp4'):
    await interaction.response.defer(ephemeral = silent, thinking = True)
    if video_url is None:
        await interaction.edit_original_response("Please add a link to a video.")
        return
    
    has_webm_flag = False
    has_file_too_large = False
    conversion_errors = []

    if video_url is not None:
        # Download the WebM file
        file_path = download_video(video_url, os.path.abspath(os.getcwd()) + "\\webm_downloads")
        has_webm_flag = True
        file_name, ext = os.path.splitext(file_path)
        framerate = get_video_frame_rate(file_path)

        if format == "mp4":
            output_name = f"{file_name}.mp4"
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
        elif format == "gif":
            output_name = f"{file_name}.gif"
            command = [
                "ffmpeg",
                "-y",  # Overwrite output files without asking
                "-i", file_path,  # Input file path
                "-r", str(framerate),  # Frame rate (frames per second) of the output GIF
                "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",  # Ensure width and height are divisible by 2 (required by GIF)
                "-f", "gif",  # Output format is GIF
                output_name  # Output file name
            ]

        try:
            subprocess.run(command, check = True)
            os.remove(file_path) # Delete original file

            if is_file_under_25mb(output_name):
                video_to_be_sent = discord.File(fp = f"{output_name}")
            else:
                if not has_file_too_large:
                    has_file_too_large = True
                conversion_errors.append(f"{output_name}")
                print(f"File too large: {output_name}")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: {e}")

    if has_webm_flag:
        if not has_file_too_large:
            await interaction.followup.send("Converted your webms!", file = video_to_be_sent, ephemeral = silent)
            os.remove(f"{output_name}")
            print("Successfully converted video.")
        elif has_file_too_large:
            await interaction.edit_original_response(f"No webms were converted, whatever you sent was too large. You still don't compare with Strawb :P\nThe following file(s) were too large: {conversion_errors}")
        else:
            await interaction.edit_original_response("Error")



async def download_attachment(attachment):
    # Ensure the download directory exists
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    # Define the path where the file will be saved
    file_path = os.path.join(DOWNLOAD_DIR, attachment.filename)

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

# MUSIC

#@client.tree.command(name="play")
#async def play(*, interaction : discord.Interaction, myurl: str):
#
#    ffmpeg_options = {'options': '-vn'}
#    ydl_opts = {'format': 'bestaudio'}
#    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#        song_info = ydl.extract_info(myurl, download=False)
#    
#    if not interaction.is_disconnected:
#        channel = interaction.user.voice.channel
#        vc = await channel.connect()
#
#    await vc.play(discord.FFmpegPCMAudio(song_info["url"], **ffmpeg_options)) 

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
# Avoid requesting songs
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

@client.tree.command(name="play")
async def _play(interaction : discord.Interaction, url : str):
    ''' Play a song (must have URL) '''
    await interaction.response.defer()
    try:
        if interaction.user.voice is None:
            await interaction.edit_original_response(content = 'Hey, doofus, you\'re not in a voice channel! Join one first and *ten* ask me to play something!')
            raise Exception("User not in Voice Chat.")
        channel = interaction.user.voice.channel
        print("Arrived here 0.5")
        if interaction.guild.voice_client == None:
            await channel.connect(self_mute = False, self_deaf = True)
        vc = interaction.guild.voice_client
        guild = interaction.guild_id
        print("Arrived here 0.75")
        song_urls.append(url)
        video, source, source_title, source_length, thumbnail = search(url)
        songs_title.append(source_title)
        song_requester.append(interaction.user)
        song_length.append(source_length)
        song_img.append(thumbnail)
        #if vc.is_playing():
        #    embed = discord.Embed(color = 0xff00cc)
        #    embed.set_thumbnail(url=song_img[0])
        #    embed.add_field(name="Natsuki Player", value=f"Queued:\n\t[{source_title}]({song_urls[0]})\nRequested by: `{song_requester[0]}`\n\t{timedelta(seconds=song_length[0])}")
        #    await interaction.edit_original_response(embed=embed)
        #    break
        try:
            while song_urls:
                print("Arrived here 2")
                if not vc.is_playing():
                    songs_list.append(source)
                    playnow_requester = song_requester[0]
                    playnow_length = song_length[0]
                    playnow_url = song_urls[0]
                    playnow_img = song_img[0]
                    playnow_title = songs_title[0]
                    embed = discord.Embed(color = 0xff00cc)
                    embed.set_thumbnail(url=playnow_img)
                    embed.add_field(name="Natsuki Player", value=f"Now playing:\n\t[{playnow_title}]({playnow_url})\nRequested by\n\t`{playnow_requester}`\n\tLength: {timedelta(seconds=playnow_length)}")
                    await interaction.edit_original_response(embed=embed)
                    playnow = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(songs_list[0], executable='ffmpeg', **ffmpeg_options))
                    
                    print(f"----- DEBUG -----\n"
                        f"songs_list: {songs_list}\n"
                        f"playnow_requester: {playnow_requester}\n"
                        f"playnow_url: {playnow_url}\n"
                        f"playnow_img: {playnow_img}\n"
                        f"playnow_title: {playnow_title}\n"
                        f"----- END OF PLAYNOW -----\n"
                        f"----- SONG_URLS -----\n"
                    )
                    print(song_urls)
                    print(f"\n----- SONG_TITLE -----\n")
                    print(songs_title)
                    print(f"\n----- SONG_REQUESTER -----\n")
                    print(song_requester)
                    print(f"\n----- SONG_LENGTH -----\n")
                    print(song_length)
                    print(f"\n----- SONG_IMG -----\n")
                    print(song_img)
                    print(f"\n----- END DEBUG LOOP -----\n")
                    
                    if songs_list:
                        del songs_list[0]
                    if songs_title:
                        del songs_title[0]
                    if song_urls:
                        del song_urls[0]
                    if song_length:
                        del song_length[0]
                    if song_requester:
                        del song_requester[0]
                    if song_img:
                        del song_img[0]
                    #if url:
                    #    del url
                    vc.play(playnow, after=play_next(interaction))
                    print("|| DEBUG || - songs_list: " + str(songs_list))
                    print("|| DEBUG || - songs_title: " + str(songs_title))
                else:
                    print("\n----- SONG_URLS -----\n")
                    print(*song_urls)
                    print(f"\n----- SONG_TITLE -----\n")
                    print(*songs_title)
                    print(f"\n----- SONG_REQUESTER -----\n")
                    print(*song_requester)
                    print(f"\n----- SONG_LENGTH -----\n")
                    print(*song_length)
                    print(f"\n----- SONG_IMG -----\n")
                    print(*song_img)
                    print(f"\n----- END DEBUG LOOP -----\n")
                    await interaction.edit_original_response(content = 'Added "' + source_title + '" to queue.')
                while vc.is_playing():
                    await asyncio.sleep(1)
        except discord.errors.HTTPException:
            await interaction.edit_original_response(content = "File too large, try again.")
        except PermissionError:
            await interaction.edit_original_response(content = "Permission err- wait what? Yea... \"Permission Error\". Huh.")
        except yt_dlp.DownloadError:
            await interaction.edit_original_response(content = "Video unavailable. Most likely because this content is not available in the host country.")
        #except Exception as e:
        #    await interaction.edit_original_response(content = "Error: " + str(e))
    except OSError:
        await interaction.edit_original_response(content = "An error occoured, please try again.")



@client.tree.command(name="stop")
async def stop(interaction : discord.Interaction):
    ''' Stop playing and disconnect '''
    await interaction.response.defer()
    voice = interaction.guild.voice_client
    if voice != None:
        await interaction.followup.send(content = "Sorry, I'll go...")
        interaction.guild.voice_client.cleanup()
        await interaction.guild.voice_client.disconnect()
        interaction.guild.voice_client.cleanup()
    else:
        await interaction.followup.send(content = "I'm not connected to anything, dummy!")

@client.tree.command(name="queue")
async def queue(interaction : discord.Interaction):
    ''' See the Queue '''
    queue_v = ""
    i = 0
    await interaction.response.defer()
    try:
        if songs_title:
            

            embed = discord.Embed(title = "YouTube Player", color = 0xff00cc)
            embed.set_author(name=interaction.client.user.display_name, icon_url=interaction.client.user.avatar, url="https://github.com/Wehrmachtserdbeere/Natsuki-Bot")
            j = 0
            embed.add_field(name=playnow_requester, value=f"[{playnow_title}]({playnow_url}) - {timedelta(seconds=playnow_length)}", inline=False)
            for _ in song_urls:
                embed.add_field(name=song_requester[j], value=f"[{songs_title[j]}]({song_urls[j]}) - {timedelta(seconds=song_length[j])}", inline=False)
                j += 1
            embed.set_footer(text=f"Bot Version: {__version__} - Running on Germany's best internet connection since 1941!")
            await interaction.edit_original_response(embed=embed)
        else:
            await interaction.edit_original_response(content="Queue is empty!")
    except Exception as e:
        await interaction.edit_original_response(content="Error! - " + str(e))



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




skipped = False

def play_next(interaction : discord.Interaction):
    try:
        if len(songs_list) >= 1:
            firstsong = False
            print("|| DEBUG || - songs_list: " + str(songs_list))
            print("|| DEBUG || - songs_title: " + str(songs_title))
            print(songs_list[0], "new song")
            print("|| DEBUG || - songs_list: " + str(songs_list))
            print("|| DEBUG || - songs_title: " + str(songs_title))

            #ctx.guild.voice_client.cleanup()
            discord.FFmpegAudio.cleanup()
            interaction.guild.voice_client.stop()
            #_play
    except Exception as e:
        print("|| ERROR || - " + str(e))


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
        voice = interaction.guild.voice_client
        if voice.is_playing():
            voice.stop()
    except Exception as e:
        await interaction.followup.send(content = "Error! Something happened! \n" + str(e))










et_names = ['User 1', 'User 2', 'User 3']
et_links = ['https://www.youtube.com/', 'https://www.google.com/', 'https://www.twitter.com/']
et_titles = ['Video 1', 'Video 2', 'Video 3']

@client.tree.command(name="embedtest")
async def embedtest(interaction : discord.Interaction):
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
    ''' Play a song from my private collection '''
    await interaction.response.defer()
    try:
        channel = interaction.user.voice.channel
        print("Arrived here 0.5")
        if interaction.guild.voice_client == None:
            await channel.connect(self_mute = False, self_deaf = True)
        vc = interaction.guild.voice_client
        if interaction.user.voice is None:
            interaction.edit_original_response(content = 'Hey, doofus, you\'re not in a voice channel! Join one first and *ten* ask me to play something!')
        print("Arrived here 0.75")
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

            print("Arrived here 2")
            print(mp3)
            await interaction.edit_original_response(content = f"Song: {audTitle} | Artist: {audArt} | Album: {audAlbum}")
            print("Arrived here 3")
            
            song = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(mp3))
            
            vc.play(song, after=lambda x: print("Done"))

            print(f"FFmpeg stderr: {stderr.decode()}")

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
    embed.add_field(name = "Support:", value = f"[Support Server](https://discord.gg/S8zDGPmXYv)", inline = False) # <-- EDIT this to your support site.
    if complexity == 'Complex':
        embed.add_field(name = "Python Version:", value = f"`{sys.version}`", inline = False)
        embed.add_field(name = "Discord.py Version:", value = f"`{version('discord')}`", inline = False)
        embed.add_field(name = "FFMPEG Version:", value = f"`{version('ffmpeg')}`", inline = False)
    embed.set_footer(text = f"Bot Version: `{__version__}`")
    await interaction.response.send_message(embed = embed)


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
    await interaction.response.defer()
    with open("longterm_lists.yaml", "r") as file: # <-- EDIT this to your yaml. Read the Readme for more information.
        data = yaml.safe_load(file)
    if "blacklist" in data and data["blacklist"]:
        blacklist = data["blacklist"]

        if interaction.user.id in blacklist:
            await interaction.followup.send("User blacklisted, command blocked.")
    else:
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
async def blacklist_add(interaction : discord.Interaction, user : str):
    ''' Bot Owner only command - Adds someone to blacklist using their UserID '''
    await interaction.response.defer()
    user = int(user)
    if interaction.user.id == 883054741263888384: # <-- EDIT this to your user ID

        with open("longterm_lists.yaml", "r") as file: # <-- EDIT to your yaml. Read the Readme for more information.
            data = yaml.safe_load(file)
        if "blacklist" in data and data["blacklist"]:
            blacklist = data["blacklist"]
        else:
            blacklist = []

        blacklist.append(user)

        data["blacklist"] = blacklist

        with open("longterm_lists.yaml", "w") as file:
            yaml.safe_dump(data, file)

        await interaction.followup.send("Added!")
    else:
        await interaction.followup.send("Sorry, but you are not the owner, and as thus cannot add people to the blacklist.")


@client.tree.command(name="blacklist")
async def blacklist(interaction : discord.Interaction):
    ''' Show the Blacklist '''
    await interaction.response.defer()

    with open("longterm_lists.yaml", "r") as file:
        data = yaml.safe_load(file)

    embed = discord.Embed(title="Blacklist")

    if "blacklist" in data and data["blacklist"]:
        blacklist = data["blacklist"]

        i = 0
        for _ in blacklist:
            username = interaction.client.get_user(blacklist[i])
            if username == "None":
                embed.add_field(name=f"Username: {username}", value=f"User ID: {blacklist[i]}", inline=False)
            else:
                embed.add_field(name=f"Unknown Username", value=f"User ID: {blacklist[i]}", inline=False)
            i += 1
    else:
        embed.add_field(name=f"Empty Blacklist", value="Looks like the blacklist is empty. Awesome!", inline=False)
    
    await interaction.followup.send(embed=embed)


@client.tree.command(name="blacklist_remove")
async def blacklist_remove(interaction : discord.Interaction, user : str):
    ''' Bot Owner only command - Removes someone from blacklist '''
    await interaction.response.defer()
    user = int(user)
    if interaction.user.id == 883054741263888384: # <-- EDIT this to your user ID

        with open("longterm_lists.yaml", "r") as file:
            data = yaml.safe_load(file)
        if "blacklist" in data and data["blacklist"]:
            blacklist = data["blacklist"]
            if user in blacklist:
                blacklist.remove(user)
                with open("longterm_lists.yaml", "w") as file:
                    yaml.safe_dump(data, file)
                await interaction.followup.send("Removed!")
            else:
                await interaction.followup.send(f"{user} does not exist in the Blacklist.")
        else:
            blacklist = []
    else:
        await interaction.followup.send("Sorry, but you are not the owner, and as thus cannot add people to the blacklist.")
        




@client.event
async def on_ready():      # Check if it runs
    num = 0
    await client.tree.sync()
    print(f'{client.user} is connected to the following guilds:\n')
    for _ in client.guilds:
        guild = client.guilds[num]
        print(
            f'{num} - {guild.name} (id: {guild.id})'
        )
        num += 1

print("Please wait a few seconds for the bot to connect")

client.run(botToken)
input("Just checking if it printed anything above.")
