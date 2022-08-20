# bot.py
import logging

import aiohttp

if __name__ == "__main__":
    pass
import random
import typing
import os
import time
import discord
from discord import app_commands
import discord.ext
from discord.ext import commands
from pymep.realParser import parse
from oracle import oracle as oraclewords
from oracle_german import oracle_de as oracle_de_words
import functools
import asyncio
from discord.ext import commands
from botToken import botToken
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from linkespruche import ls_german
from linkespruche import ls_english
import youtube_dl
import socket
import tags
import eyed3
import datetime
import string
from bs4 import BeautifulSoup
import re
import schedule
from discord.ext.commands import Context, Greedy
from typing import Optional, Literal

client = commands.Bot(command_prefix="n!", case_insensitive=True, intents=discord.Intents.default())

youtube_dl.utils.bug_reports_message = lambda: ''

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
    'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
    'download': False,
}

ffmpeg_options = {
    'options': '-vn'
}


def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
    super().__init__(source, volume)

    self.requester = ctx.author
    self.channel = ctx.channel
    self.data = data

    self.uploader = data.get('uploader')
    self.uploader_url = data.get('uploader_url')
    date = data.get('upload_date')
    self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
    self.title = data.get('title')
    self.thumbnail = data.get('thumbnail')
    self.description = data.get('description')
    self.duration = self.parse_duration(int(data.get('duration')))
    self.tags = data.get('tags')
    self.url = data.get('webpage_url')
    self.views = data.get('view_count')
    self.likes = data.get('like_count')
    self.dislikes = data.get('dislike_count')
    self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

def shorten(string):
    return string.replace(" ", "_")

print("Initializing...")

@client.tree.command(name="cute")                                                   # n!you_are_cute
async def you_are_cute(interaction: discord.Interaction) -> None:
    """ Tell me I'm cute """
    await interaction.response.send_message("I'm NOT cute!!!")

@client.tree.command(name="ping")                                  # n!ping
async def ping(interaction: discord.Interaction) -> None:
    """ Get my Ping """
    await interaction.response.send_message("Pong! `" + str(client.latency * 100) + "ms`")

@client.tree.command(name="img")                                   # Natsuki image from "Natsuki Worship"
async def img(interaction: discord.Interaction) -> None:
    """ Send an image of Natsuki """
    imgimg = "D:\Alles\Alle Bilder\DDLC\\" + random.choice(os.listdir("D:\Alles\Alle Bilder\DDLC"))
    await interaction.response.send_message(file=discord.File(imgimg))


@client.tree.command(name="shdf")                                   # Get image
async def shdf(interaction: discord.Interaction):
    """ Send an SHDF image """
    shdfimg = "D:\Alles\Alle Bilder\Anime People doing Wholesome Thing\\" + random.choice(os.listdir("D:\Alles\Alle Bilder\Anime People doing Wholesome Thing"))
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
    fateimg = "D:Alles\\Alle Bilder\\Fate\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Fate"))
    await interaction.response.send_message(file=discord.File(fateimg))


@client.tree.command(name="tanya")                           # Tanya image from
async def tanya(interaction: discord.Interaction):
    """ Get an image of Tanya von Degurechaff """
    tanyaimg = "D:\Alles\Alle Bilder\Tanya Degurechaff\\" + random.choice(os.listdir("D:\Alles\Alle Bilder\Tanya Degurechaff"))
    await interaction.response.send_message(file=discord.File(tanyaimg))

@client.tree.command(name="tomboy")                                   # Get image
async def tomboy(interaction: discord.Interaction):
    """Mmm tomboy abs yummy licky """
    tomboyimg = "D:\Alles\Alle Bilder\Anime Tomboys\\" + random.choice(os.listdir("D:\Alles\Alle Bilder\Anime Tomboys"))
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
    remimg = "D:\\Alles\\Alle Bilder\\Rem\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Rem\\"))
    await interaction.response.send_message(file=discord.File(remimg))


@client.tree.command(name="klk")
async def klk(interaction: discord.Interaction):
    """ Get an image of Kill la Kill """
    klkimg = "D:\\Alles\\Alle Bilder\\Kill la Kill\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Kill la Kill\\"))
    await interaction.response.send_message(file=discord.File(klkimg))

