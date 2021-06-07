'''
This file's purpose is to contain the classes used to represent a character with that character's stats and   
'''
from cogs.character_helpers import *

import discord
from discord.ext import commands

# Everything from embeds.py
from embeds import embedCharacter, embedAttributes, embedProfs, embedWeapons

#TODO: Attunements list function
#TODO: Smarter character sheet algorithms e.g. Read attribute scores and correct character sheet wherever necessary
#TODO: Refactor this code to put all the character not found errors in the error handling part of this code
#TODO: Add command !add_weapon to add a weapon.
class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='characters', aliases=['chars'], help='\nDisplays all saved character sheets for a given discord user.')
    async def characters(self, ctx):
        """Displays a member's characters if they are available."""
        characters = getCharacters(str(ctx.author))
        if characters == []:
            await ctx.send("No characters found.  Use ``!create {Character Name}`` to create a character.")
        else:
            print(characters)
            for character in characters:
                await ctx.send(embed=embedCharacter(str(ctx.author), character))

    @commands.command(name='character', aliases=['char'], help='\nDisplays a character sheet for the given character name.')
    async def character(self, ctx, character_name):
        if findCharacter(str(ctx.author), character_name) == None:
            await ctx.send(f"No character found with matching name {character_name}.  Create one using !create or import a character sheet using !import")
        else:
            await ctx.send(embed=embedCharacter(str(ctx.author), character_name))

    @commands.command(name='attributes', aliases=['attrs'], help='Display attributes for the given character.')
    async def attributes(self, ctx, character_name):
        if findCharacter(str(ctx.author), character_name) == None:
            await ctx.send(f"No character found with matching name {character_name}.")
        else:
            await ctx.send(embed=embedAttributes(str(ctx.author), character_name))
    
    @commands.command(name='proficiencies', aliases=['profs'], help='Display proficiencies for a given character.')
    async def profs(self, ctx, character_name):
        if findCharacter(str(ctx.author), character_name) == None:
            await ctx.send(f"No character found with matching name {character_name}.")
        else:
            await ctx.send(embed=embedProfs(str(ctx.author), character_name))

    @commands.command(name='weapons', aliase=['wpns'], help='Display all the weapons for a given character.')
    async def weapons(self, ctx, character_name):
        if findCharacter(str(ctx.author), character_name) == None:
            await ctx.send(f"No character found with matching name {character_name}.")
        else:
            await ctx.send(embed=embedWeapons(str(ctx.author), character_name))

    #TODO: Check to see if the user already has a character under that name
    @commands.command(name='import', help='Import a character from a suitable dungeons and dragons PDF')
    async def importCharacter(self, ctx, character_name):
        attachments = ctx.message.attachments

        # Need to experiment with using 'read' instead of 'save
        await attachments[0].save("characterSheet.pdf")
        importFromPDF(str(ctx.author), character_name)
        await ctx.send(f"Saved character sheet for character {character_name}")

    # Will need to do input handling later but for now is good
    @commands.command(name='update', help='\nUpdates a character\'s attribute with a specific value.')
    async def update(self, ctx, character_name, character_attribute, value):
        if updateChar(str(ctx.author), character_name, character_attribute, value):
            await ctx.send(f"Updated character {character_name} attribute {character_attribute} with {value}")
        else:
            await ctx.send(f"Failed to update: Failed to find matching character with name {character_name}")

    @commands.command(name='image', help='Set an image for the given character.  Argument must be a URL.')
    async def image(self, ctx, character_name, image_url):
        if setImage(str(ctx.author), character_name, image_url):
            await ctx.send(f"Set image for character {character_name} with image {image_url}")
        else:
            await ctx.send(f"Failed to set image, no character found for {character_name}")

    @commands.command(name='create', help='\nCreates a character sheet with the given character name.  Usage: ``!create {Character Name}``')
    async def create(self, ctx, character_name):
        if character_name is not None:
            addCharacter(str(ctx.author), character_name)
            await ctx.send(f"Created character {character_name}.")
        else:
            await ctx.send(f"Not enough arguments.  Command usage: !create \"Character Name\"")

    @commands.command(name='remove', aliases=['rm'], help='\nRemoves a character sheet with the given character name.  Usage: ``!remove {Character Name}``')
    async def remove(self, ctx, character_name):
        if character_name != "":
            if removeCharacter(str(ctx.author), character_name):
                await ctx.send(f"Removed character {character_name}.")
            else:
                await ctx.send(f"Failed to remove:  Failed to find matching character with name {character_name}")
        else:
            await ctx.send(f"Not enough arguments.  Command usage: !remove \"Character Name\"")

    @commands.command(name='modifiables', aliases=['mods'], help='Display all modifiable attributes that one can change for a character.')
    async def modifiables(self, ctx):
        modAttributes = listAttributes()
        message = "Here are the modifiable attributes for a given character sheet: \r"
        for key in modAttributes:
            message += key + "\r"

        await ctx.send(message)

    @characters.error
    async def characters_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!characters``')

    @character.error
    async def character_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!character {Character Name}``')

    @update.error
    async def update_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!update {Character Name} {Attribute} {Value}``')

    @create.error
    async def create_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!create {Character Name}``')

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!remove {Character Name}``')

def setup(bot):
    bot.add_cog(Character(bot))

# Driver code
if __name__ ==  "__main__":
    print("Driver code execute")