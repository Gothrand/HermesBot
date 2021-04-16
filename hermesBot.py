# bot.py
import os

import discord
import random
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

"""----- Bot Commands -----"""

# needs to parse through character info and display it all
@bot.command(name='character')
async def character(ctx, arg1):
    embedVar = discord.Embed(title=getInfo(str(ctx.author), str(arg1), "charName"), color=0x3399ff)
    embedVar.add_field(name="Subclass", value=getInfo(str(ctx.author), str(arg1), "subClass"), inline=True)
    embedVar.add_field(name="Class", value=getInfo(str(ctx.author), str(arg1), "charClass"), inline=True)
    embedVar.add_field(name="Level", value=getInfo(str(ctx.author), str(arg1), "level"), inline=True)
    embedVar.add_field(name="Race", value=getInfo(str(ctx.author), str(arg1), "race"), inline=True)
    embedVar.add_field(name="Background", value=getInfo(str(ctx.author), str(arg1), "background"), inline=True)
    embedVar.add_field(name="Alignment", value=getInfo(str(ctx.author), str(arg1), "alignment"), inline=True)
    await ctx.send(embed=embedVar)

# Will need to do input handling later but for now is good
@bot.command(name='update')
async def update(ctx, arg1, arg2, arg3):
    if updateChar(str(ctx.author), arg1, arg2, arg3):
        print("POOP")
        await ctx.send(f"Updated character {arg1} attribute {arg2} with {arg3}")
    else:
        await ctx.send(f"Failed to update: Failed to find matching character with name {arg1}")

@bot.command(name='create')
async def create(ctx, arg1):
    if arg1 is not None:
        addCharacter(str(ctx.author), arg1)
        await ctx.send(f"Created character {arg1}.")
    else:
        await ctx.send(f"Not enough arguments.  Command usage: !create \"Character Name\"")

@bot.command(name='remove')
async def remove(ctx, arg1):
    if str(arg1) != "":
        if removeCharacter(str(ctx.author), arg1):
            await ctx.send(f"Removed character {arg1}.")
        else:
            await ctx.send(f"Failed to remove:  Failed to find matching character with name {arg1}")
    else:
        await ctx.send(f"Not enough arguments.  Command usage: !remove \"Character Name\"")

@bot.command(name='echo')
async def echo(ctx, arg1):
    await ctx.send(arg1)


"""----- Command Error Handling -----"""
@character.error
async def character_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!character {Character Name}``')

@update.error
async def update_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!update {Character Name} {Character Attribute} {Value}``')

@create.error
async def create_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!create {Character Name}``')

@remove.error
async def remove_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!remove {Character Name}``')


"""----- Driver Code -----"""
if __name__ == "__main__":
    bot.run(TOKEN)