import discord

from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from dotenv import load_dotenv
import youtube_dl
import os
import requests
import json
import asyncio

# client = discord.Client()
# creating a connection
client = commands.Bot(command_prefix = 'mybot ')
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

# @ is a decorator functionS
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
async def on_message(message):
    await client.process_commands(message)
    if (message.content.startswith('dog')):
        # response object is given to you
        request = requests.get('https://some-random-api.ml/img/dog')
        print(request.text)
        json_dog = json.loads(request.text)
        print(json_dog)
        
        request2 = requests.get('https://some-random-api.ml/facts/dog')
        json_fact = json.loads(request2.text)

        embed = discord.Embed(title='Here is a cool dog', color=discord.Color.blue())
        embed.set_image(url=json_dog['link'])
        embed.set_footer(text=json_fact['fact'])
        await message.channel.send(embed=embed)

@client.event
async def on_voice_state_update(member, before, after):
    print(f'{member} has made a voice state change')
    if (member.bot or after.channel is None):                        # Checking that the bot does not trigger the rest of the code
        return
    songDirectory = f'theme-songs\\{member}'
    song_there = os.path.isfile(f'{songDirectory}\\themeSong.mp3')
    if (before.channel == None and after.channel != None and song_there):
        voiceChannel = after.channel
        await voiceChannel.connect()
        await asyncio.sleep(0.5)
        voice: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=after.channel.guild)
        myAudio = FFmpegPCMAudio(f'{songDirectory}\\themeSong.mp3')
        myAdjustedAudio = PCMVolumeTransformer(myAudio)
        myAdjustedAudio.volume = 0.1
        voice.play(myAdjustedAudio)
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
async def playTest(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='anime')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None:
        await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("audio-testing\\NFL.mp3"), volume=0.5))

# @client.command()
# async def play(ctx, url : str):
#     song_there = os.path.isfile("song.mp3")
#     try:
#         if song_there:
#             os.remove("song.mp3")
#     except PermissionError:
#         await ctx.send("Wait for current music to end")
#         return
#     voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='anime')
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     if voice is None:
#         await voiceChannel.connect()
#     voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])
#     for file in os.listdir("./"):
#         if file.endswith(".mp3"):
#             os.rename(file, "song.mp3")
#     voice.play(discord.FFmpegPCMAudio("song.mp3"))

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
    songDirectory = f'theme-songs\\{member}'
    print(songDirectory)
    print(url)
    hasThemeSongFolder = os.path.isdir(songDirectory)
    if hasThemeSongFolder:
        song_there = os.path.isfile(f'{songDirectory}\\themeSong.mp3')
        try:
            if song_there:
                os.remove(f'{songDirectory}\\themeSong.mp3')
        except PermissionError:
            await ctx.send("User has a folder, but no song file! Please contact dev.")
            return
    else:
        os.mkdir(f'{songDirectory}')
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        for file in os.listdir('./'):
            if file.endswith(".mp3"):
                os.rename(file, f'{songDirectory}\\themeSong.mp3')
    print("Theme Song successfully added!")
    await ctx.channel.purge(limit = 1)
    await ctx.send("Theme Song Added!")

client.run(os.getenv('GUILD_TOKEN'))