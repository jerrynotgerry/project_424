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

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='hello', help='Responds with hello world')
async def hello(ctx):
    await ctx.send('Hello World!')

@bot.command(name='connect', help='Connects to your currently occupied voice channel')
async def connect(ctx):
    if ctx.author.channel == None:
        await ctx.send('You are not in any voice channel.')
        return
    await ctx.author.channel.connect()

bot.run(TOKEN)