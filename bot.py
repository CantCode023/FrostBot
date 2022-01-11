#     ▄████████    ▄████████  ▄██████▄     ▄████████     ███          ▀█████████▄   ▄██████▄      ███
#    ███    ███   ███    ███ ███    ███   ███    ███ ▀█████████▄        ███    ███ ███    ███ ▀█████████▄
#    ███    █▀    ███    ███ ███    ███   ███    █▀     ▀███▀▀██        ███    ███ ███    ███    ▀███▀▀██
#   ▄███▄▄▄      ▄███▄▄▄▄██▀ ███    ███   ███            ███   ▀       ▄███▄▄▄██▀  ███    ███     ███   ▀
#  ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   ███    ███ ▀███████████     ███          ▀▀███▀▀▀██▄  ███    ███     ███
#    ███        ▀███████████ ███    ███          ███     ███            ███    ██▄ ███    ███     ███
#    ███          ███    ███ ███    ███    ▄█    ███     ███            ███    ███ ███    ███     ███
#    ███          ███    ███  ▀██████▀   ▄████████▀     ▄████▀        ▄█████████▀   ▀██████▀     ▄████▀

import discord
import re
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import json
import requests
from PIL import Image, ImageDraw, ImageOps
import io
from io import BytesIO
import aiohttp
import asyncio
import random
import urllib.parse
import datetime
from discord_components import *
import traceback
from colorama import Fore, Style

# ------------------------------------------------- #

import chances
import webhook
from roblox import Client
import pyttsx3
from pbwrap import Pastebin
from textblob import TextBlob
import qrcode
from mojang import MojangAPI
from keycodes import Codes
import base64

# ------------------------------------------------- #

from discord.utils import get

# ------------------------------------------------- #

good_words = ["nice", "good", "cool", "perfect", "smart", 'awesome', 'epic', 'kind', 'helpful', 'useful']
badword = ['fuck','shit','shlt','bitch','bltch','cum','dick','asshole','whore','pussy','hentai','boob','b00b','bo0b','b0ob']
ok = ['true', 'false']
whatshot = ['headshot', 'legshot', 'handshot', 'bodyshot']
verycoolfact = ['Frost bot have many more commands but some are hid by the developer.', 'Frost bot was created at 7th July 2021', 'When the developer was typing this, frost bot was only 16 days old.', 'The developer of frost bot is not American.', 'The developer was only 13 years old when it was 2021.',
                'The developer is not very smart and is still learning.', 'The developer is actually male', 'The developer has made a gender reveal. Good luck finding it using the same command.', 'You can suggest what fact to put in the fun fact database.', "You can get more chances on getting ghosts when it's night for you! Try using frost findghost.", "When the developer was writing this, no one was using frost bot :\")", "Frost bot can speak! Try frost tts Hello World", "The bot is 2 months old when the developer is typing this fact.", "Frost bot is making a huge progress (locally :tear)"]
username = 'FrostBot'

messagedeleted = None
whodeleted = None


def Code(code):
    return str(base64.b64decode(code).decode("utf-8"))

def password():
    return "Apakah?##5"

def openFile(path):
    with open(path, 'r') as f:
        return f.read()

def saveFile(path):
    with open(path ,'w') as infile:
        lines = infile.readlines()

    with open(path, 'wb') as outfile:
        outfile.writelines(lines) 

def openFileAsJson(path):
    with open(path, 'r') as f:
        return json.load(f)

def saveFileAsJson(path, var):
    with open(path, 'w') as f:
        return json.dump(var, f, indent=4)


async def readURL(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return print("Could not download file..")
            else:
                data = io.BytesIO(await resp.read())
                return data


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
intents = discord.Intents.all()
intents.members = True

# Discord Client
client = commands.Bot(intents=intents, command_prefix=['frost ', 'f!'])
client.remove_command('help')

# Roblox
roblox = Client(Code(Codes.robloxtoken))  

# Discord Buttons
button = DiscordComponents(client)

# Pastebin Client
pastebin = Pastebin(Code(Codes.pastebinapikey))
user_id = pastebin.authenticate(Code(Codes.pastebinuser), Code(Codes.pastebinpass))

trolling = False
picking = False

import string
import random

ababa = string.ascii_lowercase
adada = random.sample(ababa, 5)
ajaja = "".join(adada)
print("New dismusic password: " + ajaja)

client.lava_nodes = [
    {
        'host': 'lava.link', 
        'port': 80,
        'rest_uri': f'http://lava.link:80',
        'identifier': 'MAIN',
        'password': str(ajaja),
        'region': 'singapore',
    }
]


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(
        type=discord.ActivityType.playing, name="frost help | https://realfrostbot.repl.co/"
    ))
    print(f"{client.user.name} is ready!")
    client.load_extension('dismusic')
    

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        bruh = str(error).split(' ')
        heh = bruh[1].replace('"', '').capitalize()

        embed = discord.Embed(
            color=discord.Color.from_rgb(255,179,0)
        )
        embed.set_author(icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png', name=f"{heh} is not an existing command.")

        await ctx.send(embed=embed)
        print(f"{ctx.author.name + '#' + ctx.author.discriminator} tried to use a non-existing command: frost " +
              bruh[1].replace('"', ''))


@client.command()
async def ping(ctx):
    await ctx.send(f"Bot's current ping is {round(client.latency * 1000)}ms")


@client.command()
@commands.has_permissions(mention_everyone = True)
async def announce(ctx):
    await ctx.message.delete()
    await ctx.send('@everyone, Fross.Gaming#0191 adalah babi!')


@announce.error
async def announce_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**An error was found: You do not have the required permission to use the purge command!**")


@client.command(pass_context=True,name='purge')
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount=1):                                                                                                   
    await ctx.channel.purge(limit=amount)


@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**An error was found: You do not have the required permission to use the purge command!**")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("**An error was found: Missing Argument.**")


@client.command(pass_context=True, name='ok')
async def ok(ctx):
    await ctx.message.delete()
    ok = 0
    while ok < 10:
        ok += 1
        await ctx.send('ok')


@client.command(pass_context=True, name='google')
async def google(ctx, *, search):
    await ctx.message.delete()
    link = urllib.parse.quote(search)
    avatar = ctx.author.avatar_url
    embed=discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    embed.set_author(name=f'searched {search}',icon_url=avatar)
    await ctx.send(
        embed=embed,
        components = [
            [Button(label = search, custom_id = "link", style=ButtonStyle.URL, url=f'https://google.com/search?q={link}')]
        ],
    )


@client.command(pass_context=True, name='test')
async def test(ctx, a: int):
    await ctx.message.delete()
    bruh = 0
    while bruh < a:
        bruh += 1
        await ctx.send("test")

dada = ""
titleing = False


@client.command(pass_context=True, name='embed')
async def embed(ctx, *, ah: str):
    await ctx.message.delete()
    global dada
    global titleing
    global currentmessaging
    dada = ah
    titleing = True
    currentmessaging = ctx.message.author.id


@client.command(pass_context=True, name='massreact')
async def massreact(ctx, limit: int, reaction: str):
    await ctx.message.delete()
    async for message in ctx.message.channel.history(limit=limit):
        await message.add_reaction(reaction)


@massreact.error
async def massreact_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("**MISSING ARGUMENT**")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("**ERROR: BAD ARGUMENT**")

currentchannel = None
@client.command(pass_context=True, name='dm')   
async def dm(ctx,  user: discord.User, *, message=None):
    global currentchannel
    currentchannel = int(ctx.message.channel.id)
    await ctx.channel.purge(limit=1)
    channel = await user.create_dm()
    await channel.send(message)
    webhook = Webhook.from_url(
        "https://discord.com/api/webhooks/921060144786321528/uItOu1A4MfdohJ9chjHM8DQkNnBjynbOWrzYSe7XV-FTnIDm7kpxcDVcpT8Yqggv0v8Z", adapter=RequestsWebhookAdapter())
    webhook.send(str(ctx.message.author) + " sent the message " +
                 str(message) + " to " + str(user))


@client.command(pass_context=True, name="respond")
async def respond(ctx, *, message=None):
    global currentchannel
    c = client.get_channel(currentchannel)
    await c.send(message)


@client.command(name='cleardm')
async def cleardm(ctx, user: discord.User):
    await ctx.channel.purge(limit=1)
    async for message in user.history():
        if message.author == client.user:
            await message.delete()


@client.command(pass_context=True, name='say')
async def say(ctx, *, message=None):
    await ctx.channel.purge(limit=1)
    message = message
    await ctx.send(message)


@client.command(pass_context=True)
async def reply(ctx, *, message=None):
    a = False
    for i in badword:
        if "‎" in str(ctx.message.content):
            if i in str(ctx.message.content.replace("‎",'')).lower() and not ctx.author.bot:
                await ctx.message.delete()
                a = True
            else:
                a = False
        else:
            if i in str(ctx.message.content).lower() and not ctx.author.bot:
                await ctx.message.delete()
                a = True
            else:
                a = False
    if a:
        await ctx.send(f"{ctx.author.mention}, you are weird.")
    else:
        await ctx.reply(message)


@client.command(pass_context=True)
async def afk(ctx, mins=1, reason=None):
    await ctx.send(f"{ctx.author.mention} has gone afk for {mins} minutes! Reason: {reason}")

    counter = 0
    while counter <= int(mins):
        counter += 1
        await asyncio.sleep(60)

        if counter == int(mins):
            await ctx.send(f"{ctx.author.mention} is no longer afk!")
            break


@client.command(pass_context=True)
async def quote(ctx):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    cool = json_data[0]['q']
    auth = json_data[0]['a']
    await ctx.send(f"{cool} - {auth}")


oke = None


@client.command(pass_context=True, name='loopquote')
async def loopquote(ctx, *, cooldown: int):
    global oke
    oke = True
    while oke:
        channel = client.get_channel(867796401432559616)
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        cool = json_data[0]['q']
        auth = json_data[0]['a']
        await channel.send(f"{cool} - {auth}\n")
        await asyncio.sleep(cooldown*60)


@client.command(pass_context=True, name='stoploopquote')
async def stoploopquote(ctx):
    global oke
    oke = False
    await ctx.send("Loop quote was successfully stopped.")


@client.command(pass_context=True, name='av')
async def av(ctx, *, user: discord.User=None):
    if user == None:
        user = ctx.author
    await ctx.send(user.avatar_url_as(size=256, static_format='png'))


@client.command(pass_context=True, name='talk')
async def talk(ctx, channelid, *, lolwhat: str):
    if ctx.message.author.id == 737912807810662400:
        channel = client.get_channel(int(channelid))
        await channel.send(lolwhat)


