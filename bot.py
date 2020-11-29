# bot.py
import os
import random
import logging
import discord
from dotenv import load_dotenv
from process import *
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='-')

discord.opus.load_opus(".\opus.dll")
if not discord.opus.is_loaded():
    print("Opus not loaded")
    exit()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='hello', help='Responds with hello world')
async def hello(ctx):
    await ctx.send('Hello World!')

@bot.command(name='connect', help='Connects to your currently occupied voice channel')
async def connect(ctx):
    if ctx.author.voice == None:
        await ctx.send('You are not in any voice channel.')
        return None
    client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if client:
        await client.move_to(ctx.author.voice.channel)
        return client
    else:
        return await ctx.author.voice.channel.connect()

@bot.command(name='play', help='Plays an audio file')
async def play(ctx, input_obj, pitchFactor=1.0, speedFactor=1.0):
    # os.system("process.py {} {} {}".format(audio_file,pitchFactor,speedFactor))
    guild = ctx.guild
    if not bot.voice_clients:
        existing_client = await connect(ctx)
    else:
        existing_client = discord.utils.get(bot.voice_clients, guild=guild)
        if not existing_client:
            existing_client = await connect(ctx)

    if not existing_client:
        return None
    # generate ffmpeg options string
    pitchProcessString = GetPitchString(pitchFactor)
    speedProcessString = GetTempoString(speedFactor)
    audio_source = discord.FFmpegOpusAudio(input_obj, options="-af {}{}".format(pitchProcessString,speedProcessString))
    existing_client.play(audio_source)

@bot.command(name='playYoutube', help='Plays an audio from YouTube')
async def play(ctx, youtubeLink, pitchFactor=1.0, speedFactor=1.0):
    guild = ctx.guild
    if not bot.voice_clients:
        existing_client = await connect(ctx)
    else:
        existing_client = discord.utils.get(bot.voice_clients, guild=guild)
        if not existing_client:
            existing_client = await connect(ctx)

    if not existing_client:
        return None
    # Download youtube audio
    os.system("youtube-dl --extract-audio --audio-format mp3 --output ""youtubeIn.%(ext)s"" {}".format(youtubeLink))
    os.system("process.py {} {} {}".format("youtubeIn.mp3",pitchFactor,speedFactor))
    pitchProcessString = GetPitchString(pitchFactor)
    speedProcessString = GetTempoString(speedFactor)
    audio_source = discord.FFmpegOpusAudio("youtubeIn.mp3", options="-af {}{}".format(pitchProcessString,speedProcessString))
    await existing_client.play(audio_source)
    
@bot.command(name='disconnect', help='Disconnects from voice')
async def disconnect(ctx):
    target = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if target:
        await target.disconnect()

@bot.command(name='pause', help='Pauses current playback')
async def pause(ctx):
    target = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if target and target.is_playing():
        target.pause()

@bot.command(name='resume', help='Resumes playback if paused')
async def pause(ctx):
    target = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if target and target.is_paused():
        target.resume()

@bot.command(name='stop', help='Stops playback entirely')
async def stop(ctx):
    target = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    target.stop()
    
bot.run(TOKEN)
