# bot.py
import os, discord
from dotenv import load_dotenv

# Command stuff from the discord library
from discord.ext import commands

# Load data from a .env file into memory instead of storing it in the bot file itself
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Determines what key character the bot uses to detect commands
bot = commands.Bot(command_prefix='!', description='A Dungeons & Dragons Character Sheet Discord Interface.')

# cog locations (folder.python file name)
initial_extensions = ['cogs.character',
                      'cogs.cards',
                      'cogs.maps',
                      'cogs.admin']

# load cogs
if __name__ == "__main__":
    for extension in initial_extensions:
        bot.load_extension(extension)

# needs to be moved to a dedicated cog but is fine here for now.
@bot.command(name='echo', help='Echos the passed argument.')
async def echo(ctx, argument):
    await ctx.send(argument)

# Logon info
@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Dungeons & Dragons"))
    print(f'Successfully logged in!')

# gogogo
bot.run(TOKEN)