@client.command(pass_context=True, name='warn')
async def warn(ctx, user: discord.Member, *, reason):
    await ctx.message.delete()
    embed = discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0),
        description=f"{user.name} have been warned by {ctx.author.name}\nReason: {reason}"
    )
    embed.set_author(name=f'warned {user.name}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    channel = await user.create_dm()
    embed1 = discord.Embed(
        title=f'You have been warned by {ctx.author.name} on the server {user.guild.name}',
        description=f"Reason: {reason}",
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    await channel.send(embed=embed1)


@client.command(pass_context=True)
async def countdown(ctx, *, timber=None):
    await ctx.send("Countdown has started!")
    count = 0
    while count <= int(timber):
        await asyncio.sleep(1)
        count += 1

        if count == int(timber):
            await ctx.send("Countdown has ended!")
            break


@client.command(pass_context=True, name='info')
async def info(ctx, *, member: discord.Member):
    embed = discord.Embed(
        title=str(member.name) + "'s Info.",
        description=f"""
        Name: {member.name}
        Created At: {member.created_at}
        Joined at: {member.joined_at}
        Discriminator: {member.discriminator}
        Display Name: {member.display_name}
        ID: {member.id}
        Is Avatar Animated: {member.is_avatar_animated()}
        Top Role: {member.top_role}
        Colour: {member.color}
        """,
        color=discord.Color.from_rgb(255,179,0)
    )
    await ctx.send(embed=embed)


@client.command(pass_context=True, name='guest')
async def tetamu(ctx, *, user: discord.Member):
    await ctx.send(f"{user.mention} will come to your house!")


@client.command(pass_context=True,name='help', invoke_without_command=True, aliases=['command', 'commands', 'cmd', 'cmds'])
async def nice(ctx, page: str = None):
    main=discord.Embed(
        description="The prefix for Frost Bot is `frost`.",
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    main.set_author(name='🧰 Commands', icon_url='https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256')
    main.add_field(name=f'👨🏻‍🦲 User', value=f'```frost help user```', inline=True)
    main.add_field(name=f'🔥 API', value='```frost help api```', inline=True)
    main.add_field(name=f'🗿 Others', value=f'```frost help others```', inline=True)
    main.add_field(name=f'🤔 Suggest', value=f'```frost help suggest```', inline=True)
    main.add_field(name=f'🎵 Music', value=f'```frost help music```', inline=True)
    main.add_field(name=f'😱 All', value=f'```frost help all```', inline=True)
    main.add_field(name=f'😏 Updates', value=f'```frost help updates```', inline=True)
    main.add_field(name=f'🤖 Roblox', value=f'```frost help roblox```', inline=True)
    main.add_field(name=f'🔨 Mod', value=f'```frost help mod```', inline=True)
    main.set_footer(text=f'Requested by {ctx.author.name}')

    user=discord.Embed(
        description='''
        **dm**: frost dm @example hello, Frost bot will send a message you typed to a specific user.
        **cleardm**: frost cleardm @example, Clears a specific user dm that was sent by Frost bot.
        **av**: frost av @example, Gets a specific user\'s avatar.
        **info**: frost info @example, Gets a specific user\'s information.'
        **troll**: frost troll @example, Spams an image in a dm of a specific user.
        **trollstop**: frost trollstop, Stops bot from spamming image.
        **shoot**: frost shoot @example, Shoots a specific user.
        **joke**: frost joke @example, Sends a message saying a specific user doesn\'t know about jokes.
        **advice**: frost advice @example, Advices a specific user. 
        **warn**: frost warn @example, Warns a specific user.
        **getrobloxdata**: frost getrobloxdata @example, Gets a specific user\'s Roblox\'s data.
        **report**: frost report @example, Reports a specific user.
        **insult**: frost insult @example, Insults a specific user.
        **move**: frost move @example (voice_id), Moves a specific user to a different voice channel (USER MUST BE IN CALL).
        **kidnap**: frost kidnap @example, Kidnaps a specific user.
        ''',
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    user.set_author(name='🧰 Commands', icon_url='https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256')
    user.set_footer(text=f'Requested by {ctx.author.name}')

    api= discord.Embed(
        description='''
        **hack**: frost hack Russia, "Hacks" something, can also be a user: frost hack @example.
        **quote**: frost quote, Sends a random quote.
        **dadjoke**: frost dadjoke, Sends a random dadjoke.
        **insult**: frost insult @example, Insults a specific user.
        **randomcat**: frost randomcat, Sends a random cat image
        **advice**: frost advice @example, Sends a random advice to a specific user.
        **randomevent**: frost randomevent, Sends a random event that have happened to the world.
        **fruit**: frost fruit (fruitname), Sends a specific information about the fruit.
        **memegenerator**: frost memegenerator (Meme ID), Generates meme by meme id, get meme id using frost allmemes.
        **getrobloxdata**: frost getrobloxdata @example, Gets a specific user\'s Roblox\'s data.
        **randompicture**: frost randompicture, Sends a random picture (VERY RANDOM).
        **search**: frost search (max_search) (what to search), Example: frost search 5 ice cream. Almost as same as google but it sends the title and link in discord instead of you opening google. Try frost google (what to search) and frost search to see the differences!
        **movie**: frost movie (moviename), Example: frost movie Stand By Me Doraemon. Sends a list of movie and the informations of it. (Currently in BETA)
        **ship**: frost ship @example @example, Ships someone. Don't ship with bot.
        **covid-19**: frost covid-19 (country name), Gives the latest covid 19 statistics of a specific country.
        **urdict**: frost urdict (what_to_search), Urban dictionary.
        **removebg**: frost removebg, Removes background of a picture.
        **textblob**: frost textblob (message), Just a sentiment analyzer.
        **bored**: frost bored, If you're bored, do this command.
        **qr**: frost qr (link), Converts link to qr code.
        **getminecraftdata**: frost getminecraftdata (minecraft username), Gets a specific Minecraft User's data.
        **rhyme**: frost rhyme (word), Gives you 10 words that rhymes with the word given.
        **ytmp4**: frost ytmp4, Sends you a website link for youtube mp4.
        **ytmp3**: frost ytmp3, Sends you a website link for youtube mp3.
        **ytshort** frost ytshort, Sends you a website link for youtube short.
        **wallpaper**: frost wallpaper, Gets random wallpaper from the wallpaper subreddit.
        **phumor**: frost phumor, Memes for programmers, fetched from ProgrammerHumor subreddit.
        ''',
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    print("Hello World!")
    api.set_author(name='🧰 Commands', icon_url='https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256')
    api.set_footer(text=f'Requested by {ctx.author.name}')

    others=discord.Embed(
        description='''
        **ping**: frost ping, Checks the bot\'s current ping.
        **purge**: frost purge (amount to purge), Deletes messages.
        **say**: frost say (message), Sends message using bot.
        **help** frost help, Shows the main help page.
        **afk**: frost afk (minutes) (reason), AFK.
        **reply**: frost reply (message), Frost bot will reply a message you send.
        **countdown**: frost countdown (seconds), Starts a countdown timer.
        **check**: frost check, Check if Frost bot is activated and available to use.
        **massreact**: frost massreact (amount) (emoji), Reacts to every (amount) messages with (emoji)
        **sendhelp**: frost sendhelp (anything), "Sends help" to (anything), can also be used to user: frost sendhelp @example.
        **destroy**: frost destroy (anything), "Destroys" (anything), can also be user: frost destroy @example.
        **hyperlink**: frost hyperlink (Link Name), Generates a hyperlink.
        **fact**: frost fact, Sends facts that was manually typed by the owner of Frost Bot.
        **embed**: frost embed (title) (description), Generates an embed with the title (title) and the description (description).
        **google**: frost google (anything), Sends a link.
        **snipe**: frost snipe, Gets the latest deleted message.
        **findghost**: frost findghost, Find ghost.
        **buttons**: frost buttons, Sends list of buttons.
        **servercount**: frost servercount, Counts how many servers Frost Bot is in.
        **shopeesearch**: frost shopeesearch (max_limit) (what_to_search), Example: frost shopeesearch 5 pillow. Shopee is like Amazon but asian. This is a shopee search engine that is integrated to Frost Bot. Made using my latest API https://shopeeapi.smktd.repl.co/
        **tts**: frost tts (message), Frost bot can speak.
        **pin**: frost pin (details), Example: frost pin true. If details is set to true then Frost Bot will give the pinned message and the details if it's false then Frost Bot will only give the pinned message.
        **poll**: frost poll (message), Example: frost poll Should I make a new video?. What this does: This is basically a poll to ask people's opinion about a something you want to ask.
        **about**: frost about, Sends about FrostBot.
        **guessmyage**: frost guessmyage, Guesses your age mathematically.
        **craftyisasussybaka**: frost craftyisasussybaka
        **blueduckisasussybaka**: frost blueduckisasussybaka
        **buttons**: frost buttons, List of discord buttons.
        **report**: frost report @someone reason, Reports a specific user to the owner of Frost Bot (will be changed report to the owner of the group after frost bot's revamp)
        **randompicture**: frost randompicture, Sends a random picture.
        **servercount**: frost servercount, Sends the number of how many servers frost bot have joined.
        **flip**: frost flip, Flips the coin.
        **futurepartner**: frost futurepartner @example, you know the rules and so do I.
        **sourcecode**: frost sourcecode, Source Code of Frost Bot.
        ''',
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    others.set_author(name='🧰 Commands', icon_url='https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256')
    others.set_footer(text=f'Requested by {ctx.author.name}')

    suggest = discord.Embed(
        description='''
        **suggestfact**: frost suggestfact (Fact), Suggests a fact. Fact will be added if the owner agrees to.
        **suggestghost**: frost suggestghost (Ghost Name) (Ghost Image), Suggests a ghost. Ghost will be added if the owner agrees to.
        **suggestcommand**: frost suggestcommand (Command), Suggests a command. Command will be added if the owner agrees to.
        ''',
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    suggest.set_author(name='🧰 Commands', icon_url='https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256')
    suggest.set_footer(text=f'Requested by {ctx.author.name}')

    music = discord.Embed(
        description='''
        **connect**: frost connect, Connects to a voice channel that you're currently in.
        **disconnect**: frost disconnect, Disconnects from a voice channel that the bot\'s currently in.
        **loop**: frost loop, 3 Types of loop: NONE, CURRENT, PLAYLIST. None, Loop = False, CURRENT, Loop = True for current song playing, PLAYLIST, Loop = true for every song in queue and current song.
        **nowplaying**: frost nowplaying, Checks what song is currently playing.
        **play**: frost play (song name), Plays the song that you searched for.
        **pause**: frost pause, Pauses the current song that's playing.
        **resume**: frost resume, Resumes the current song that's playing.
        **queue**: frost queue, Checks songs that is currently in queue.
        **skip**: frost skip, Skips the current song that's playing.
        **volume**: frost volume (number), Sets volume.
        ''',
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    music.set_author(name='🧰 Commands', icon_url='https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256')
    music.set_footer(text=f'Requested by {ctx.author.name}')

    embede = discord.Embed(
        description="""
        Please visit https://commands.smktd.repl.co/
        """,
        color=discord.Color.from_rgb(255,179,0)
    )
    embede.set_author(name='🧰 Commands', icon_url='https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256')
    embede.set_footer(text=f'Requested by {ctx.author.name}')

    error = discord.Embed(
        color=discord.Color.from_rgb(255,179,0)
    )
    error.set_author(name=f'Can\'t find that help command.', icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')

    update = discord.Embed(
        description='''
        **updates**: frost updates, Checks the latest update for Frost Bot.
        **working on**: frost working on, Checks what Frost Bot's developers are currently working on.
        ''',
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    update.set_author(name='🧰 Commands', icon_url='https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256')
    update.set_footer(text=f'Requested by {ctx.author.name}')

    robloxia = discord.Embed(
        description='''
        **getrobloxdata**: frost getrobloxdata @example, Gets a specific user\'s Roblox\'s data.
        **headshot**: frost headshot (robloxusername), Gets a headshot picture of a specific roblox user.
        **outfits**: frost outfits (roblox username), Gets all OutfitId and OutfitName of a specific user.
        **getoutfit**: frost getoutfit (outfitid), Gets an image of an outfitId. Use **frost outfits (roblox username)** to get outfitId.
        ''',
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    robloxia.set_author(name='🧰 Commands', icon_url='https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256')
    robloxia.set_footer(text=f'Requested by {ctx.author.name}')

    mod = discord.Embed(
        description="""
        **setgetrole**: frost setgetrole (role name) (emoji reaction) (message). What this does: It's basically like react = get role. Example: frost setgetrole Members :white_check_mark: React the reaction to get the role "Members"!
        **purge**: frost purge (num). Bulk delete (num) messages. Example: frost purge 3
        **addcapsperm**: frost addcapsperm @someone (ALIASES: addcperm, acp), As you all know Frost Bot comes with Anti Caps, but I (Owner of Frost Bot) knowns how annoying it is sometimes, so I made a command to have caps permission. Only the owner of Frost Bot can give you caps perm. Dm Blue Duck#8344 to ask permission to get caps perm.
        **removecapsperm**: frost removecapsperm @someone (ALIASES: removecperm, rcp), Just like addcapsperm but removes caps perm.
        """
    )
    mod.set_author(name='🧰 Commands', icon_url='https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256')
    mod.set_footer(text=f'Requested by {ctx.author.name}')

    if page == None:
        await ctx.send(embed=main)
    elif page == "user":
        await ctx.send(embed=user)
    elif page == "api":
        await ctx.send(embed=api)
    elif page == "others":
        await ctx.send(embed=others)
    elif page == "suggest":
        await ctx.send(embed=suggest)
    elif page == "all":
        await ctx.send(embed=embede)
    elif page == "music":
        await ctx.send(embed=music)
    elif page == 'updates':
        await ctx.send(embed=update)
    elif page == 'roblox':
        await ctx.send(embed=robloxia)
    elif page == 'mod':
        await ctx.send(embed=mod)
    else:
        await ctx.send(embed=error)


mentio = None
shooter = None


@client.command(pass_context=True, name='sendhelp')
async def sendhelp(ctx, *, country: str):
    await ctx.send(f"Sent help to {country}")


@client.command(pass_context=True, name='move')
async def move(ctx, member: discord.Member = None, VoiceChannel=None):
    await ctx.message.delete()
    try:
        channel = discord.utils.get(ctx.guild.channels, id=int(VoiceChannel))
        if member == None:
            await ctx.message.author.move_to(channel)
        else:
            await member.move_to(channel)
    except Exception as e:
        embed = discord.Embed(
            title="**ERROR**",
            description=e,
            color=discord.Color.from_rgb(255,179,0).red()
        )
        await ctx.send(embed=embed)


@client.command(pass_context=True, name='randomcat')
async def randomcat(ctx):
    r = requests.get("https://api.thecatapi.com/v1/images/search")
    ok = json.loads(r.text)
    url = ok[0]['url']
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await ctx.send("Couldn't find a cat image!")
            else:
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, str(url)))


@client.command(pass_context=True, name='insult')
async def insult(ctx, *, user: discord.Member):
    await ctx.message.delete()
    r = requests.get("https://evilinsult.com/generate_insult.php?")
    await ctx.send(f"{user.mention}, {r.text}")


@insult.error
async def insult_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        ctx.send("**MISSING ARGUMENT**")


@client.command(pass_context=True, name='shoot')
async def shoot(ctx, user: discord.User):
    global picking
    await ctx.send(f"{ctx.author.mention} tries to shoot {user.mention}!")
    await asyncio.sleep(3)
    await ctx.send(f"_ _\n{user.mention} what will you do?\nA. Dodge\nB. Let {ctx.author.mention} shoots you")
    global picking
    picking = True
    global mentio
    global shooter
    mentio = user.id
    shooter = ctx.author


@client.command()
async def check(ctx):
    await ctx.send("Frost's here! Ready to explore?")


@client.command(pass_context=True, name='hack')
async def hack(ctx, israel: str):
    await ctx.message.delete()
    message = await ctx.send(f"Hacking {israel}")
    await asyncio.sleep(2)
    await message.edit(content="Analizing IP.")
    await asyncio.sleep(.5)
    await message.edit(content="Analizing IP..")
    await asyncio.sleep(.5)
    await message.edit(content="Analizing IP...")
    await asyncio.sleep(.5)
    await message.edit(content="Analizing IP.")
    await asyncio.sleep(.5)
    await message.edit(content="Analizing IP..")
    await asyncio.sleep(.5)
    await message.edit(content="Analizing IP...")
    await asyncio.sleep(.5)
    await message.edit(content="Analizing IP.")
    await asyncio.sleep(.5)
    await message.edit(content="Analizing IP..")
    await asyncio.sleep(.5)
    await message.edit(content="Analizing IP...")
    await asyncio.sleep(2)
    await message.delete()

    Ip = requests.get(
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all")
    a = Ip.text.split("\n")
    b = list(a)

    await ctx.send(f"Sending IP to {ctx.message.author.mention}'s dm.")
    await asyncio.sleep(2)
    channel = await ctx.message.author.create_dm()
    await channel.send(f"{israel}'s IP: ||{random.choice(b)}||")


@client.command(pass_context=True, name='joke')
async def joke(ctx, user: discord.User):
    await ctx.send(f"{user.mention} doesn't know about joke!!!")


@client.command(pass_context=True, name='advice')
async def advice(ctx, *, user: discord.Member = None):
    r = requests.get("https://api.adviceslip.com/advice")
    ok = json.loads(r.text)
    if user != None:
        await ctx.send(f"{user.mention}, {ok['slip']['advice']}")
    else:
        await ctx.send(ok['slip']['advice'])


@client.command(pass_context=True, name='troll')
async def troll(ctx, user: discord.User):
    global trolling
    trolling = True
    await ctx.message.delete()
    channel = await user.create_dm()
    webhook = Webhook.from_url(
        "https://discordapp.com/api/webhooks/862874757347278899/nP2eqq4XbtJYDI7WkePjn6jNgme1QA1O8-_0NmPMZQEOdc6rAnSKsa3zL1LvgfLnWpKC", adapter=RequestsWebhookAdapter())
    webhook.send(str(ctx.message.author) +
                 " have started trolling " + str(user))
    while trolling:
        myurl = "https://cdn.discordapp.com/attachments/789852217737084968/864117255855276052/unknown.png"
        async with aiohttp.ClientSession() as session:
            async with session.get(myurl) as resp:
                if resp.status != 200:
                    print("Could not download file..")
                data = io.BytesIO(await resp.read())
                await channel.send(file=discord.File(data, 'haha.png'))


@client.command(pass_context=True, name='dadjoke')
async def dadjoke(ctx):
    r = requests.get('https://icanhazdadjoke.com',
                     headers={"Accept": "application/json"})
    joke = json.loads(r.text)
    realjoke = joke['joke']
    await ctx.send(realjoke)


@client.command(pass_context=True, name='randomevent')
async def randomevent(ctx):
    r = requests.get("http://numbersapi.com/random/date")
    await ctx.send(r.text)


@client.command(pass_context=True, name='trollstop')
async def trollstop(ctx):
    global trolling
    trolling = False
    await ctx.channel.purge(limit=1)
    webhook = Webhook.from_url(
        "https://discordapp.com/api/webhooks/862874757347278899/nP2eqq4XbtJYDI7WkePjn6jNgme1QA1O8-_0NmPMZQEOdc6rAnSKsa3zL1LvgfLnWpKC", adapter=RequestsWebhookAdapter())
    webhook.send(str(ctx.message.author) + " have stopped trolling.")


@client.command(pass_context=True, name='kidnap')
async def kidnap(ctx, *, user: discord.Member):
    global ok
    a = random.choice(ok)
    if a == "true":
        await ctx.send(f"{ctx.message.author.mention} have kidnapped {user.mention}")
    elif a == "false":
        await ctx.send(f"{ctx.message.author.mention} tried to kidnap {user.mention} but the police saw them and catched them in an instant.")


linkname = None
asking = False
currentmessaging = None


@client.command(pass_context=True, name='hyperlink')
async def hyperlink(ctx, *, name: str):
    await ctx.message.delete()
    global linkname
    linkname = name
    global asking
    asking = True
    global currentmessaging
    currentmessaging = ctx.message.author.id
    ok = await ctx.author.create_dm()
    await ok.send(f"Your hyperlink's link name will be {linkname}, please put a link in the server you're currently messaging.")


@client.command(pass_context=True, name='destroy')
async def destroy(ctx, *, item: str):
    await ctx.send(f"{ctx.message.author.mention} have destroyed {item}!!")


@client.command(pass_context=True, name='fruit')
async def fruit(ctx, *, fruit: str):
    ok = requests.get(f"https://www.fruityvice.com/api/fruit/{fruit}")
    bruh = json.loads(ok.text)

    embed = discord.Embed(
        title=f'{fruit.capitalize()}',
        description=f"Genus: {bruh['genus']}\nName: {bruh['name']}\nFamily: {bruh['family']}\nNutritions:\n\n\tCarbohydrates: {bruh['nutritions']['carbohydrates']}\n\tProtein: {bruh['nutritions']['protein']}\n\tFat: {bruh['nutritions']['fat']}\n\tCalories: {bruh['nutritions']['calories']}\n\tSugar: {bruh['nutritions']['sugar']}",
        color=discord.Color.from_rgb(255,179,0)
    )

    await ctx.send(embed=embed)


@fruit.error
async def fruit_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("**Fruit was not found.**")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("**Missing Argument.**")


@client.command(pass_context=True, name='fact')
async def fact(ctx):
    global verycoolfact
    randomfact = random.choice(verycoolfact)
    await ctx.send(f"Fun Fact: {randomfact}")


@client.command(pass_context=True, name='swag')
async def swag(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    swag = Image.open("swag.png")
    asset = user.avatar_url_as(size=128)
    data = io.BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp.resize((137, 133))
    swag.paste(pfp, (50, 77))
    swag.save('swaggy.png')
    await ctx.send(file=discord.File("swaggy.png"))


@client.command(pass_context=True, name='fear')
async def fear(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    fear = Image.open('fear.png')
    asset = user.avatar_url_as(size=128)
    data = io.BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp.resize((125, 96))
    fear.paste(pfp, (0, 101))
    fear.save('feary.png')
    await ctx.send(file=discord.File('feary.png'))


@client.command(pass_context=True, name='wanted')
async def wanted(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    wanted = Image.open('wanted.png')
    asset = user.avatar_url_as(size=256)
    data = io.BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp.resize((500, 500))
    wanted.paste(pfp, (62, 174))
    wanted.save('wantedy.png')
    await ctx.send(file=discord.File('wantedy.png'))

meme_number = 0
meme_text1 = ''
meme_text2 = ''
memeing = False
whomeme = None
howmeme = 0


@client.command(pass_context=True, name='memegenerator')
async def memegenerator(ctx, memenum=None):
    global meme_number
    global memeing
    global whomeme
    global howmeme
    if memenum == None:
        meme_number = 0
    else:
        meme_number = memenum
    memeing = True
    whomeme = ctx.author.id
    howmeme = 1
    await ctx.send("Give text 1")


@client.command(pass_context=True, name='allmemes')
async def allmemes(ctx):
    currentpage = 1
    embed = discord.Embed(
        color=discord.Color.from_rgb(255,179,0),
        timestamp=datetime.datetime.utcnow()
    )
    embed1 = discord.Embed(
        color=discord.Color.from_rgb(255,179,0),
        timestamp=datetime.datetime.utcnow()
    )
    embed2 = discord.Embed(
        color=discord.Color.from_rgb(255,179,0),
        timestamp=datetime.datetime.utcnow()
    )
    embed3 = discord.Embed(
        color=discord.Color.from_rgb(255,179,0),
        timestamp=datetime.datetime.utcnow()
    )

    data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
    images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]

    # Page 1
    ctr = 1
    for i in range(0,25):
        embed.add_field(name=str(ctr), value=f'```{images[i]["name"]}```', inline=True)
        ctr += 1
    embed.set_footer(text=f'Current Page: 1')
    embed.set_author(name='All Memes', icon_url='https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256')
    

    # Page 2
    ctr1 = 26
    for i in range(25,51):
        embed1.add_field(name=str(ctr1), value=f'```{images[i]["name"]}```', inline=True)
        ctr1 += 1
    embed1.set_footer(text=f'Current Page: 2')
    embed1.set_author(name='All Memes', icon_url='https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256')

    # Page 3
    ctr2 = 51
    for i in range(50,76):
        embed2.add_field(name=str(ctr2), value=f'```{images[i]["name"]}```', inline=True)
        ctr2 += 1
    embed2.set_footer(text=f'Current Page: 3')
    embed2.set_author(name='All Memes', icon_url='https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256')
    

    # Page 4
    ctr3 = 76
    for i in range(75,100):
        embed3.add_field(name=str(ctr3), value=f'```{images[i]["name"]}```', inline=True)
        ctr3 += 1
    embed3.set_footer(text=f'Current Page: 4')
    embed3.set_author(name='All Memes', icon_url='https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256')

    m = await ctx.send(
        embed=embed,
        components = [
            [
                Button(label='<', style=ButtonStyle.grey, custom_id='<'),
                Button(label='>', style=ButtonStyle.grey, custom_id='>')
            ]
        ]
    )
    print("Sent message!")
    while True:
        interaction = await client.wait_for("button_click")
        if interaction.component.label == ">":
            if currentpage == 4:
                currentpage = 1
            else:
                currentpage += 1
        elif interaction.component.label == "<": 
            if currentpage == 1:
                currentpage = 4
            else:
                currentpage -= 1
        if currentpage == 1:
            await m.edit(
                embed=embed,
                components = [
                    [
                        Button(label='<', style=ButtonStyle.grey, custom_id='<'),
                        Button(label='>', style=ButtonStyle.grey, custom_id='>')
                    ]
                ]
            )
        elif currentpage == 2:
            await m.edit(
                embed=embed1,
                components = [
                    [
                        Button(label='<', style=ButtonStyle.grey, custom_id='<'),
                        Button(label='>', style=ButtonStyle.grey, custom_id='>')
                    ]
                ]
            )
        elif currentpage == 3:
            await m.edit(
                embed=embed2,
                components = [
                    [
                        Button(label='<', style=ButtonStyle.grey, custom_id='<'),
                        Button(label='>', style=ButtonStyle.grey, custom_id='>')
                    ]
                ]
            )
        elif currentpage == 4:
            await m.edit(
                embed=embed3,
                components = [
                    [
                        Button(label='<', style=ButtonStyle.grey, custom_id='<'),
                        Button(label='>', style=ButtonStyle.grey, custom_id='>')
                    ]
                ]
            )


@client.event
async def on_message_delete(message):
    global messagedeleted
    global whodeleted
    messagedeleted = message.content
    whodeleted = message.author


@client.command(pass_context=True, name='snipe')
async def snipe(ctx):
    global messagedeleted
    global whodeleted
    if (messagedeleted == None and whodeleted == None) or (messagedeleted == None and whodeleted != None) or (messagedeleted != None and whodeleted == None):
        embed = discord.Embed(
            description="There's currently nothing to snipe!",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.from_rgb(255,179,0)
        )
        await ctx.send(embed=embed)
    else:
        avatar = whodeleted.avatar_url
        embed = discord.Embed(
            description=str(messagedeleted),
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.from_rgb(255,179,0)
        )
        embed.set_author(name=str(whodeleted), icon_url=avatar)
        await ctx.send(embed=embed)
    await asyncio.sleep(60)
    messagedeleted = None
    whodeleted = None


@client.command(pass_context=True, name='findghost')
async def findghost(ctx):
    now = datetime.datetime.now()
    check = now.strftime('%p')
    morning = {'No ghost': 95, 'Pocong': 5, 'Dracula': 5, 'Pontianak': 5}
    night = {'No ghost': 50, 'Pocong': 10, 'Dracula': 10, 'Pontianak': 10}
    pocong = 'https://png.pngtree.com/png-clipart/20200701/original/pngtree-ghost-cartoon-pocong-png-image_5390788.jpg'
    dracula = 'https://i.graphicmama.com/uploads/2019/3/5c8a274f98cb6-Little%20Vampire%20Kid%20Vector%20Cartoon%20Character.png'
    pontianak = 'https://64.media.tumblr.com/40bfdbf433d5f905dcae6c3f2cd93770/3c40d0d0a0d9b1c6-f3/s2048x3072/00c7a9e1283e98cd573d42f774ee8f881f740e3a.png'
    if check == 'AM':
        morning_random = chances.Chances(morning)
        if morning_random == 'No ghost':
            embed1 = discord.Embed(
                title=f'You found no ghost!',
                timestamp=datetime.datetime.utcnow(),
                description="Sadly you didn't found any ghost! Try using frost fact to get the secret way on how to easily get ghosts.",
                color=discord.Color.from_rgb(255,179,0)
            )
            await ctx.send(embed=embed1)
        elif morning_random == 'Pocong':
            embed2 = discord.Embed(
                title=f'You found a pocong!',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.from_rgb(255,179,0)
            )
            embed2.set_image(url=pocong)
            await ctx.send(embed=embed2)
        elif morning_random == 'Dracula':
            embed3 = discord.Embed(
                title='You found a dracula!',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.from_rgb(255,179,0)
            )
            embed3.set_image(url=dracula)
            await ctx.send(embed=embed3)
        elif morning_random == 'Pontianak':
            embed4 = discord.Embed(
                title='You found a pontianak!',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.from_rgb(255,179,0)
            )
            embed4.set_image(url=pontianak)
            await ctx.send(embed=embed4)
    elif check == 'PM':
        night_random = chances.Chances(night)
        if night_random == 'No ghost':
            embed1 = discord.Embed(
                title=f'You found no ghost!',
                timestamp=datetime.datetime.utcnow(),
                description="Sadly you didn't found any ghost! Try using frost fact to get the secret way on how to easily get ghosts.",
                color=discord.Color.from_rgb(255,179,0)
            )
            await ctx.send(embed=embed1)
        elif night_random == 'Pocong':
            embed2 = discord.Embed(
                title=f'You found a pocong!',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.from_rgb(255,179,0)
            )
            embed2.set_image(url=pocong)
            await ctx.send(embed=embed2)
        elif night_random == 'Dracula':
            embed3 = discord.Embed(
                title='You found a dracula!',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.from_rgb(255,179,0)
            )
            embed3.set_image(url=dracula)
            await ctx.send(embed=embed3)
        elif night_random == 'Pontianak':
            embed4 = discord.Embed(
                title='You found a pontianak!',
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.from_rgb(255,179,0)
            )
            embed4.set_image(url=pontianak)
            await ctx.send(embed=embed4)


@client.command(pass_context=True, name='suggestfact')
async def suggestfact(ctx, *, message):
    webhook.SendMessage(
        message, "https://discord.com/api/webhooks/911880793327034398/gZFQpsj03Sakpy-__ICyP8JCkwIdDlnqu1FCB3sHMsqXd8XhsdGFZP4tMKzVa-5a9kV4")
    await ctx.send("Fact suggested!")


@client.command(pass_context=True, name='suggestghost')
async def suggestghost(ctx, picture, ghostname):
    webhook.SendMessage(ghostname + '\n' + picture,
                        "https://discord.com/api/webhooks/911880736506789898/uoqZ-8g98Ss3ljbfunz5JxXgvWXMoFIS9bft0Cf8kTqgaN3d2HQ9OD0oMms9Na5YsS3n")
    await ctx.send("Ghost suggested!")


@client.command(pass_context=True, name='suggestcommand')
async def suggestcommand(ctx, *, command):
    webhook.SendMessage(
        command, "https://discord.com/api/webhooks/911880668252872794/ttwQQtsFIYiWDr6mKJbwohRbP6lcHBf_Ws_Eh8LxQ-lrlYlNoc0MpAYh04AxcY2QMkF8")
    await ctx.send("Command suggested!")


@client.command(pass_context=True, name='invitelink', aliases=['invite'])
async def invitelink(ctx):
    embed=discord.Embed(
        title=f'Invite {client.user.name}',
        description=f'Invite {client.user.name} to your server by clicking the button below or copy this link, https://discord.com/api/oauth2/authorize?client_id=862253094746325002&permissions=8&scope=bot',
        color=discord.Color.from_rgb(255,179,0)
    )
    embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=ctx.author.avatar_url)
    await ctx.send(
        embed=embed,
        components = [
            [Button(label = 'Invite now!', custom_id = "invitelink", style=ButtonStyle.URL, url=f'https://discord.com/api/oauth2/authorize?client_id=862253094746325002&permissions=8&scope=bot')]
        ],
    )


@client.command(pass_context=True, name='getrobloxdata')
async def getrobloxdata(ctx, user: discord.User = None):
    if user == None:
        user = ctx.author
    a = requests.get(f"https://verify.eryn.io/api/user/{user.id}", headers={"Accept": "application/json"})
    apifirst = json.loads(a.text)
    await ctx.send(f"{user.mention} is not verified on RoVer, ask them to verify here: https://verify.eryn.io/") if apifirst['status'] == 'error' else print("Successfully fetched data")
    b = requests.get(f"https://roblox.data-viewer.ga/user/{apifirst['robloxUsername']}/raw", headers={"Accept": "application/json"})
    secondapi = json.loads(b.text)
    player = await roblox.get_user(apifirst['robloxId'])
    ispremium = await player.has_premium()
    if apifirst['status'] == "ok":
        embed = discord.Embed(
            color=discord.Color.from_rgb(255,179,0),
            timestamp=datetime.datetime.utcnow()
        )
        omg = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={apifirst["robloxId"]}&size=100x100&format=Png&isCircular=false', headers={"Accept": "application/json"})
        avatar = json.loads(omg.text)
        omgomg = avatar['data'][0]['imageUrl']
        pastnames = ', '.join(secondapi['oldNames']) or 'None'
        blurb = secondapi['blurb'] or 'None'
        status = secondapi['status'] or 'None'
        embed.set_thumbnail(url=omgomg)
        embed.set_footer(text=f'Requested by {ctx.author.name}')
        embed.set_author(name=f"{apifirst['robloxUsername']}'s data",icon_url=user.avatar_url)
        embed.add_field(name='Username', value=f"```{secondapi['username']}```", inline=True)
        embed.add_field(name='Display Name', value=f"```{secondapi['displayName']}```", inline=True)
        embed.add_field(name='Status', value=f"```{status}```", inline=True)
        embed.add_field(name='About', value=f"```{blurb}```", inline=False)
        embed.add_field(name='Joined at', value=f"```{player.created.strftime('%m/%d/%Y')}```", inline=True)
        embed.add_field(name='Account age', value=f"```{secondapi['age']}```", inline=True)
        embed.add_field(name='Friends', value=f"```{secondapi['friendCount']}```", inline=True)
        embed.add_field(name='Followers', value=f"```{secondapi['followerCount']}```", inline=True)
        embed.add_field(name='Is Premium', value=f"```{ispremium}```", inline=True)
        embed.add_field(name='Following', value=f"```{secondapi['followingCount']}```", inline=True)
        embed.add_field(name='Past Names', value=f"```{pastnames}```", inline=False)
        embed.add_field(name='Is Banned', value=f"```{secondapi['isBanned']}```", inline=True)
        embed.add_field(name='User ID', value=f"```{apifirst['robloxId']}```", inline=True)
        await ctx.send(embed=embed)


@client.command(pass_context=True,name='buttons')
async def buttono(ctx):
    m = await ctx.send(
        "These are the list of all buttons",
        components = [
            [Button(label = "Primary Button!", custom_id = "primary", style=ButtonStyle.blue), 
            Button(label = "Secondary Button!", custom_id = "secondary", style=ButtonStyle.grey),
            Button(label = "Success Button!", custom_id = "success", style=ButtonStyle.green),
            Button(label = "Danger Button!", custom_id = "danger", style=ButtonStyle.red),
            Button(label = "Link Button!", custom_id = "link", style=ButtonStyle.URL, url="https://example.com")]
        ],
    )
    while True:
        interaction = await client.wait_for("button_click")
        await interaction.respond(content=f'You clicked {interaction.component.label}')

@client.command(pass_context=True,name='report')
async def report(ctx, user:discord.User=None, *, reason: str):
    await ctx.message.delete()
    webhook.SendMessage(f"New report: {user.mention} was reported with the reason {reason}", "https://discord.com/api/webhooks/911879387790594058/qY-EkjwNqQpJsUPE1915nbACHXmERBr7WG6TzfrMf6vbdkUSpTvJcIMxE7h0GuKrtfF1")


@client.command(pass_context=True,name='randompicture')
async def randompicture(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://picsum.photos/200/300') as resp:
            if resp.status != 200:
                return print("Could not download file..")
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, 'bapaktibe.png'))


@client.command(pass_context=True, name='servercount')
async def servercount(ctx):
    embed = discord.Embed(
        description=f"{client.user.name} is currently in {str(len(client.guilds))} servers.\nInvite {client.user.name} to your server using `frost invitelink`!",
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    embed.set_author(name='Server Count', icon_url='https://cdn.discordapp.com/emojis/753325366139027457.png')
    embed.set_footer(text=f'Requested by {ctx.author.name}')

    await ctx.send(embed=embed)


aja = []
with open ('./texts/update.json', 'r') as f:
    updates = json.load(f)
    aja.append(updates['lastlist'][0])
@client.command(pass_context=True,name='update')
async def update(ctx, *, update):
    global aja
    if ctx.author.id == 737912807810662400:
        updates = None
        with open ('./texts/update.json', 'r') as f:
            updates = json.load(f)

        print(str(datetime.datetime.now().strftime('%m/%d/%Y')))
        if str(datetime.datetime.now().strftime('%m/%d/%Y')) == updates['today']:
            aja.append(updates['uptodate'])
            updates['lastupdate'] = aja
            updates['lastlist'] = updates['lastupdate']
            updates['uptodate'] = update
            updates['today'] = str(datetime.datetime.now().strftime('%m/%d/%Y'))
        else:
            updates['uptodate'] = update
            updates['lastlist'] = [update]
            updates['lastupdate'] = []
            updates['today'] = str(datetime.datetime.now().strftime('%m/%d/%Y'))
        await ctx.send("Successfully updated!")

        with open('./texts/update.json', 'w') as f:
            json.dump(updates, f, indent=2)
    else:
        await ctx.send("You are not the owner of Frost Bot therefore you cannot announce an update.")


@client.command(pass_context=True,name="currently")
async def currently(ctx, working: str='working', on: str='on', *, nano):
    if ctx.author.id == 737912807810662400:
        if working == 'working' and on == 'on':
            bersin = None
            with open('./texts/update.json', 'r') as f:
                bersin = json.load(f)
            
            bersin['currentwork'] = str(nano)

            with open('./texts/update.json', 'w') as f:
                json.dump(bersin, f, indent=2)
                await ctx.send("Currently Working is updated!")
        else:
            await ctx.send("Wrong parameters, please use frost working on (project) instead.")
    else:
        await ctx.send("You are not the owner of Frost Bot therefore you cannot set a current project.")


@client.command(pass_context=True,name='updates')
async def updates(ctx):
    with open('./texts/update.json', 'r') as f:
        a = json.load(f)
        await ctx.send(f"Frost bot's current update:\n{datetime.datetime.now().strftime('%m/%d/%Y')}\n```Last Update Today: {', '.join(a['lastupdate'])}\n\nCurrent Update: {a['uptodate']}```")


@client.command(pass_context=True,name='working')
async def working(ctx, on: str = 'on'):
    if on == 'on':
        with open('./texts/update.json', 'r') as f:
            acaca = json.load(f)
            await ctx.send(f"```{acaca['currentwork']}```")


@client.command(pass_context=True,name='headshot')
async def headshot(ctx, username): 
    user = await roblox.get_user_by_username(username)
    userid = user.id
    avatar = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={userid}&size=420x420&format=Png&isCircular=false', headers={"Accept": "application/json"}).json()['data'][0]['imageUrl']
    embed = discord.Embed(
        title=username,
        url=f'https://www.roblox.com/users/{userid}/profile',
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
    embed.set_image(url=avatar)

    await ctx.send(embed=embed)


@client.command(pass_context=True, name='circleav')
async def circleav(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    welcome = Image.open("welcome.png")
    
    asset = user.avatar_url_as(size = 128)
    data = io.BytesIO(await asset.read())
    img=Image.open(data).convert("RGB")
    img.tobytes()
    
    size = (141,139)
    mask = Image.new('L', size, 255)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + size, fill=0)
    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    output.paste(0, mask=mask)
    output.convert('P', palette=Image.ADAPTIVE)

    welcome.paste(output, (79,14))
    welcome.save("profile.png")

    await ctx.send(file=discord.File('profile.png'))


isimaging = False
imagelink = ''
imagename = ''
naming = False
whoimage = None
@client.command(pass_context=True,name='uploadimg')
async def uploadimg(ctx):
    global naming
    global isimaging
    global whoimage
    await ctx.send("Please send a picture.")
    isimaging = True
    naming = False
    whoimage = ctx.author.id


@client.command(pass_context=True, name='outfits')
async def outifts(ctx, name):
    player = await roblox.get_user_by_username(name)
    ok = requests.get(f"https://avatar.roblox.com/v1/users/{player.id}/outfits")
    outfits = json.loads(ok.text)
    omg = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={player.id}&size=100x100&format=Png&isCircular=false', headers={"Accept": "application/json"})
    avatar = json.loads(omg.text)
    omgomg = avatar['data'][0]['imageUrl']
    embed = discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    embed.add_field(name='Total Outift', value=f"```{outfits['total']}```", inline=False)
    for i in outfits['data']:
        embed.add_field(name=i['name'], value=f'```{i["id"]}```', inline=True)
    embed.set_author(name=f"{name}'s Outfits")
    embed.set_thumbnail(url=omgomg)
    embed.set_footer(text=f'Requested by {ctx.author.name}')
    await ctx.send(embed=embed)


@client.command(pass_context=True, name='getoutfit')
async def getoutfit(ctx, outfitid):
    aja = requests.get(f'https://thumbnails.roblox.com/v1/users/outfits?userOutfitIds={outfitid}&size=150x150&format=Png&isCircular=false')
    outfit = json.loads(aja.text)
    embed = discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    embed.set_author(name=f'OutfitID: {outfitid}')
    embed.set_image(url=outfit['data'][0]['imageUrl'])
    embed.set_footer(text=f'Requested by {ctx.author.name}')
    await ctx.send(embed=embed)


@getoutfit.error
async def getoutfit_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        error = discord.Embed(
            color=discord.Color.from_rgb(255,179,0)
        )
        error.set_author(name=f'**An error was found: Missing Argument.**', icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')
        await ctx.send(embed=error)


@client.command(pass_context=True, name='search')
async def search(ctx, max_search, *, args):
    if int(max_search) <= 25:
        parsed_link = urllib.parse.quote(args)
        url = f"https://google-search3.p.rapidapi.com/api/v1/search/q={parsed_link}&num={str(int(max_search) + 1)}"
        headers = {
            'x-user-agent': "desktop",
            'x-rapidapi-host': "google-search3.p.rapidapi.com",
            'x-rapidapi-key': Code(Codes.searchkey)
        }
        response = requests.request("GET", url, headers=headers)
        a = json.loads(response.text)

        for i in a['results']:
            await ctx.send(f"Title: {i['title']}\nLink: <{i['link']}>\n")

        await ctx.send(f"Total: {str(len(a['results']))}")
    else:
        await ctx.send("Sorry, but the maximum searched can't be more than 25.")


@search.error
async def search_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        error = discord.Embed(
            color=discord.Color.from_rgb(255,179,0)
        )
        error.set_author(name=f'**An error was found: Missing Argument.**', icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')
        await ctx.send(embed=error)


@client.command(pass_context=True, name='movie')
async def movie(ctx, *, movie_name: str):
    url = "https://imdb8.p.rapidapi.com/auto-complete"

    querystring = {"q":movie_name}

    headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': Code(Codes.searchkey)
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    a = json.loads(response.text)

    for i in a['d']:
        urla = "https://imdb8.p.rapidapi.com/title/get-synopses"

        querystringa = {"tconst":i['id']}

        headersa = {
            'x-rapidapi-host': "imdb8.p.rapidapi.com",
            'x-rapidapi-key': Code(Codes.searchkey)
            }

        tibe = requests.request("GET", urla, headers=headersa, params=querystringa)
        b = json.loads(tibe.text)

        embed = discord.Embed(
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.from_rgb(255,179,0)
        )
        embed.set_author(name=f"Movie Name: {i['l']}")
        embed.set_image(url=i['i']['imageUrl'])
        embed.add_field(name='Published On', value=f"```{i['y']}```", inline=True)
        embed.add_field(name='Type', value=f"```{i['q']}```", inline=True)
        embed.add_field(name='Movie ID', value=f"```{i['id']}```", inline=True)
        await ctx.send(embed=embed)
    await ctx.send(f"Total: {len(a['d'])}")
    await ctx.send(f"Short Synopses for {b[0]['id'].split('/')[2]}")
    await ctx.send(b[0]['text'].split('\n')[0])


@movie.error
async def movie_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        error = discord.Embed(
            color=discord.Color.from_rgb(255,179,0)
        )
        error.set_author(name=f'**An error was found: Missing Argument.**', icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')
        await ctx.send(embed=error)


@client.command(pass_context=True, name='ship')
async def ship(ctx, user: discord.Member=None, user1:discord.Member=None):
    await ctx.message.delete()
    if not user.bot and not user1.bot:
        url = "https://love-calculator.p.rapidapi.com/getPercentage"

        querystring = {"fname":user.name,"sname":user1.name}

        headers = {
            'x-rapidapi-host': "love-calculator.p.rapidapi.com",
            'x-rapidapi-key': Code(Codes.searchkey)
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        a = json.loads(response.text)

        await ctx.send(f"{a['fname']} x {a['sname']} = {a['percentage']}%\n{a['result']}")
    else:
        await ctx.send("Shipping someone with a bot is **illegal**")


@ship.error
async def ship_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        error = discord.Embed(
            color=discord.Color.from_rgb(255,179,0)
        )
        error.set_author(name=f'**An error was found: Missing Argument.**', icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')
        await ctx.send(embed=error)


@client.command(pass_context=True, name='covid19')
async def covid19(ctx, *, country):
    capitalized = country.capitalize()

    url = "https://covid-193.p.rapidapi.com/statistics"

    querystring = {"country":capitalized}

    headers = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': Code(Codes.searchkey)
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    tibe = json.loads(response.text)

    embed = discord.Embed(
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )

    cases = tibe['response'][0]['cases']['new'] or '0'
    active = tibe['response'][0]['cases']['active'] or '0'
    critical = tibe['response'][0]['cases']['critical'] or '0'
    recovered = tibe['response'][0]['cases']['recovered'] or '0'
    total = tibe['response'][0]['cases']['total'] or '0'
    death = tibe['response'][0]['deaths']['new'] or '0'
    totaldeath = tibe['response'][0]['deaths']['total'] or '0'
    
    embed.set_author(name=f"Covid-19 statistics for {capitalized}.", icon_url="https://apsic-apac.org/wp-content/uploads/2020/03/Coronavirus-CDC-645x645-statnews.jpg")
    embed.add_field(name="Newest Cases", value=f"```{cases}```", inline=True)
    embed.add_field(name="Active Cases", value=f"```{active}```", inline=True)
    embed.add_field(name="Critical Cases", value=f"```{critical}```", inline=True)
    embed.add_field(name="Recovered", value=f"```{recovered}```", inline=True)
    embed.add_field(name="Total Cases", value=f"```{total}```", inline=True)
    embed.add_field(name="Newest Deaths", value=f"```{death}```", inline=True)
    embed.add_field(name="Total Deaths", value=f"```{totaldeath}```", inline=True)
    await ctx.send(embed=embed)


@covid19.error
async def covid19_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        error = discord.Embed(
            color=discord.Color.from_rgb(255,179,0)
        )
        error.set_author(name=f'**An error was found: Missing Argument.**', icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')
        await ctx.send(embed=error)


@client.command(pass_context=True, name='shortenlink')
async def shortenlink(ctx, link:str="https://google.com"):
    await ctx.message.delete()
    url = urllib.parse.quote_plus(link)
    a = requests.get("https://urlshortener.smktd.repl.co/chilpit?link=" + str(url)).text.replace('"', '')
    await ctx.send(f"Your link is now shortened to: <{a}>")

@shortenlink.error
async def shortenlink_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        error = discord.Embed(
            color=discord.Color.from_rgb(255,179,0)
        )
        error.set_author(name=f'**An error was found: Missing Argument.**', icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')
        await ctx.send(embed=error)


@client.command(pass_context=True,name="urdict")
async def urdict(ctx, *, term:str):
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

    querystring = {"term":term}

    headers = {
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
        'x-rapidapi-key': Code(Codes.searchkey)
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    a = json.loads(response.text)

    error = discord.Embed(
        color=discord.Color.from_rgb(255,179,0)
    )
    error.set_author(name=f'Sorry, but we couldn\'t find: {term}', icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')

    if len(a['list']) > 0:
        for i in range(0,len(a['list'])):
            try:
                uhuks = str(a['list'][i]['written_on']).split('.')[0]
                written_on = datetime.datetime.strptime(uhuks, "%Y-%m-%dT%X").strftime("%Y/%m/%d at %I:%M %p")
                embed = discord.Embed(
                    timestamp=datetime.datetime.utcnow(),
                    color=discord.Color.from_rgb(255,179,0)
                )
                embed.set_author(name=term, icon_url="https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256")
                embed.add_field(name="Definition", value=f"```{str(a['list'][i]['definition']).replace('[','').replace(']','')}```", inline=False)
                embed.add_field(name="Example", value=f"```{str(a['list'][i]['example']).replace('[','').replace(']','')}```", inline=False)
                embed.add_field(name="Link", value=f"```{a['list'][i]['permalink']}```", inline=True)
                embed.add_field(name="Likes", value=f"```{a['list'][i]['thumbs_up']}```", inline=True)
                embed.add_field(name="Dislikes", value=f"```{a['list'][i]['thumbs_down']}```", inline=True)
                embed.add_field(name="Written on", value=f"```{written_on}```", inline=True)
                embed.add_field(name="Author", value=f"```{a['list'][i]['author']}```", inline=True)
                embed.set_footer(text=f"Requested by {ctx.author}")
                await ctx.send(embed=embed)
            except Exception as e:
                error1 = discord.Embed(
                    color=discord.Color.from_rgb(255,179,0)
                )
                error1.set_author(name=f"There was an error!\n\n{e}", icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')
                await ctx.send(embed=error1)
    else:
        await ctx.send(embed=error)

    
@urdict.error
async def urdict_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        error = discord.Embed(
            color=discord.Color.from_rgb(255,179,0)
        )
        error.set_author(name=f'**An error was found: Missing Argument.**', icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')
        await ctx.send(embed=error)

    
@client.command(pass_context=True, name="tts")
async def tts(ctx, *, message: str="Hello World!"):
    await ctx.message.delete()
    speaker = pyttsx3.init()
    speaker.save_to_file(message, "speech.mp3")
    speaker.runAndWait()
    await ctx.send(file=discord.File("speech.mp3"))


@tts.error
async def tts_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        error = discord.Embed(
            color=discord.Color.from_rgb(255,179,0)
        )
        error.set_author(name=f'**An error was found: Missing Argument.**', icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')
        await ctx.send(embed=error)


@client.command(pass_context=True, name="pin")
async def pin(ctx, details:str="true"):
    pin = await ctx.channel.pins()
    if details == "true":
        embed = discord.Embed(
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.from_rgb(255,179,0)
        )
        embed.set_author(name="Latest pinned message", icon_url="https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256")
        embed.add_field(name="Message", value=f"```{pin[0].content}```", inline=False)
        embed.add_field(name="Details", value=f"```{pin[0]}```", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed=embed)
    elif details == "false":
        embed = discord.Embed(
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.from_rgb(255,179,0)
        )
        embed.set_author(name="Latest pinned message", icon_url="https://cdn.discordapp.com/avatars/862253094746325002/c3d92c16920b504f69251973bdd107c4.webp?size=256")
        embed.add_field(name="Message", value=f"```{pin[0].content}```", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed=embed)
    else:
        error = discord.Embed(
            color=discord.Color.from_rgb(255,179,0)
        )
        error.set_author(name=f'That type of bool doesn\'t exist!', icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')
        await ctx.send(embed=error)


@pin.error
async def pin_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        error = discord.Embed(
            color=discord.Color.from_rgb(255,179,0)
        )
        error.set_author(name=f'**An error was found: Missing Argument.**', icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')
        await ctx.send(embed=error)


@client.command(pass_context=True,name='setgetrole')
@commands.has_permissions(manage_roles = True)
async def setgetrole(ctx, role_name:str, reaction:str, *, message:str):
    await ctx.message.delete()
    m = await ctx.send(message)
    await m.add_reaction(reaction)
    role = get(ctx.message.guild.roles, name=role_name)
    
    def check(reaction, user):
        if not user.bot:
            print(user.name)
            return user

    try:
        while True:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            if user:
                await user.add_roles(role, reason="Get Role By Reaction")
            else:
                pass
    except Exception as e:
        print(e)

    
@setgetrole.error
async def setgetrole_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        error = discord.Embed(
            color=discord.Color.from_rgb(255,179,0)
        )
        error.set_author(name=f'**An error was found: You do not have the required permission to use the setgetrole command!**', icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')
        await ctx.send(embed=error)
    elif isinstance(error, commands.MissingRequiredArgument):
        error = discord.Embed(
            color=discord.Color.from_rgb(255,179,0)
        )
        error.set_author(name=f'**An error was found: Missing Argument.**', icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')
        await ctx.send(embed=error)


@client.command(pass_context=True,name="poll")
async def poll(ctx, *, message:str):
    embed = discord.Embed(
        description=message,
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    embed.set_author(name=f"New poll by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    m = await ctx.send(embed=embed)
    try:
        await m.add_reaction('✅')
        await m.add_reaction('❌')
    except Exception as f:
        print(f)
    
    valid_emoji = ['✅', '❌']

    def check(reaction, user):
        if not user.bot and user != ctx.author and str(reaction.emoji) in valid_emoji:
            print(user.name)
            return user

    try:
        while True:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            if user:
                channel = await ctx.author.create_dm()
                if str(reaction.emoji) == "✅":
                    await channel.send(f"{user} said yes! to your poll: {message}")
                elif str(reaction.emoji) == "❌":
                    await channel.send(f"{user} said no! to your poll: {message}")
            else:
                pass
    except Exception as e:
        print(e)

    
@poll.error
async def poll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        error = discord.Embed(
            color=discord.Color.from_rgb(255,179,0)
        )
        error.set_author(name=f'**An error was found: Missing Argument.**', icon_url='https://images-ext-1.discordapp.net/external/tRyQekhx5OTGiDmVMdAVkAjWQHC_C5aqgP28EBD8HX4/https/img.icons8.com/fluent/96/unavailable.png')
        await ctx.send(embed=error)


@client.command(pass_context=True, name='about')
async def about(ctx):
    await ctx.send(
        "Frost Bot is a FREE premium bot with high-level commands created by Blue Duck#8344. Check out https://realfrostbot.repl.co/ for more information!",
        components=[
            [
                Button(label="Frost Bot's Website", style=ButtonStyle.URL, url="https://realfrostbot.repl.co/")
            ]
        ]
    )


@client.command(pass_context=True, name='omgip')
async def omgip(ctx, name, link):
    await ctx.message.delete()
    a = requests.get(link)
    b = json.loads(a.text)
    await ctx.send(f"Username: {name}\nIP: {b['ip']}\nContinent: {b['continent_name']}\nCountry: {b['country_name']}\nRegion: {b['region_name']}\nCity: {b['city']}\nCapital City: {b['location']['capital']}")


rbging = False
whorbging = None
@client.command(pass_context=True, name='removebg')
async def removebg(ctx):
    global rbging
    global whorbging
    await ctx.send("Please send an image url or straight up send an image.")
    rbging = True
    whorbging = ctx.author.id


@client.command(pass_context=True, name='textblob')
async def textblob(ctx, *, message:str=None):
    if message == None:
        await ctx.send("Missing required arguments.")
    a = TextBlob(message)
    b = a.sentiment.polarity    

    if b < 0:
        await ctx.send("Negative")
        webhook.SendMessage(f"{ctx.author.mention} typed a negative message {message}. Detected using sentiment analiser", "https://discord.com/api/webhooks/911880927272112138/5pr_g81k6QPQQVTj4uQzXwh-ME-8pYXXR81hKiT5cgvJGTjjBJ_MSWhpLhI7btn6_tJO")
    elif b == 0:
        await ctx.send("Neutral")
    elif b > 0 and b <= 1:
        await ctx.send("Positive")


# @client.command(pass_context=True,name="ytmp4")
# async def ytmp4(ctx, link:str="https://www.youtube.com/watch?v=QtBDL8EiNZo"):
#     await ctx.message.delete()

#     url = "https://ytstream-download-youtube-videos.p.rapidapi.com/dl"
#     a = link.split("v=")[1]
#     querystring = {"id":a}
#     headers = {
#         'x-rapidapi-host': "ytstream-download-youtube-videos.p.rapidapi.com",
#         'x-rapidapi-key': Code(Codes.searchkey)
#     }
#     response = requests.request("GET", url, headers=headers, params=querystring)
#     hmm = json.loads(response.text)
#     b = discord.Embed(
#         timestamp=datetime.datetime.utcnow(),
#         color=discord.Color.from_rgb(255,179,0)
#     )

#     category = "None" if hmm["category"] == "" else hmm["category"]
#     description = "None" if hmm['description'] == "" else hmm['description']

#     b.set_thumbnail(url=hmm['thumb'])
#     b.set_author(name=hmm['title'], url=link)
#     b.add_field(name="Title", value=hmm['title'], inline=True)
#     b.add_field(name="Author", value=hmm['author'], inline=True)
#     b.add_field(name="Length", value=hmm['length'], inline=True)
#     b.add_field(name="Description", value=description, inline=False)
#     b.add_field(name="Category", value=category, inline=True)
#     b.add_field(name="Channel Link", value=f"https://www.youtube.com/channel/{hmm['channelid']}", inline=True)
#     b.add_field(name="Average Rating", value=hmm['avg_rating'], inline=True)
#     b.add_field(name="Video Links", value="_ _", inline=False)

#     url = "https://youtube-videos.p.rapidapi.com/mp4"

#     querystring = {"videoId":a}

#     headers = {
#         'x-rapidapi-host': "youtube-videos.p.rapidapi.com",
#         'x-rapidapi-key': Code(Codes.searchkey)
#     }

#     try:
#         hm = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)
#         cur = hm['items'][1]
#         b.add_field(name='Quality', value=cur['quality'], inline=False)
#         print("test")
#         a = cur['url']
#         babab = requests.get(str(cur['url']), allow_redirects=True)
#         print("hello")
#         print(babab.url)
#         await ctx.send(
#             embed = b,
#             components = [
#                 [
#                     Button(label="Video Link", style=ButtonStyle.URL, url=babab.url)
#                 ]
#             ]
#         )
#     except Exception as e:
#         print(e)


boreding = False
whoboreding = None
@client.command(pass_context=True, name="bored")
async def bored(ctx):
    global boreding
    global whoboreding
    embed = discord.Embed(
        title = "Please choose a type!",
        description="""
        1. Education
        2. Recreational
        3. Social
        4. DIY
        5. Charity
        6. Cooking
        7. Relaxation
        8. Music
        9. Busywork
        """,
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    await ctx.send(embed=embed)
    await ctx.send("Please send the type number!")
    boreding = True
    whoboreding = ctx.author.id


@client.command(pass_context=True, name='qr')
async def qr(ctx, link:str="https://www.youtube.com/watch?v=QtBDL8EiNZo"):
    await ctx.message.delete()
    a = requests.get(link)
    if a.status_code == 200:
        try:
            hm = qrcode.make(link)
            with BytesIO() as f:
                hm.save(f, format="PNG")
                f.seek(0)
                okok = await ctx.author.create_dm()
                await okok.send(f"This is your qr code for the link ||{link}||")
                await okok.send(file=discord.File(fp=f, filename='image.png'))
        except Exception as e:
            print('error ' + str(e))
    else:
        await ctx.send("The link given doesn't exist.")


@client.command(pass_context=True,name='getminecraftdata')
async def getminecraftdata(ctx, namie:str="Notch"):
    url = "https://minecraft-user-data.p.rapidapi.com/"
    querystring = {"name":namie}
    headers = {
        'x-rapidapi-host': "minecraft-user-data.p.rapidapi.com",
        'x-rapidapi-key': Code(Codes.searchkey)
    }
    a = requests.get(url, headers=headers, params=querystring)
    if a.status_code == 200:
        try:
            b = json.loads(a.text)

            embed = discord.Embed(
                timestamp=datetime.datetime.utcnow(),
                color=discord.Color.from_rgb(255,179,0)
            )

            profile = MojangAPI.get_profile(MojangAPI.get_uuid(namie))
            skin = profile.skin_url

            embed.set_thumbnail(url=skin)
            embed.set_author(name=b['name'])
            embed.add_field(name="ID", value=f"```{b['id']}```", inline=False)
            embed.add_field(name="_ _", value="_ _", inline=True)
            embed.add_field(name="Past Names", value="_ _", inline=True)
            embed.add_field(name="_ _", value="_ _", inline=True)
            

            for i in b['name-history']:
                createdat = datetime.datetime.utcfromtimestamp(int(str(i['changedToAt'])[0:-3])).strftime('%Y/%m/%d %I:%M:%S %p') if "changedToAt" in i else 'First Name'
                embed.add_field(name=i['name'], value=f"```{createdat}```", inline=True)
            embed.set_footer(text=f"Requested by {ctx.author}")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("An error was found!\n\n{}".format(e))
    else:
        await ctx.send("Can't find that Minecraft user.")


@client.command(pass_context=True, name='rhyme')
async def rhyme(ctx, word:str):
    a = json.loads(requests.get(f"https://rhymebrain.com/talk?function=getRhymes&word={word}").text)
    await ctx.send(f"These are 10 words that rhymes with the word {word}.")
    for i in range(1,11):
        b = a[i]
        await ctx.send(f"{i}. {b['word']}")


gmanum = None
whogmanum = None
gmanuming = False
isbirthdaying = False
@client.command(pass_context=True, name='guessmyage', aliases=['gma'])
async def guessmyage(ctx):
    global gmanuming,gmanum,whogmanum
    global isbirthdaying
    gmanum = 2
    isbirthdaying = True
    gmanuming = False
    await ctx.send("Have you celebrated your birthday this year? (yes or no)")
    gmanum = None
    whogmanum = ctx.author.id
    gmanuming = True


@client.command(pass_context=True, name='craftyisasussybaka')
async def craftyisasussybaka(ctx):
    await ctx.send("Yes, I agree.")


@client.command(pass_context=True, name='blueduckisasussybaka')
async def craftyisasussybaka(ctx):
    await ctx.send("No, I don't agree.")


@client.command(pass_context=True, name='addcapsperm', aliases=['addcperm', 'acp'])
async def addcapsperm(ctx, user: discord.Member=None):
    if ctx.author.id == 737912807810662400:
        if user != None:
            capsperm = None
            with open('./texts/capsperm.json', 'r') as f:
                capsperm = json.load(f)

            if str(user.id) not in capsperm['data']:
                capsperm['data'].append(str(user.id))
                try:
                    with open('./texts/capsperm.json', 'w') as f:
                        json.dump(capsperm,f, indent=4)
                        await ctx.send(f"Successfully whitelisted {user.mention} for caps perm!")
                except Exception as e:
                    await ctx.send(f"There was an error when whitelisting!\n\n{e}")
            else:
                await ctx.send(f"{user.mention} is already whitelisted in caps perm!")
        else:
            await ctx.send("You did not fill the required argument! Please fill it correctly.")
    else:
        await ctx.send("You do not have the required permission to use addcapsperm.")


@client.command(pass_context=True, name='removecapsperm', aliases=['removecperm','rcp'])
async def removecperm(ctx, user: discord.Member=None):
    if ctx.author.id == 737912807810662400:
        if user != None:
            capsperm = None
            with open('./texts/capsperm.json', 'r') as f:
                capsperm = json.load(f)

            if str(user.id) in capsperm['data']:
                capsperm['data'].pop(capsperm['data'].index(str(user.id)))
                try:
                    with open('./texts/capsperm.json', 'w') as f:
                        json.dump(capsperm, f, indent=4)
                        await ctx.send(f"Successfully blacklisted {user.mention} from caps perm!")
                except Exception as e:
                    await ctx.send(f"There was an error when blacklisting!\n\n{e}")
            else:
                await ctx.send(f"{user.mention} is not whitelisted therefore can't be blacklisted.")
        else:
            await ctx.send("You did not fill the required argument! Please fill it correctly.")
    else:
        await ctx.send("You do not have the required permission to use removecapsperm!")
        

@client.command(pass_context=True, name="addbadperm")
async def addbadperm(ctx, user: discord.Member=None):
    if ctx.author.id == 737912807810662400:
        if user != None:
            capsperm = None
            with open('./texts/badperm.json', 'r') as f:
                capsperm = json.load(f)

            if str(user.id) not in capsperm['data']:
                capsperm['data'].append(str(user.id))
                try:
                    with open('./texts/badperm.json', 'w') as f:
                        json.dump(capsperm,f, indent=4)
                        await ctx.send(f"Successfully whitelisted {user.mention} for bad perm!")
                except Exception as e:
                    await ctx.send(f"There was an error when whitelisting!\n\n{e}")
            else:
                await ctx.send(f"{user.mention} is already whitelisted in bad perm!")
        else:
            await ctx.send("You did not fill the required argument! Please fill it correctly.")
    else:
        await ctx.send("You do not have the required permission to use addbadperm.")


@client.command(pass_context=True, name='removebadperm')
async def removebadperm(ctx, user: discord.Member=None):
    if ctx.author.id == 737912807810662400:
        if user != None:
            capsperm = None
            with open('./texts/badperm.json', 'r') as f:
                capsperm = json.load(f)

            if str(user.id) in capsperm['data']:
                capsperm['data'].pop(capsperm['data'].index(str(user.id)))
                try:
                    with open('./texts/badperm.json', 'w') as f:
                        json.dump(capsperm, f, indent=4)
                        await ctx.send(f"Successfully blacklisted {user.mention} from bad perm!")
                except Exception as e:
                    await ctx.send(f"There was an error when blacklisting!\n\n{e}")
            else:
                await ctx.send(f"{user.mention} is not whitelisted therefore can't be blacklisted.")
        else:
            await ctx.send("You did not fill the required argument! Please fill it correctly.")
    else:
        await ctx.send("You do not have the required permission to use removebadperm!")


@client.command(pass_context=True, name="crime")
async def crime(ctx):
    randomCommit = ["drug distribution", "identity theft", "fraud", "shoplifting", "vandalism", "murder", "cyber bullying", "tax evasion", "hacking"]

    m = await ctx.send(
        "**What crime do you want to commit?**\n_Pick an option blow to commit one!_",
        components=[
            [
                Button(label=random.choice(randomCommit), style=ButtonStyle.blue, custom_id="1"),
                Button(label=random.choice(randomCommit), style=ButtonStyle.blue, custom_id="2"),
                Button(label=random.choice(randomCommit), style=ButtonStyle.blue, custom_id="3")
            ]
        ]
    )

    while True:
        interaction = await client.wait_for("button_click")

        await interaction.respond("")

        embed = discord.Embed(
            title = f"**{ctx.author.name} committed a {interaction.component.label.upper()}**",
            description = f"ok"
        )

        await m.edit(
            "",
            embed=embed
        )


@client.command(pass_context=True, name='ytmp4')
async def ytmp4(ctx):
    await ctx.send("Visit this website for youtubemp4! https://ytmp4.realfrostbot.repl.co")


@client.command(pass_context=True, name="ytmp3")
async def ytmp3(ctx):
    await ctx.send("Visit this website for youtubemp3! https://ytmp3.realfrostbot.repl.co")


@client.command(pass_context=True, name='ytshort')
async def ytshort(ctx):
    await ctx.send("Visit this website to download youtube shorts! https://youtubeshorts.smktd.repl.co")


@client.command(pass_context=True, name="flip")
async def flip(ctx):
    a = {"head": 50, "tail": 50}
    b = chances.Chances(a)
    if b == "head":
        myurl = "https://cdn.discordapp.com/attachments/918732557103824896/918804365874196540/xlrZx4dJW1MAAAAABJRU5ErkJggg.png"
        async with aiohttp.ClientSession() as session:
            async with session.get(myurl) as resp:
                if resp.status != 200:
                    print("Could not download file..")
                data = io.BytesIO(await resp.read())
                await ctx.send("It was head!", file=discord.File(data, "head.png"))
    elif b == "tail":
        myurl = "https://cdn.discordapp.com/attachments/918732557103824896/918804366083895406/AOvYn9ErP9y87Bat3RhqA5gAAAABJRU5ErkJggg.png"
        async with aiohttp.ClientSession() as session:
            async with session.get(myurl) as resp:
                if resp.status != 200:
                    print("Could nt download file!")
                data = io.BytesIO(await resp.read())
                await ctx.send("It was tail!", file=discord.File(data, "tail.png"))


@client.command(pass_context=True, name="futurepartner")
async def futurepartner(ctx, user: discord.Member=None):
    b = []
    if user == None:
        user = ctx.message.author

    for i in ctx.guild.members:
        if not i.bot and i != user:
            b.append(i)

    if user == ctx.message.author:
        await ctx.send(f"Your future partner is {random.choice(b).mention}!")
    else:
        await ctx.send(f"{user.mention}'s future partner is {random.choice(b).mention}")


@client.command(pass_context=True, name="wallpaper")
async def wallpaper(ctx):
    a = requests.get("https://wallpaperapi.smktd.repl.co/getwallpaper").text.replace('"','')
    data = await readURL(a)
    await ctx.send(file=discord.File(data, "wallpaper.png"))


@client.command(pass_context=True, name="phumor", aliases=["ph", "programmerh"])
async def phumor(ctx):
    try:
        ok = requests.get("https://www.reddit.com/r/ProgrammerHumor/new.json")
        a = json.loads(ok.text)
        b = []
        for i in a["data"]["children"]:
            if i["data"]["domain"] == "i.redd.it":
                b.append(str(f"{i['data']['url']}rock{i['data']['title']}"))

        c = random.choice(b)
        c = c.split("rock")
        image = c[0]
        title = c[1]
        embed = discord.Embed(
            title = title,
            color = discord.Color.from_rgb(255,179,0)
        )
        embed.set_image(url=image)

        await ctx.send(embed=embed)
    except Exception:
        ok = requests.get("https://www.reddit.com/r/ProgrammerHumor/new.json")
        while ok.status_code != 200:
            ok = requests.get("https://www.reddit.com/r/ProgrammerHumor/new.json")
            if ok.status_code == 200:
                a = json.loads(ok.text)
                b = []
                for i in a["data"]["children"]:
                    if i["data"]["domain"] == "i.redd.it":
                        b.append(str(f"{i['data']['url']}rock{i['data']['title']}"))

                c = random.choice(b)
                c = c.split("rock")
                image = c[0]
                title = c[1]

                embed = discord.Embed(
                    title = title,
                    color = discord.Color.from_rgb(255,179,0)
                )
                embed.set_image(url=image)

                await ctx.send(embed=embed)
                break


@client.command(pass_context=True, name="sourcecode", aliases=["sc", "source"])
async def sourcecode(ctx):
    embed = discord.Embed(
        title="Frost Bot Source Code",
        description="Frost bot is now public in github and runs 24/7! (might be down because of bugs)",
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(255,179,0)
    )
    await ctx.send(
        embed=embed,
        components=[
            [
                Button(label='Source Code', style=ButtonStyle.URL, url="https://github.com/CantCode023/FrostBot")
            ]
        ]
    )


@client.command(pass_context=True, name="wordthatstartswith", aliases=["uwu"])
async def uwu(ctx, query: str):
    a = requests.get("https://wordsthatstartswith.herokuapp.com/wordsThatStartsWith?char=" + query).text
    b = json.loads(a)
    for i in b['amount']+1:
        b = b['data'][i]
        await ctx.send(f"{i}. {b}")


@client.command(pass_context=True, name="getversion", aliases=["getver"])
async def getversion(ctx):
    a = openFile("currentVersion.txt")
    await ctx.send(a)
        


boredtype = None
isbirthday = False
whenborn,borning = None,False
@client.event
async def on_message(message):
    global picking
    global shooter
    global mentio
    global whatshot
    global currentmessaging
    global linkname
    global asking
    global titleing
    global dada
    global ok
    global meme_number
    global memeing
    global whomeme
    global meme_text1
    global meme_text2
    global howmeme
    global isimaging
    global imagelink 
    global imagename
    global naming
    global whoimage
    global rbging
    global whorbging
    global boreding
    global whoboreding
    global boredtype
    global gmanuming,gmanum,whogmanum,isbirthday,isbirthdaying,whenborn,borning
    # Webhook use frost bot
    ctx = await client.get_context(message)
    if ctx.valid and message.author.id == 873923972490756146:
        await client.invoke(ctx)
    # Chatbot
    if message.content.lower().startswith('back'):
        await message.reply("Welcome back!", mention_author=True)
    elif message.content.lower().startswith('afk'):
        await message.reply("I hope you'll be back soon!", mention_author=True)
    elif message.content.lower().startswith('gtg'):
        await message.reply("I'm sad to see you go :(", mention_author=True)
    elif message.content.lower().startswith('idc') or message.content.lower().startswith("i dont care"):
        my_url = "https://ishouldhavesaid.net/wp-content/uploads/2013/05/when-a-person-says-they-dont-care.jpg"
        async with aiohttp.ClientSession() as session:
            async with session.get(my_url) as resp:
                if resp.status != 200:
                    return print("Could not download file..")
                data = io.BytesIO(await resp.read())
                await message.reply(file=discord.File(data, 'cool_image.png'))
    elif message.content.lower().startswith("shut up"):
        myurl = "https://i.pinimg.com/originals/13/26/d3/1326d35a0ddd63161b9cec48c9db9adf.png"
        async with aiohttp.ClientSession() as session:
            async with session.get(myurl) as resp:
                if resp.status != 200:
                    return print("Could not download file..")
                data = io.BytesIO(await resp.read())
                await message.reply(file=discord.File(data, 'lol_image.png'))
    if 'sad' in message.content.lower():
        myurl = "https://media1.tenor.com/images/52c67089641063eda192dec105a487d7/tenor.gif?itemid=16537209"
        async with aiohttp.ClientSession() as session:
            async with session.get(myurl) as resp:
                if resp.status != 200:
                    print("Could not download file..")
                data = io.BytesIO(await resp.read())
                await message.reply(file=discord.File(data, "sad.gif"))
    elif 'get a life' in message.content:
        await message.reply("You mean like your meaningless life? No thanks, I'll pass.")
    # Shooting Options
    elif message.content.upper() == "A" and message.author.id == mentio:
        if picking == True:
            hmm = ['true', 'false']
            randompick = random.choice(hmm)
            if randompick == "true":
                await message.reply("Congrats! You successfully dodged!")
            elif randompick == "false":
                cool = random.choice(whatshot)
                await message.reply("You failed to dodge! Go to a training dude!")
                await message.reply(f"{shooter.mention} got a " + cool + "!")
        picking = False
    elif message.content.upper() == "B" and message.author.id == mentio:
        if picking == True:
            cool = random.choice(whatshot)
            await message.reply("You died! Rest In Peace.")
            await message.reply(f"{shooter.mention} got a " + cool + "!")
            picking = False
    # Hyperlink
    elif message.content.startswith("https") and asking == True and message.author.id == currentmessaging:
        dude = message.content
        await message.delete()
        await message.channel.send(embed=discord.Embed(title='', description=f"[{linkname}]({dude})", color=discord.Color.from_rgb(255,179,0)))
        asking = False
        currentmessaging = ""
    elif message.content.startswith("http") and asking == True and message.author.id == currentmessaging:
        bruh = message.content
        await message.delete()
        await message.channel.send(embed=discord.Embed(title='', description=f"[{linkname}]({bruh})", color=discord.Color.from_rgb(255,179,0)))
        asking = False
        currentmessaging = ""
    elif titleing == True and message.author.id == currentmessaging:
        await message.delete()
        embed = discord.Embed(
            title=dada,
            description=message.content,
            color=discord.Color.from_rgb(255,179,0)
        )
        await message.channel.send(embed=embed)
        titleing = False
    elif memeing and message.author.id == whomeme and howmeme == 1:
        if message.content == '_ _':
            meme_text1 = ''
        else:
            meme_text1 = message.content
        howmeme = 2
        await message.channel.send("Give text 2")
    elif memeing and message.author.id == whomeme and howmeme == 2:
        if message.content == '_ _':
            meme_text2 = ''
        else:
            meme_text2 = message.content
        URL = 'https://api.imgflip.com/caption_image'
        memes = requests.get(
            'https://api.imgflip.com/get_memes').json()['data']['memes']
        images = [{'name': image['name'], 'url':image['url'],
                   'id':image['id']}for image in memes]
        if meme_text1 == '' and meme_text2 == '':
            await message.channel.send("No texts specified. Remember, API request parameters are Http parameters not JSON.")
            params = {
                'username': username,
                'password': password(),
                'template_id': images[int(meme_number)-1]['id'],
                'text0': meme_text1,
                'text1': ' ',
            }
        else:
            params = {
                'username': username,
                'password': password(),
                'template_id': images[int(meme_number)-1]['id'],
                'text0': meme_text1,
                'text1': meme_text2,    
            }
        response = requests.request('POST', URL, params=params).json()  
        hehe = response['data']['url']
        async with aiohttp.ClientSession() as session:
            async with session.get(hehe) as resp:
                if resp.status != 200:
                    return print("Could not download file..")
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, 'lol_image.png'))
        memeing = False
        whomeme = 0
        meme_number = 0
        meme_text2 = ''
        meme_text1 = ''
        howmeme = 0
    elif rbging and whorbging == message.author.id:
        if message.attachments:
            try:
                try:
                    a = requests.post(
                        'https://api.remove.bg/v1.0/removebg',
                        data={
                            'image_url': message.attachments[0].url,
                            'size': 'auto'
                        },
                        headers={'X-Api-Key': Code(Codes.removebgkey)}
                    )
                except Exception:   
                    await ctx.send(f"There was an error!\n\n{traceback.format_exc()}")
                if a.status_code == 200:
                    try:
                        with open('e.png', 'wb') as f:
                            f.write(a.content)
                            await message.channel.send(file=discord.File(open('e.png', 'rb')))
                    except Exception:
                        await ctx.send(f"There was an error!\n\n{traceback.format_exc()}")
                else:
                    await message.channel.send("There was an error when trying to remove background!")
            except Exception as e:
                await message.channel.send(f"There was an error when trying to remove background! {e}")
            rbging = False
            whorbging = None
        else:
            try:
                a = requests.post(
                    'https://api.remove.bg/v1.0/removebg',
                    data={
                        'image_url': message.content,
                        'size': 'auto'
                    },
                    headers={'X-Api-Key': Code(Codes.removebgkey)}
                )
                if a.status_code == 200:
                    with open('e.png', 'wb') as f:
                        f.write(a.content)
                        await message.channel.send(file=discord.File(open('e.png', 'rb')))
                else:
                    await message.channel.send("There was an error when trying to remove background!")
            except Exception as e:
                await message.channel.send(f"There was an error when trying to remove background! {e}")
            rbging = False
            whorbging = None
    elif boreding and whoboreding == message.author.id:
        boredtype = int(message.content)
        okok = {
            "1" : "education",
            "2" : "recreational",
            "3" : "social",
            "4" : "diy",
            "5" : "charity",
            "6" : "cooking",
            "7" : "relaxation",
            "8" : "music",
            "9" : "busywork"
        }
        b = requests.get(f"https://www.boredapi.com/api/activity?type={okok[str(boredtype)]}")
        c = json.loads(b.text)
        await message.channel.send(f"Here's a fun activity to do!\n{c['activity']}")
        boredtype = None
        boreding = False
        whoboreding = None

    # Anti Caps
    with open("./texts/capsperm.json", "r") as f:
        fyou = json.load(f)

    currentcaps = 0
    if not message.author.bot:
        for a in str(re.sub('\W+','',str(message.content)).strip()):
            for i,c in enumerate(a):
                if c.isupper() and not str(message.author.id) in fyou['data']:
                    currentcaps += 1
                elif not c.isupper() and c != " ":
                    currentcaps = 0

    if currentcaps > 10:
        await message.delete()
        await message.channel.send(str(message.content).capitalize() + f"\n- {message.author.mention}")
        dm = await message.author.create_dm()
        await dm.send("Please do not use more than 10 caps!")

    # Anti Swear
    with open("./texts/badperm.json", "r") as f:
        poiyu = json.load(f)

    for i in badword:
        if i in str(re.sub('\W+','',str(message.content)).strip()).lower() and not message.author.bot:
            if str(message.author.id) not in poiyu['data']:
                await message.delete()
                channel = await message.author.create_dm()
                await channel.send(f"{message.author.mention}, stop sending bad words.")

    # Good Word
    for i in good_words:
        if i in message.content.lower() and message.author.id != client.user.id:
            await message.reply(f"You're {i}!")
            break

    # Guess My Age (gmanuming, gmanum, whogmanum)
    if isbirthdaying and message.author.id == whogmanum:
        if str(message.content).lower() == "yes":
            isbirthday = True
            isbirthdaying = False
            borning = True
            await message.channel.send("What year were you born?")
        elif str(message.content).lower() == "no":
            isbirthday = False
            isbirthdaying = False
            borning = True
            await message.channel.send("What year were you born?")
        else:
            await message.channel.send("Please restart!")
            gmanuming,gmanum,whogmanum,isbirthday,isbirthdaying,whenborn,borning = False,None,None,False,False,None,False
    elif borning and message.author.id == whogmanum:
        whenborn = int(message.content)
        a = None
        if isbirthday:
            a = 2*2+5*50+1768-whenborn+3-4
        else:
            a = 2*2+5*50+1767-whenborn+3-4
        await message.channel.send(f"You're {str(a)} years old!")
        gmanuming,gmanum,whogmanum,isbirthday,isbirthdaying,whenborn,borning = False,None,None,False,False,None,False
    elif "yamete~" in message.content.lower():
        await message.reply("wtf")


    # Process Commands
    await client.process_commands(message)


@client.event
async def on_guild_join(guild):
    try:
        joinchannel = guild.system_channel

        embed = discord.Embed(
            title='Thanks for inviting me to your server!',
            description="Invite me to your server too using [this](https://discord.com/api/oauth2/authorize?client_id=862253094746325002&permissions=8&scope=bot) link",
            color=discord.Color.from_rgb(255,179,0)
        )
        await joinchannel.send(embed=embed)
        serverinvite = await joinchannel.create_invite(max_age=0, max_uses=0, reason="Inviting the owner of Frost Bot to this server.")
        print(serverinvite)
        acah=None

        with open('./texts/servers.json', 'r') as f:
            acah = json.load(f)

        if guild.name in acah:
            print("Bot is already in this server.")
        else:
            acah[guild.name] = str(serverinvite)

        with open('./texts/servers.json', 'w') as f:
            json.dump(acah, f, indent=2)

    except:
        embed = discord.Embed(
            title='Thanks for inviting FrostGaming to your server!',
            description="Invite FrostGaming to your server [here](https://discord.com/api/oauth2/authorize?client_id=862253094746325002&permissions=8&scope=bot)",
            color=discord.Color.from_rgb(255,179,0)
        )
        await guild.text_channels[0].send(embed=embed)
        serverinvite = await joinchannel.create_invite(max_age=0, max_uses=0, reason="Inviting the owner of Frost Bot to this server.")


@client.event
async def on_member_join(member):
    await member.send(f"Have a great time in **{member.guild.name}**!\nPlease join this server for fun stories https://discord.gg/XPmynnNFMA")
    await member.guild.text_channels[0].send("https://cdn.discordapp.com/emojis/878191198060302337.png?size=40")
    await member.guild.text_channels[0].send(f"Say hello to our new member, {member.mention}!")


@client.event
async def on_member_remove(member):
    await member.guild.text_channels[0].send("https://cdn.discordapp.com/emojis/878191134516592641.png?size=40")
    await member.guild.text_channels[0].send(f"Please say goodbye to our \"used-to-be\" member, {member.mention}..")


client.run(Code(Codes.frostbot))  