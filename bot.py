# bot.py
import aiohttp

if __name__ == "__main__":
    pass
import random
import os
import time
import discord
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

client = commands.Bot(command_prefix="n!", case_insensitive=True)

youtube_dl.utils.bug_reports_message = lambda: ''

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

@client.command(brief="I'm not!!!")                                                   # n!you_are_cute
async def you_are_cute(ctx):
    print("a")
    await ctx.send("I'M NOT CUTE YOU IDIOT!!!")
    time.sleep(3.7)
    await ctx.send("...thanks")

@client.command(brief="Get my ping in milliseconds")                                  # n!ping
async def ping(ctx):
    print("a")
    await ctx.send("Pong! `" + str(client.latency * 100) + "ms`")

@client.command(brief="Get a random Natsuki image")                                   # Natsuki image from "Natsuki Worship"
async def img(ctx):
    #try:
    #    natsu_channel = client.get_channel(773887728110010378)  # Channel id here
    #    natsu_pics = await natsu_channel.history(limit=500).flatten()
    #    natsu_pic = random.choice(natsu_pics)
    #    natsu_pic_url = natsu_pic.attachments[0].url
    #    await ctx.send(natsu_pic_url)
    #except:
    #    await ctx.send("Error: Please try again.")
    #def get_random_file_from_dir(dirpath):
    #    files = os.listdir(dirpath)
#
#        return os.path.join(dirpath, files[random.randint(0, len(files) - 1)])
    toDelImg = await ctx.send("Please give me a few seconds to upload...")
    imgimg = "D:\Alles\Alle Bilder\DDLC\\" + random.choice(os.listdir("D:\Alles\Alle Bilder\DDLC"))
    await ctx.send(file=discord.File(imgimg))
    await toDelImg.delete()
    print(f"Natsuki Image -- {imgimg}")

@client.command(name="padoru", brief="Natsuki Padoru")                                # Natsuki Padoru
async def padoru(ctx):
    print("Hashire Sori Yo")
    await ctx.send(file=discord.File("D:\Alles\Alle Bilder\DDLC\Padoru Natsuki.png"))

@client.command(brief="Say hello to me")                                              # n!hello
async def hello(ctx):
    await ctx.send("Hey there! I'm the Natsuki Bot!")

@client.command(brief="Tell the truth")                                              # n!youre_the_best
async def youre_the_best(ctx):
    await ctx.send("You... You really think so..?")
    time.sleep(1)
    await ctx.send("Thank you...")
    time.sleep(0.5)
    await ctx.send("I-i meant Baka!")

@client.command(name="yuri_is_better", brief="State your incorrect opinion")          # n!yuri_is_better
async def yuri_is_better(ctx):
    print("a")
    await ctx.send("Nice joke, everyone knows **I** am the best \;D")
    time.sleep(2)
    await ctx.send("Wait, you're serious? Ok then...")
    await ctx.send("https://cdn.discordapp.com/attachments/896022117487878145/903669903544963142/227-2276698_post-pol-christ-chan.png")

print("Command 8 loaded")

@client.command(brief="Check the Wikipedia of something")                             # n!wiki
async def wiki(ctx, article):
    await ctx.send("https://en.wikipedia.org/wiki/" + article)

print("Command 9 loaded")

@client.command(name="animepfp",brief="Send this when someone says 'Ok Anime Pfp'")
async def animepfp(ctx):
    await ctx.send(file=discord.File("D:\Alles\Alle Bilder\hahaloser.png"))

print("Command 10 loaded")

@client.command(brief="Check the Wikipedia of something without preview")            # n!nwiki
async def nwiki(ctx, article):
    await ctx.send("<https://en.wikipedia.org/wiki/" + article + ">")

print("Command 11 loaded")

@client.command(name="bug", brief="Bugreport Contact")
async def bug(ctx):
    print("Bugreport Contact sent")
    await ctx.send("Currently you can report bugs to the user <@883054741263888384> or `Strawberry Mk.VI#6872`.")

print("Command 12 loaded")

@client.command(brief="")                                   # Get image
async def shdf(ctx):
    toDelShdf = await ctx.send("Please give me a few seconds to upload...")
    shdfimg = "D:\Alles\Alle Bilder\Anime People doing Wholesome Thing\\" + random.choice(os.listdir("D:\Alles\Alle Bilder\Anime People doing Wholesome Thing"))
    await ctx.send(file=discord.File(shdfimg))
    await toDelShdf.delete()
    print(f"SHDF Image -- {shdfimg}")

