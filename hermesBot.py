# bot.py
import os

import discord
import random
from dotenv import load_dotenv

# Command stuff from the discord library
from discord.ext import commands

# Everything from character.py
from character import *

# Everything from embeds.py
from embeds import embedCharacter, embedAttributes, embedProfs, embedWeapons

# Load data from a .env file into memory instead of storing it in the bot file itself
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Determines what key character the bot uses to detect commands
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return

#     await message.channel.send(message.content)

"""----- Bot Commands -----"""
#TODO: Add command to display all the different modifiable attributes used for the '!update' command

#TODO: Add pre/post conditons for each function
#TODO: Refactor this code to put all the character not found errors in the error handling part of this code
#TODO: Add command !add_weapon to add a weapon.
'''
Purpose: Creates and posts embeds displaying information for each character for the user
Pre-condition: User must have at least one character saved in the database to work.  If no character, then no character will be posted
Post-condition:  An embed each of that user's character(s) will be posted to the channel this command is called from
'''
@bot.command(name='characters', help='\nDisplays all saved character sheets for a given discord user.')
async def characters(ctx):
    characters = getCharacters(str(ctx.author))
    if characters == []:
        await ctx.send("No characters found.  Use ``!create {Character Name}`` to create a character.")
    else:
        print(characters)
        for character in characters:
            await ctx.send(embed=embedCharacter(str(ctx.author), character))

'''
Purpose:  Creates and posts an embed displaying the information for a particular for the user
Pre-condition:  The discord user must have a character saved in the database.  If no character is present, they are directed to create one using
                !create or import one using !import
Post-condition:  Hermes will post an embed of that character's specific information
'''
@bot.command(name='character', help='\nDisplays a character sheet for the given character name.  Usage: ``!character {Character Name}``')
async def character(ctx, character_name):
    if findCharacter(str(ctx.author), character_name) == None:
        await ctx.send(f"No character found with matching name {character_name}.  Create one using !create or import a character sheet using !import")
    else:
        await ctx.send(embed=embedCharacter(str(ctx.author), character_name))

@bot.command(name='attributes', help='Display attributes for the given character.  Usage:  ``!attributes {Character Name}``')
async def attributes(ctx, character_name):
    if findCharacter(str(ctx.author), character_name) == None:
        await ctx.send(f"No character found with matching name {character_name}.")
    else:
        await ctx.send(embed=embedAttributes(str(ctx.author), character_name))

@bot.command(name='profs', help='Display proficiencies for a given character.')
async def profs(ctx, character_name):
    if findCharacter(str(ctx.author), character_name) == None:
        await ctx.send(f"No character found with matching name {character_name}.")
    else:
        await ctx.send(embed=embedProfs(str(ctx.author), character_name))

@bot.command(name='weapons', help='Display all the weapons for a given character.')
async def weapons(ctx, character_name):
    if findCharacter(str(ctx.author), character_name) == None:
        await ctx.send(f"No character found with matching name {character_name}.")
    else:
        await ctx.send(embed=embedWeapons(str(ctx.author), character_name))
    

"""----- Character Sheet Handling ---"""
#TODO: Check to see if the user already has a character under that name
@bot.command(name='import', help='Import a character from a suitable dungeons and dragons PDF')
async def importCharacter(ctx, character_name):
    # message is of the discord object 'Message' which contains the attribute 'attachment' which will check for attachments from a message
    message = ctx.message
    attachments = message.attachments

    # Need to experiment with using 'read' instead of 'save
    await attachments[0].save("characterSheet.pdf")
    importFromPDF(str(ctx.author), character_name)
    await ctx.send(f"Saved character sheet for character {character_name}")

# Will need to do input handling later but for now is good
@bot.command(name='update', help='\nUpdates a character\'s attribute with a specific value.  Usage: ``!update {Character Name} {Attribute} {Value}``')
async def update(ctx, character_name, character_attribute, value):
    if updateChar(str(ctx.author), character_name, character_attribute, value):
        await ctx.send(f"Updated character {character_name} attribute {character_attribute} with {value}")
    else:
        await ctx.send(f"Failed to update: Failed to find matching character with name {character_name}")

@bot.command(name='image', help='Set an image for the given character.  Argument must be a URL.')
async def image(ctx, character_name, image_url):
    if setImage(str(ctx.author), character_name, image_url):
        await ctx.send(f"Set image for character {character_name} with image {image_url}")
    else:
        await ctx.send(f"Failed to set image, no character found for {character_name}")

@bot.command(name='create', help='\nCreates a character sheet with the given character name.  Usage: ``!create {Character Name}``')
async def create(ctx, character_name):
    if character_name is not None:
        addCharacter(str(ctx.author), character_name)
        await ctx.send(f"Created character {character_name}.")
    else:
        await ctx.send(f"Not enough arguments.  Command usage: !create \"Character Name\"")

@bot.command(name='remove', help='\nRemoves a character sheet with the given character name.  Usage: ``!remove {Character Name}``')
async def remove(ctx, character_name):
    if character_name != "":
        if removeCharacter(str(ctx.author), character_name):
            await ctx.send(f"Removed character {character_name}.")
        else:
            await ctx.send(f"Failed to remove:  Failed to find matching character with name {character_name}")
    else:
        await ctx.send(f"Not enough arguments.  Command usage: !remove \"Character Name\"")


@bot.command(name='modifiables', help='Display all modifiable attributes that one can change for a character.')
async def modifiables(ctx):
    modAttributes = listAttributes()
    message = "Here are the modifiable attributes for a given character sheet: \r"
    for key in modAttributes:
        message += key + "\r"

    await ctx.send(message)

@bot.command(name='echo', help='Echos the passed argument.')
async def echo(ctx, argument):
    await ctx.send(argument)



"""----- Command Error Handling -----"""
#TODO: Add more complex error handling for each command, more cases and such if applicable
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

# Maybe more stuff to add in the driver code later
"""----- Driver Code -----"""
if __name__ == "__main__":
    bot.run(TOKEN)