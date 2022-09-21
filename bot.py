# bot.py

import aiohttp

if __name__ == "__main__":
    pass
import random
import os
import discord
from discord import app_commands
import discord.ext
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

client = commands.Bot(command_prefix="n!", case_insensitive=True, intents=discord.Intents.default())


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
    imgimg = "D:\\Alles\\Alle Bilder\\DDLC\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\DDLC"))
    await interaction.response.send_message(file=discord.File(imgimg))


@client.tree.command(name="shdf")                                   # Get image
async def shdf(interaction: discord.Interaction):
    """ Send an SHDF image """
    shdfimg = "D:\\Alles\\Alle Bilder\\Anime People doing Wholesome Thing\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Anime People doing Wholesome Thing"))
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
    tanyaimg = "D:\\Alles\\Alle Bilder\\Tanya Degurechaff\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Tanya Degurechaff"))
    await interaction.response.send_message(file=discord.File(tanyaimg))


@client.tree.command(name="tomboy")                                   # Get image
async def tomboy(interaction: discord.Interaction):
    """Mmm tomboy abs yummy licky """
    tomboyimg = "D:\\Alles\\Alle Bilder\\Anime Tomboys\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Anime Tomboys"))
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
        await interaction.response.defer()
        mp4 = "D:\\Alles\\Alle Musik und Videos\\" + random.choice(os.listdir("D:\\Alles\\Alle Musik und Videos\\"))
        await interaction.followup.send(file=discord.File(mp4))
    except discord.errors.HTTPException:
        await interaction.followup.send("File too large, try again.")
    except PermissionError:
        await interaction.followup.send("Permission denied; Folder was auto-blocked, please try again.")


@client.tree.command(name="rr")
async def rr(interaction: discord.Interaction):
    """ Get a NS song (Most likely German) """
    await interaction.response.defer()
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
            await interaction.followup.send(file=discord.File(mp3))
            await interaction.followup.send(f"Song: {audTitle} | Artist: {audArt} | Album: {audAlbum}")
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
        await interaction.response.send_message(the_url + f"\nTags recorded: `{ctxtags}`\nID: {source[the_url_num]} | Found `{file_urls_length - 1}` other entries.")
        print(
            f"Someone has searched for \"{tags}\"\nThis has resulted in the bot sending this link: [ {urlSafePre} ]")

    except IndexError:
        await interaction.response.send_message(f"No results found for {tags}.")


@client.tree.command(name="gelbooru")
async def gel(interaction: discord.Interaction, tags: str, nsfw: Literal['safe', 'safe and questionable', 'all', 'explicit only'] = 'safe', gendered: Literal['Female Only', 'Male Only', 'Any'] = 'Any'):
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
        if gendered == 'Female Only':
            urlSafePre += "+-1boy+-2boys+-3boys+-4boys+-5boys+-6%2bboys+-penis+-multiple_penises+-muscular_male"
        elif gendered == 'Male Only':
            urlSafePre += "+-1girl+-2girls+-3girls+-4girls+-5girls+-6%2bgirls+-vagina"
        else:
            pass
        async with aiohttp.ClientSession() as session:
            async with session.get(urlSafePre) as response:
                html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        gel_file_urls = []
        source = []
        gel_file_urls_length = 0
        for post in soup.find('posts').find_all('post'):
            # if post.find('rating').get_text().strip().lower() == "general":
            gel_file_urls.append(post.find('file_url').get_text())
            source.append(post.find('id').get_text())
            gel_file_urls_length += 1

        the_url_num = random.randint(0, gel_file_urls_length - 1)
        the_url = gel_file_urls[the_url_num]
        await interaction.followup.send(the_url + f"\nTags recorded: `{ctxtags2}`\nUser searched for: `{nsfw}`\nID: `{source[the_url_num]}`\nFound `{gel_file_urls_length - 1}` other entries.")
        print(
            f"Someone has searched for \"{tags}\"\nThis has resulted in the bot sending this link: [ {urlSafePre} ]\nThe ID of the post is `{source[the_url_num]}`\n"
            f"This is the link sent: -# {the_url} #-")

    except IndexError or discord.app_commands.errors.CommandInvokeError:
        await interaction.followup.send(f"No results found for `{tags}`.")

    except ValueError:
        await interaction.followup.send(f"Something went wrong. Please check the spelling of each tag and try again.\nTags used: `{tags.replace('+', ', ')}`")


@client.tree.command(name="bleachbooru")
async def bleach(interaction: discord.Interaction, tags: str, nsfw: Literal['safe', 'questionable and safe (high filter)', 'questionable and safe (low filter)', 'all', 'explicit only'] = 'safe'):
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
                bleachb = await response.text()
        soup = BeautifulSoup(bleachb, 'xml')
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

    #except AttributeError:
    #    await interaction.followup.send(f"Due to retarded Bleachbooru limitations, you can only search for a single tag. Please try again.\nTags recorded: `{tags}`\n`Note: This might also happen when the API is down. Check the site if it's down.`")


#  @client.tree.command(name="e621")
#  async def e621(interaction: discord.Interaction, *, tags: str):
#    """ Get an image from e621 (SFW only, you damn furfag) """
#    try:
#        print(tags)
#        tags = ' '.join([tag.strip().replace(' ', '_') for tag in tags.split(',')])
#        e621_file_urls = []
#        urlSafePreFur = "https://e621.net/posts.json"
#        async with aiohttp.ClientSession() as session:
#            async with session.get(urlSafePreFur, params={'tags': tags + " -trans_(lore) -lgbt_pride -trans_man_(lore) -trans_woman_(lore) -transgender_pride_colors -lgbt_history_month -rainbow_pride_flag -lgbt_couple -male%2Fmale rating:safe"}) as response:
#                data = await response.json()
#        for post in data['posts']:
#            e621_file_urls.append(post['file']['url'])
#
#        the_url = random.choice(e621_file_urls)
#        await interaction.response.send_message(the_url + f"\nTags recorded: `{tags}`")
#
#    except IndexError:
#        await interaction.response.send_message(f"No results found for `{tags}`.")


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