print("Command 13 loaded")

#def split(equasion):
#    return [int(x) for x in equasion.split()]


@client.command(name="math", brief="Do some math")                                      #n!math
async def math(ctx, equasion):
    try:
        result = parse(equasion)
    except OverflowError:
        result = "Number too large \:("
    except ZeroDivisionError:
        result = "Infinite"
    await ctx.send(result)

print("Command 14 loaded")

@client.command(name="timer", brief="A timer")
async def timer(ctx, timernum: int):
    user = ctx.message.author.id
    while timernum != 0:
        await asyncio.sleep(1)
        timernum -= 1
    await ctx.send(f'Your timer ran out, <@{user}>')

print("Command 15 loaded")

B = ":black_large_square:"
b = B
W = ":white_large_square:"
w = W
R = ":red_square:"
r = R

@client.command(name="draw", brief="Use W and B to draw, use period to go to the next line")
async def draw(ctx, drawmessage: str):
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
        await ctx.send(finalmessage)
    else:
        await ctx.send("Message too long. It has to be ~100 characters or less.\nBecause Discord Emojis vary in string sizes, it may be more or less than 100.")

print("Command 16 loaded")

@client.command(name="info", brief="Get info on me and my creators")                  # n!info
async def info(ctx):
    print("a")
    await ctx.send(
        "```\n"
        "| - - - - - - - - - - - - - - - - - - |\n"
        "| - - - - General Information - - - - |\n"
        "| - - - - - - - - - - - - - - - - - - |\n"
        "Bot Version:       -  26.10.21\n"
        "Bot Created on     -  June 29th, 2020\n"
        "Invite:            -  No Public Invite\n"
        "| - - - - - - - - - - - - - - - - - - |\n"
        "| - - - - - - - Credits - - - - - - - |\n"
        "| - - - - - - - - - - - - - - - - - - |\n"
        "Created by         -  Strawberry Mk.V\n"
        "Emotional Support  -  Natsuki\n"
        "| - - - - - - - - - - - - - - - - - - |\n"
        "| - - - - - Additional Info - - - - - |\n"
        "| - - - - - - - - - - - - - - - - - - |\n"
        "Regular Downtime   -  12 AM to 10 AM\n"
        "                         German Time\n"
        "Support Contact    -  Strawberry Mk.V\n"
        "                                 #3287\n"
        "| - - - - - - - - - - - - - - - - - - |\n"
        "| - - - - - Special  Thanks - - - - - |\n"
        "| - - - - - - - - - - - - - - - - - - |\n"
        "Strawberry Games\n"
        "And more!"
        "```\n"
    )

print("Command 17 loaded")

# Oracle
@client.command(name="Oracle", brief="Terry A. Davis' oracle")
async def oracle(ctx, amount: int):
    await ctx.send(functools.reduce(lambda line, word: line + f"{word} ", (random.choice(oraclewords) for _ in range(amount)), str()))

print("Command 18 loaded")

# Oracle German
@client.command(name="oracle_ger", brief="Terry A. Davis' oracle translated into German")
async def oracle_ger(ctx, amount_de: int):
    await ctx.send(functools.reduce(lambda line, word: line + f"{word} ", (random.choice(oracle_de_words) for _ in range(amount_de)), str()))

print("Command 19 loaded")

@client.command(brief="Get a random Fate image (Previously n!saber)")                           # Saber image
async def fate(ctx):
    toDelFate = await ctx.send("Please give me a few seconds to upload...")
    fateimg = "D:Alles\\Alle Bilder\\Fate\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Fate"))
    await ctx.send(file=discord.File(fateimg))
    await toDelFate.delete()
    print(f"Fate Image -- {fateimg}")


print("Command 20 loaded")

@client.command(brief="hi")
async def hi(ctx):
    toDelHi = await ctx.send("Please give me a few seconds to upload...")
    await ctx.send(file=discord.File("D:\Alles\Alle Bilder\Edgy Memes\hi.gif"))
    await toDelHi.delete()

print("Command 21 loaded")

@client.command(brief="random sauce generator")
async def sauce(ctx):
    await ctx.send(random.randint(1, 399999))

print("Command 22 loaded")

