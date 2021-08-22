import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument

from cogs.maps_helpers import *

currentMapPath = "resources/maps/current_map_grid.jpg"

class Maps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pfp', hidden=True, help='WIP command')
    async def pfp(self, ctx):
        await ctx.send(str(ctx.author.avatar_url))

    @commands.command(name='setmap', help='Set a battle map to use.')
    async def setmap(self, ctx, size):
        attachments = ctx.message.attachments
        await attachments[0].save("resources/maps/current_map.jpg")
        setMap("resources/maps/current_map.jpg", int(size))
        await ctx.send("Map successfully set.")

    @commands.command(name='map', help='Render the current battle map')
    async def showMap(self, ctx):
        await ctx.send("Rendering map...")
        path = render()
        file = discord.File(path, filename="current_map.jpg")
        try:
            await ctx.send(file=file)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name='position', aliases=['move'], help='Set your position on the battlemap.  Use the battle map to select a box and then type "!position {the box name}"')
    async def position(self, ctx, pos, character=None):
        if character is not None:
            if update(character, pos.upper()):
                file = discord.File(render(), filename="current_map.jpg")
                await ctx.send(f"Position updated for {character}.", file=file)
            else:
                await ctx.send("Position update failed.")
        else:
            if update(str(ctx.author), pos.upper()):
                file = discord.File(render(), filename="current_map.jpg")
                await ctx.send(f"Position updated for {str(ctx.author)}.", file=file)
            else:
                await ctx.send("Position update failed.")

    @commands.command(name='token', help='Upload a personal token to use on the battlefield.  You must upload the token like you would any other image, and type "!token" in the comment box.')
    async def token(self, ctx, name=None):
        attachments = ctx.message.attachments
        if attachments is None:
            await ctx.send("You need to upload an image alongside.  Upload an image and in the comment type ``!token``")
        elif name is not None:
            await attachments[0].save(f'resources/tokens/{name+".jpg"}')
            await ctx.send(f"Token saved as {name}!")
        else:
            await attachments[0].save(f"resources/tokens/{str(ctx.author)}.jpg")
            await ctx.send(f"Token saved for {str(ctx.author)}!")

    @commands.command(name='region', help='Get a region from the current map.')
    async def region(self, ctx, pos1, pos2):
        path = getRegion(pos1, pos2)
        file = discord.File(path, filename="region_map.jpg")
        try:
            await ctx.send(file=file)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @token.error
    async def token_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!token {image upload}``')

    @region.error
    async def region_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!region {position 1} {position 2}``')

def setup(bot):
    bot.add_cog(Maps(bot))

if __name__ == "__main__":
    # print(getPixelCoordinate(('B', 4), 300))
    print("Driver Code")