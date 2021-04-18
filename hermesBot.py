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

@bot.command(name='characters', help='\nDisplays all saved character sheets for a given discord user.')
async def characters(ctx):
    characters = getCharacters(str(ctx.author))
    if characters == []:
        await ctx.send("No characters found.  Use ``!create {Character Name}`` to create a character.")
    else:
        for character in characters:
            embedVar = discord.Embed(title=getInfo(str(ctx.author), character, "charName"), color=0x3399ff)
            embedVar.add_field(name="Subclass", value=getInfo(str(ctx.author), character, "subClass"), inline=True)
            embedVar.add_field(name="Class", value=getInfo(str(ctx.author), character, "charClass"), inline=True)
            embedVar.add_field(name="Level", value=getInfo(str(ctx.author), character, "level"), inline=True)
            embedVar.add_field(name="Race", value=getInfo(str(ctx.author), character, "race"), inline=True)
            embedVar.add_field(name="Background", value=getInfo(str(ctx.author), character, "background"), inline=True)
            embedVar.add_field(name="Alignment", value=getInfo(str(ctx.author), character, "alignment"), inline=True)

            embedVar.add_field(name="Str", value=getInfo(str(ctx.author), character, "attrStr"), inline=True)
            embedVar.add_field(name="Dex", value=getInfo(str(ctx.author), character, "attrDex"), inline=True)
            embedVar.add_field(name="Con", value=getInfo(str(ctx.author), character, "attrCon"), inline=True)
            embedVar.add_field(name="Int", value=getInfo(str(ctx.author), character, "attrInt"), inline=True)
            embedVar.add_field(name="Wis", value=getInfo(str(ctx.author), character, "attrWis"), inline=True)
            embedVar.add_field(name="Char", value=getInfo(str(ctx.author), character, "attrChar"), inline=True)
            await ctx.send(embed=embedVar)

# needs to parse through character info and display it all
@bot.command(name='character', help='\nDisplays a character sheet for the given character name.  Usage: ``!character {Character Name}``')
async def character(ctx, arg1):
    if findCharacter(str(ctx.author), str(arg1)) == None:
        await ctx.send(f"No character found with matching name {arg1}.")
    else:
        embedVar = discord.Embed(title=getInfo(str(ctx.author), str(arg1), "charName"), color=0x3399ff)
        embedVar.add_field(name="Subclass", value=getInfo(str(ctx.author), str(arg1), "subClass"), inline=True)
        embedVar.add_field(name="Class", value=getInfo(str(ctx.author), str(arg1), "charClass"), inline=True)
        embedVar.add_field(name="Level", value=getInfo(str(ctx.author), str(arg1), "level"), inline=True)
        embedVar.add_field(name="Race", value=getInfo(str(ctx.author), str(arg1), "race"), inline=True)
        embedVar.add_field(name="Background", value=getInfo(str(ctx.author), str(arg1), "background"), inline=True)
        embedVar.add_field(name="Alignment", value=getInfo(str(ctx.author), str(arg1), "alignment"), inline=True)

        embedVar.add_field(name="Str", value=getInfo(str(ctx.author), str(arg1), "attrStr"), inline=True)
        embedVar.add_field(name="Dex", value=getInfo(str(ctx.author), str(arg1), "attrDex"), inline=True)
        embedVar.add_field(name="Con", value=getInfo(str(ctx.author), str(arg1), "attrCon"), inline=True)
        embedVar.add_field(name="Int", value=getInfo(str(ctx.author), str(arg1), "attrInt"), inline=True)
        embedVar.add_field(name="Wis", value=getInfo(str(ctx.author), str(arg1), "attrWis"), inline=True)
        embedVar.add_field(name="Char", value=getInfo(str(ctx.author), str(arg1), "attrChar"), inline=True)
        await ctx.send(embed=embedVar)

# Will need to do input handling later but for now is good
@bot.command(name='update', help='\nUpdates a character\'s attribute with a specific value.  Usage: ``!update {Character Name} {Attribute} {Value}``')
async def update(ctx, arg1, arg2, arg3):
    if updateChar(str(ctx.author), arg1, arg2, arg3):
        print("POOP")
        await ctx.send(f"Updated character {arg1} attribute {arg2} with {arg3}")
    else:
        await ctx.send(f"Failed to update: Failed to find matching character with name {arg1}")

@bot.command(name='create', help='\nCreates a character sheet with the given character name.  Usage: ``!create {Character Name}``')
async def create(ctx, arg1):
    if arg1 is not None:
        addCharacter(str(ctx.author), arg1)
        await ctx.send(f"Created character {arg1}.")
    else:
        await ctx.send(f"Not enough arguments.  Command usage: !create \"Character Name\"")

@bot.command(name='remove', help='\nRemoves a character sheet with the given character name.  Usage: ``!remove {Character Name}``')
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
#TODO:
@characters.error
async def characters_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!characters``')

@character.error
async def character_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!character {Character Name}``')

@update.error
async def update_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!update {Character Name} {Attribute} {Value}``')

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