@client.tree.command(name="rmeme")
async def rmeme(interaction: discord.Interaction):
    """ Get one of Strawb's memes """
    try:
        mp4 = "D:\\Alles\\Alle Musik und Videos\\" + random.choice(os.listdir("D:\\Alles\\Alle Musik und Videos\\"))
        await interaction.response.send_message(file=discord.File(mp4))
    except discord.errors.HTTPException:
        await interaction.response.send_message("File too large, try again.")
    except PermissionError:
        await interaction.response.send_message("Permission denied; Folder was auto-blocked, please try again.")


@client.tree.command(name="rr")
async def rr(interaction: discord.Interaction):
    """ Get a NS song (Most likely German) """
    try:
        mp3 = "D:\\Alles\\Alle Musik und Videos\\RR under 8MB\\" + random.choice(os.listdir("D:\\Alles\\Alle Musik und Videos\\RR under 8MB\\"))
        now = datetime.datetime.now()
        print(f'{now} | Song: {mp3}')
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
            await interaction.response.send_message(file=discord.File(mp3))
            print(f"RR music -- {mp3}")
        except discord.errors.HTTPException:
            await interaction.response.send_message("File too large, try again.")
        except PermissionError:
            await interaction.response.send_message("Permission denied; Folder was probably auto-blocked because of lewdness, please try again.")
    except OSError:
        await interaction.response.send_message("An error occoured, please try again.")


@client.tree.command(name="christ_chan")
async def christ_chan(interaction: discord.Interaction):
    """ Get an image of Christ-Chan """
    chrImg = "D:\\Alles\\Alle Bilder\\Christ-chan\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Christ-chan\\"))
    await interaction.response.send_message(file=discord.File(chrImg))

@client.tree.command(name="chan")
async def chan(interaction: discord.Interaction):
    """ Get an image of another Chan """
    chanImg = "D:\\Alles\\Alle Bilder\\Other Chans\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Other Chans\\"))
    await interaction.response.send_message(file=discord.File(chanImg))

@client.tree.command(name="megu")
async def megu(interaction: discord.Interaction):
    """ Get an image of Megumin """
    chanImg = "D:\\Alles\\Alle Bilder\\Megumin\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Megumin\\"))
    await interaction.response.send_message(file=discord.File(chanImg))

# Add a command for Rosh Hashanah

@client.tree.command(name="safe")
async def safe(interaction: discord.Interaction, *, tags : str):
    """ Get an image from Safebooru """
    try:
        ctxtags1 = tags.replace(", ", "+")
        ctxtags = ctxtags1.replace(" ", "_")
        urlSafePre = "https://safebooru.org/index.php?page=dapi&s=post&q=index&tags=" + ctxtags
        async with aiohttp.ClientSession() as session:
            async with session.get(urlSafePre) as response:
                html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        file_urls = []
        for post in soup.find_all('post'):
            if post.get('rating') == "s":
                file_urls.append(post.get('file_url'))
        await interaction.response.send_message(random.choice(file_urls) + f"\nTags recorded: `{ctxtags}`")
        print(
            f"Someone has searched for \"{tags}\"\nThis has resulted in the bot sending this link: [ {urlSafePre} ]")

    except IndexError:
        await interaction.response.send_message(f"No results found for {tags}.")


@client.tree.command(name="gelbooru")
async def gel(interaction: discord.Interaction, *, tags : str):
    """ Get an image from Gelbooru (SFW only) """
    try:
        print(tags)
        ctxtags3 = tags.replace(", ", "+")
        ctxtags2 = ctxtags3.replace(" ", "_")
        print(ctxtags2)
        urlSafePre = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=" + ctxtags2
        async with aiohttp.ClientSession() as session:
            async with session.get(urlSafePre) as response:
                html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        gel_file_urls = []
        for post in soup.find('posts').find_all('post'):
            if post.find('rating').get_text().strip().lower() == "general":
                gel_file_urls.append(post.find('file_url').get_text())

        await interaction.response.send_message(random.choice(gel_file_urls) + f"\nTags recorded: `{ctxtags2}`")
        print(
            f"Someone has searched for \"{tags}\"\nThis has resulted in the bot sending this link: [ {urlSafePre} ]")

    except IndexError:
        await interaction.response.send_message(f"No results found for {tags}.")

num = 0 # I have no idea what this is for

@client.event
async def on_ready():      # check if it runs
    num = 0
    await client.tree.sync()
    print(f'{client.user} is connected to the following guilds:\n')
    for _ in client.guilds:
        guild = client.guilds[num]
        print(
            f'{num} - {guild.name} (id: {guild.id})'
        )
        num += 1
    num = 0

print("Please wait a few seconds for the bot to connect")

client.run(botToken)
input("Just checking if it printed anything above. ")