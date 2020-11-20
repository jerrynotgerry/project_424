# bot.py
import os
import random
import logging
import discord
from dotenv import load_dotenv

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
    else:
        await ctx.author.voice.channel.connect()

@bot.command(name='play', help='Plays an audio file')
async def play(ctx, audio_file, pitchFactor=1.0, speedFactor=1.0):
    os.system("process.py {} {} {}".format(audio_file,pitchFactor,speedFactor))
    guild = ctx.guild
    existing_client = discord.utils.get(bot.voice_clients, guild=guild)
    if not existing_client:
        existing_client = connect(ctx)
    audio_source = discord.FFmpegOpusAudio("out.mp3")
    await existing_client.play(audio_source)
    
bot.run(TOKEN)
