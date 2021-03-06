import discord
import youtube_dl
import os
import requests
import json
import asyncio

from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from albumGenerator import AlbumGenerator

# client = discord.Client()
# creating a connection
command_prefix = '$'
# Loading in the .env file that has our guild token
load_dotenv('.env')
myId = os.getenv('PERSONAL_ID')
myGuild = os.getenv('GUILD_ID')
ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
        }

client = commands.Bot(os.getenv('COMMAND_PREFIX'))

# @ is a decorator functions
@client.event
async def on_ready():
    print('Bot is ready!')

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server')

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.command()
async def ping2(ctx):
    await ctx.send(f'{round(client.latency*1000)} ms')

@client.command()
async def clear(ctx, amount=5):
    if(amount >= 10):
        amount = 5
    await ctx.channel.purge(limit = amount)

@client.event
async def on_voice_state_update(member, before, after):
    voiceChannel = after.channel
    print(f'{member} has joined {voiceChannel}')
    if (member.bot or after.channel is None):                        # Checking that the bot does not trigger the rest of the code
        return
    songDirectory = f'theme-songs/{member}'
    song_there = os.path.isfile(f'{songDirectory}/themeSong.mp3')
    if (before.channel == None and after.channel != None and song_there):
        await voiceChannel.connect()
        await asyncio.sleep(0.5)
        voice: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=after.channel.guild)
        myAudio = FFmpegPCMAudio(f'{songDirectory}/themeSong.mp3')
        myAdjustedAudio = PCMVolumeTransformer(myAudio)
        myAdjustedAudio.volume = 0.1
        voice.play(myAudio)
        await asyncio.sleep(10)
        voice.stop()
        if voice.is_connected():
            await voice.disconnect()

@client.command()
async def join(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='anime')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None:
        await voiceChannel.connect()
    else:
        await ctx.send("I am already connected to a channel!")

@client.command()
async def p(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='anime')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None:
        await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        voice.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("audio-testing/draftSong.mp3"), volume=0.5))
        await asyncio.sleep(7)
        voice.stop()

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for current music to end")
        return
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='anime')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None:
        await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await client.send("I am not connected to a channel!")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await client.send("No audio playing.")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await client.send("Audio is not paused")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command(pass_context=True)
async def addThemeSong(ctx, url : str, member : discord.Member = None):
    await ctx.send("Loading theme song...")
    member = member or ctx.author
    songDirectory = f'theme-songs/{member}'
    hasThemeSongFolder = os.path.isdir(songDirectory)
    if hasThemeSongFolder:
        song_there = os.path.isfile(f'{songDirectory}/themeSong.mp3')
        try:
            if song_there:
                os.remove(f'{songDirectory}/themeSong.mp3')
        except PermissionError:
            await ctx.send("User has a folder, but no song file! Please contact dev.")
            return
    else:
        os.mkdir(f'{songDirectory}')
    try: 
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            for file in os.listdir('./'):
                if file.endswith(".mp3"):
                    os.rename(file, f'{songDirectory}/themeSong.mp3')
    except:
            await ctx.channel.purge(limit = 1)
            await ctx.send("Error downloading song! Please try again.")
    print("Theme Song successfully added!")
    await ctx.channel.purge(limit = 1)
    await ctx.send("Theme Song Added!")

@client.command()
async def playRex(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='anime')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None:
        await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio("audio-testing/Rexs_Journey_Remastered_1.mp3"))

@client.command()
async def playJaag(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='anime')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None:
        await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio("audio-testing/j.A.A.g_city_3.mp3"))


@client.command()
async def playKnowJoe(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='anime')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None:
        await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio("audio-testing/Know_Joe_Self.mp3"))


@client.command()
async def playWeBack(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='anime')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None:
        await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio("audio-testing/We_Back_feat._The_Buckets.mp3"))


# NEED TO MOVE TO SEPERATE MODULE IN THE FUTURE https://1001albumsgenerator.com/?joinGroup=discord-bot

@client.command()
async def joinGroup(ctx):                     
    ctx.send('https://1001albumsgenerator.com/?joinGroup=discord-bot')

@client.command()
async def aotd(ctx, username='swiftarrow4'):
    albumData = AlbumGenerator.GetAlbumOTD(username)

    embed = discord.Embed(title="{albumName} by {albumArtist}".format(**albumData), color=discord.Color.blue(), url="https://open.spotify.com/album/{albumSpotifyLink}?si=hV_-OPGBTHGvstYz1TjxbQ".format(**albumData))
    embed.set_image(url=albumData['albumImage'])
    await ctx.send(embed=embed)

@client.command()
async def vote(ctx, rating):
    if rating < 1 or rating > 5:
        return ctx.send('Please input a number between 1 and 5')
    await ctx.send(f'Please register to give a rating at {command_prefix}joinGroup')

@client.command()
async def summary(ctx, user='swiftarrow4'):
    response = requests.get(f'https://1001albumsgenerator.com/api/v1/projects/{user}')
    soup = BeautifulSoup(response.content, 'html.parser')
    # TODO: Parse html page for summary data
    responseData = json.loads(response.text)
    summary = responseData['shareableUrl']
    await ctx.send(f'Summary page for {user}: {summary}')

client.run(os.getenv('GUILD_TOKEN'))