@client.command(brief="Get a random Tanya image")                           # Tanya image from
async def tanya(ctx):
    toDelTanya = await ctx.send("Please give me a few seconds to upload...")
    tanyaimg = "D:\Alles\Alle Bilder\Tanya Degurechaff\\" + random.choice(os.listdir("D:\Alles\Alle Bilder\Tanya Degurechaff"))
    await ctx.send(file=discord.File(tanyaimg))
    await toDelTanya.delete()
    print(f"Tanya Image -- {tanyaimg}")

print("Command 23 loaded")

@client.command(brief="Get an NSFW Natsuki image")                          # NSFW Natsuki image
async def nimg(ctx):
    toDelNImg = await ctx.send("Please give me a few seconds to upload...")
    nsfwnat = "G:\\Natsuki Private\\" + random.choice(os.listdir("G:\\Natsuki Private"))
    await ctx.send(file=discord.File(nsfwnat))
    await toDelNImg.delete()
    print(f"NSFW Natsuki Image -- {nsfwnat}")

print("Command 24 loaded")

@client.command(brief="Roll a dice")                                        # Roll a dice
async def dice(ctx, sides: int):
    sides -= 1
    result = random.randrange(sides)
    sides += 1
    result += 1
    await ctx.send("Sides: " + str(sides) + "\nResult: " + str(result))

print("Command 25 loaded")

@client.command(brief="Tomboy yummy")                                   # Get image
async def tomboy(ctx):
    toDelTom = await ctx.send("Please give me a few seconds to upload...")
    tomboyimg = "D:\Alles\Alle Bilder\Anime Tomboys\\" + random.choice(os.listdir("D:\Alles\Alle Bilder\Anime Tomboys"))
    print(f"Tomboy Image -- {tomboyimg}")
    await ctx.send(file=discord.File(tomboyimg))
    await toDelTom.delete()

print("Command 26 loaded")

@client.command(brief="Quotes of the Left in Germany")
async def links(ctx):
    await ctx.send(functools.reduce(lambda line, word: line + f"{word}", (random.choice(ls_german)), str()))

print("Command 27 loaded")

@client.command(brief="Quotes of the Left in Germany (English)")
async def links_en(ctx):
    await ctx.send(functools.reduce(lambda line, word: line + f"{word}", (random.choice(ls_english)), str()))

print("Command 28 loaded")

#@commands.command()
#async def join_voice(self, ctx):
#    channel = ctx.author.voice.channel
#    print(channel.id)
#    await self.client.VoiceChannel.connect()

#@client.command(brief="Load my Chad Playlist")
#async def play(ctx):
#    author = ctx.message.author
#    channel = author.voice_channel
#    await client.join_voice_channel(channel)
#    await ctx.send("p!play https://www.youtube.com/playlist?list=PLqA1TPFVNT1ZJPXptEJvL2ME6gbZvuXvE")
#    await vc.disconnect()


#def channel():
#    channel = ctx.author.VoiceState.channel

urlArray = []

@client.command(brief="WIP - Join a VC")
async def play(ctx, *, url):
    channel = ctx.author.voice.channel
    urlArray.append(url)

    def my_after(error):
        coro = play(urlArray[0])
        fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
        try:
            fut.result()
        except:
            # an error happened sending the message
            pass
    """Joins a voice channel"""
    if ctx.author.voice is None:
        await ctx.send("Please join a Voice Channel first.")
    else:
        #channel = ctx.author.voice.channel
        #if ctx.voice_client is not None:
        #await channel.connect()
        pass
    if ctx.guild.voice_client == None:
        await channel.connect()
    else:
        pass
    print(urlArray)

    async with ctx.typing():
        if not ctx.guild.voice_client.is_playing():
            player = await YTDLSource.from_url(urlArray[0], stream=True)
            ctx.voice_client.play(player, after=my_after)
            del urlArray[0]
            await ctx.send(f'Now playing: {player.title}\n')



@client.command(brief="See the queue if it exists")
async def queue(ctx):
    qNum = 0
    for _ in urlArray:
        await ctx.send(str(qNum + 1) + " - " + urlArray[qNum])
        qNum += 1


@client.command(brief="WIP - Leave VC")
async def stop(ctx):
    await ctx.guild.voice_client.disconnect()

@client.command(brief="WIP - Pause the song")
async def pause(ctx):
    await ctx.guild.voice_client.pause()
    await ctx.send("Audio paused.")

