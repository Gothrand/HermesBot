# bot.py
import os

import discord
from dotenv import load_dotenv

# 1
from discord.ext import commands

from character import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='create_character', help='Create a dungeons and dragons character')
async def create_character(ctx):
    response = "Creating character..."
    await ctx.send(response)

# needs to parse through character info and display it all
@bot.command(name='charTest')
async def charTest(ctx):
    embedVar = discord.Embed(title=ctx.author, description="BITCH", color=0x00ff00)
    embedVar.add_field(name="Character Name", value=getInfo(str(ctx.author), "charName"), inline=False)
    embedVar.add_field(name="Class", value=getInfo(str(ctx.author), "charClass"), inline=True)
    embedVar.add_field(name="Subclass", value=getInfo(str(ctx.author), "subClass"), inline=True)
    await ctx.send(embed=embedVar)

# Will need to do input handling later but for now is good
@bot.command(name='update')
async def update(ctx, arg1, arg2):
    print("sucks", arg1, arg2)
    updateChar(str(ctx.author), arg1, arg2)
    await ctx.send(f"Updated {arg1} with {arg2}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


if __name__ == "__main__":
    print(getInfo("Gothrand#9375", "charName"))
    bot.run(TOKEN)