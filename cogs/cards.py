import discord, os, glob
from discord.ext import commands
from include import DOMT_DESCRIPTIONS
from random import randint

"""
This cog is used for card pulling e.g. from the deck of many things or for pulling tarot cards.
Main purpose is just a fun thing to do.  Might rename this later to something more generic in regards to random gacha stuff lol.
"""
class Cards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # Change this command so that it sends the images in one message (try to)
    @commands.command(name='tarot', help='Pull a major arcana tarot card.')
    async def tarot(self, ctx, amount=1):
        for i in range(amount):
            tarotCardPath = pullCard("tarot")
            file = discord.File(tarotCardPath)
            await ctx.send("You have pulled: ", file=file)

    @commands.command(name='domt', help='Pull a card from the Deck of Many Things.  Must indicate how many cards you would like to draw.')
    async def deck_of_many_things(self, ctx, amount=1):
        for i in range(amount):
            cardPath = pullCard("domt")
            cardName = cardPath.rsplit('.')[0].rsplit('/', 1)[1]
            file = discord.File(cardPath)
            await ctx.send(f"You have pulled: {cardName}. {DOMT_DESCRIPTIONS[cardName]}", file=file)

    @deck_of_many_things.error
    async def domt_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!domt {number of cards to pull}``')

def setup(bot):
    bot.add_cog(Cards(bot))

tarotPath = os.getcwd().replace('\\', '/') + "/resources/tarotGifs/"
domtPath = os.getcwd().replace('\\', '/') + "/resources/domtGifs/"
def pullCard(cardSet: str) -> str:
    if cardSet == "tarot":
        gifs = [gif.replace('\\', '/') for gif in glob.glob(tarotPath+"*")]
    else:
        gifs = [gif.replace('\\', '/') for gif in glob.glob(domtPath+"*")]
    
    return gifs[randint(0, len(gifs)-1)]


# def pullDOMT():
#     gifs = [gif.replace('\\', '/') for gif in glob.glob(domtPath+"*")]
#     domtCard = gifs[randint(0, len(gifs)-1)]
#     return domtCard