@client.command(brief="WIP - Resume the song")
async def unpause(ctx):
    await ctx.guild.voice_client.resume()
    await ctx.send("Audio resumed.")

print("Command 29 loaded")

@client.command(brief="If someone mentions porn")
async def fap(ctx):
    await ctx.send(
    "\n☝️ أيها الإخوة ، لا تشاهدوا الإباحية. إنه يخيب آمال الرب. ☝"
    "\n☝️وروsو ، فحش مه ګورئ. دا څښتن مایوسه کوي. ☝️\n"
    "☝️Αδέλφια, μην βλέπετε πορνό. Απογοητεύει τον Κύριο. ☝\n"
    "☝️Fratres, nolite vigilare sex. Decipit Dominum. ☝️\n"
    "☝️Братья, не смотрите порно. Это разочаровывает Господа. ☝\n️"
    "☝️Brothers, do not watch porn. It disappoints the Lord.☝️\n"
    )

print("Command 30 loaded")

@client.command(brief="Send an image of Rem")
async def rem(ctx):
    toDelRem = await ctx.send("Please give me a few seconds to upload...")
    remimg = "D:\\Alles\\Alle Bilder\\Rem\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Rem\\"))
    await ctx.send(file=discord.File(remimg))
    await toDelRem.delete()
    print(f"Rem Image -- {remimg}")

print("Command 31 loaded")

@client.command(brief="Send an image from Kill la Kill (Slightly NSFW)")
async def klk(ctx):
    toDelKlk = await ctx.send("Please give me a few seconds to upload...")
    klkimg = "D:\\Alles\\Alle Bilder\\Kill la Kill\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Kill la Kill\\"))
    await ctx.send(file=discord.File(klkimg))
    await toDelKlk.delete()
    print(f"Kill la Kill Image -- {klkimg}")

print("Command 32 loaded")

@client.command(brief="Create a fake hentai doujin with tags")
async def hentai(ctx, *, name):
    await ctx.send(
        f'Character: `{name}`\n'
        f'Tags : ' + functools.reduce(lambda line, word: line + f"`{word}` ", (random.choice(tags.tags) for _ in range(random.randint(1, 10))), str()) + '\n'
        f'Artist: `' + random.choice(tags.artists) + '`\n'
    )

print("Command 33 loaded")

@client.command(brief="Send a random one of Strawb's memes. This command will not be kept up-to-date and may have errors connected to file sizes.")
async def rmeme(ctx):
    toDelRMeme = await ctx.send("Please give me a few seconds to upload...")
    try:
        mp4 = "D:\\Alles\\Alle Musik und Videos\\" + random.choice(os.listdir("D:\\Alles\\Alle Musik und Videos\\"))
        await ctx.send(file=discord.File(mp4))
        print(f"rmeme -- {mp4}")
    except discord.errors.HTTPException:
        await ctx.send("File too large, try again.")
    except PermissionError:
        await ctx.send("Permission denied; Folder was probably auto-blocked because of lewdness, please try again.")
    await toDelRMeme.delete()

print("Command 34 loaded")

@client.command(brief="Random RR song. Most likely to be German.")
async def rr(ctx):
    toDelRR = await ctx.send("Please give me a few seconds to upload...")
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
            await ctx.send(file=discord.File(mp3))
            await ctx.send(f'Title: {audTitle}\nArtist: {audArt}\nAlbum: {audAlbum}')
            print(f"RR music -- {mp3}")
        except discord.errors.HTTPException:
            await ctx.send("File too large, try again.")
        except PermissionError:
            await ctx.send("Permission denied; Folder was probably auto-blocked because of lewdness, please try again.")
    except OSError:
        await ctx.send("An error occoured, please try again.")
    await toDelRR.delete()

print("Command 35 loaded")

@client.command(brief="Sends you good hentai")
async def hen(ctx):
    toDelHen = await ctx.send("Please give me a few seconds to find a nice video...")
    time.sleep(random.randint(1, 5))
    vid = random.randint(1, 3)
    if vid == 1:
        await ctx.send("https://cdn.discordapp.com/attachments/883060024971251713/902586473319124992/hentai.mp4")
    elif vid == 2:
        await ctx.send("https://cdn.discordapp.com/attachments/883060024971251713/902586820326473838/Lewd.mp4")
    elif vid == 3:
        await ctx.send("https://cdn.discordapp.com/attachments/883060024971251713/902587106784870460/Free_Loli_Lewd.mp4")
    await toDelHen.delete()

