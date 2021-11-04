# bot.py
import os, discord
from discord.ext import commands

from dotenv import load_dotenv

class MyHelpCommand(commands.HelpCommand):
    async def command_callback(self, ctx, *, command=None):
        if command:
           await ctx.send(f"This the help page for the command {command} ")
        else:
            await ctx.send("This is the front page for the bots help command")

#TODO:  Convert entire structure of database for bot to postgreSQL from JSON since JSON is not ideal for
# database management.
# Load data from a .env file into memory instead of storing it in the bot file itself
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Determines what key character the bot uses to detect commands
bot = commands.Bot(command_prefix='!', description='A Dungeons & Dragons Discord Interface.')
bot.help_command = MyHelpCommand()

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

# cog locations (folder.python file name)
initial_extensions = ['cogs.character',
                      'cogs.cards',
                      'cogs.maps',
                      'cogs.admin',
                      'cogs.lookups']

def main():
    for extension in initial_extensions:
            bot.load_extension(extension)
# load cogs
if __name__ == "__main__":
    main()

# gogogo
bot.run(TOKEN)