print("Command 36 loaded")

@client.command(brief="Send an image of Christ-Chan")
async def christ(ctx):
    toDelChr = await ctx.send("Please give me a few seconds upload...")
    chrImg = "D:\\Alles\\Alle Bilder\\Christ-chan\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Christ-chan\\"))
    await ctx.send(file=discord.File(chrImg))
    print(f"Christ-Chan image --- {chrImg}")
    await toDelChr.delete()
    print(f"Christ-chan Image -- {chrImg}")

@client.command(brief="Send an image of another Chan")
async def chan(ctx):
    toDelChr = await ctx.send("Please give me a few seconds upload...")
    chanImg = "D:\\Alles\\Alle Bilder\\Other Chans\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Other Chans\\"))
    await ctx.send(file=discord.File(chanImg))
    print(f"Christ-Chan image --- {chanImg}")
    await toDelChr.delete()
    print(f"Christ-chan Image -- {chanImg}")

@client.command(brief="Send an image of Megumin")
async def megu(ctx):
    toDelChr = await ctx.send("Please give me a few seconds upload...")
    chanImg = "D:\\Alles\\Alle Bilder\\Megumin\\" + random.choice(os.listdir("D:\\Alles\\Alle Bilder\\Megumin\\"))
    await ctx.send(file=discord.File(chanImg))
    print(f"Megumin image --- {chanImg}")
    await toDelChr.delete()

# Add a command for Rosh Hashanah

@client.command(brief="Safebooru search")
async def safe(ctx, *, tags : str):
    try:
        #print(tags)
        ctxtags1 = tags.replace(", ", "+")
        ctxtags = ctxtags1.replace(" ", "_")
        #print(ctxtags)
        urlSafePre = "https://safebooru.org/index.php?page=dapi&s=post&q=index&tags=" + ctxtags
        userSafe = ctx.message.author.id
        async with aiohttp.ClientSession() as session:
            async with session.get(urlSafePre) as response:
                html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        file_urls = []
        for post in soup.find_all('post'):
            if post.get('rating') == "s":
                file_urls.append(post.get('file_url'))
        #print(file_urls)
        message = await ctx.send(random.choice(file_urls))
        print(
            f"{userSafe} has searched for \"{tags}\"\nThis has resulted in the bot sending this link: [ {urlSafePre} ]")
        await message.add_reaction('❌')
        await ctx.send(f"\nTags recorded: `{ctxtags}`")
        try:
            await client.wait_for(
                "reaction_add",
                timeout=30.0,
                check=lambda r, u: u.id == userSafe
                    and r.emoji == "❌"
                    and r.message.id == message.id,
            )
        except TimeoutError:
            pass
        await message.delete()

    except IndexError:
        await ctx.send(f"No results found for {tags}.")


@client.command(brief="Gelbooru search")
async def gel(ctx, *, tags : str):
    try:
        print(tags)
        ctxtags3 = tags.replace(", ", "+")
        ctxtags2 = ctxtags3.replace(" ", "_")
        print(ctxtags2)
        urlSafePre = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=" + ctxtags2
        userSafe = ctx.message.author.id
        async with aiohttp.ClientSession() as session:
            async with session.get(urlSafePre) as response:
                html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        gel_file_urls = []
        for post in soup.find('posts').find_all('post'):
            print(len(soup.find_all('posts')))
            print('we get here')
            print(post.find('rating').get_text().strip().lower())
            if post.find('rating').get_text().strip().lower() == "general":
                print('we are past the check')
                gel_file_urls.append(post.find('file_url').get_text())
                print(gel_file_urls)

        print(gel_file_urls)
        message = await ctx.send(random.choice(gel_file_urls))
        print(
            f"{userSafe} has searched for \"{tags}\"\nThis has resulted in the bot sending this link: [ {urlSafePre} ]")
        await message.add_reaction('❌')
        await ctx.send(f"\nTags recorded: `{ctxtags2}`")
        try:
            await client.wait_for(
                "reaction_add",
                timeout=30.0,
                check=lambda r, u: u.id == userSafe
                    and r.emoji == "❌"
                    and r.message.id == message.id,
            )
        except TimeoutError:
            pass
        await message.delete()

    except IndexError:
        await ctx.send(f"No results found for {tags}.")

num = 0 # I have no idea what this is for

@client.event
async def on_ready():      # check if it runs
    num = 0
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