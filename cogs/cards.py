import discord, os, glob
from discord.ext import commands
from include import DOMT_DESCRIPTIONS
from random import randint

# Cog used for random card pulling from Tarot and Deck of Many Things decks.
class Cards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='tarot', help='Pull a major arcana tarot card.')
    async def tarot(self, ctx):
        tarotCardPath = pullTarot()
        # tarotCardName = tarotCardPath.rsplit('-')
        file = discord.File(tarotCardPath)
        await ctx.send("You have pulled: ", file=file)

    @commands.command(name='domt', help='Pull a card from the Deck of Many Things.  Must indicate how many cards you would like to draw.')
    async def deck_of_many_things(self, ctx, amount):
        for i in range(int(amount)):
            cardPath = pullDOMT()
            cardName = cardPath.rsplit('.')[0]
            cardName = cardName.rsplit('/', 1)[1]
            print(cardName)
            file = discord.File(cardPath)
            await ctx.send(f"You have pulled: {cardName}. {DOMT_DESCRIPTIONS[cardName]}", file=file)

    @commands.command(name='cast', help='Cast a spell.  COMMAND WORK IN PROGRESS')
    async def cast(self, ctx, spell_name):
        await ctx.send(f"Casting spell: {spell_name}")

    @deck_of_many_things.error
    async def domt_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Invalid command usage, not enough arguments.  Usage: ``!domt {number of cards to pull}``')

def setup(bot):
    bot.add_cog(Cards(bot))

tarotPath = os.getcwd().replace('\\', '/') + "/resources/tarotGifs/"
def pullTarot():
    gifs = []
    for gif in glob.glob(tarotPath+"*"):
        gifs.append(gif.replace('\\','/'))
    
    tarotIndex = randint(0, len(gifs)-1)
    tarotCard = gifs[tarotIndex]
    return tarotCard

domtPath = os.getcwd().replace('\\', '/') + "/resources/domtGifs/"
def pullDOMT():
    gifs = []
    for gif in glob.glob(domtPath+"*"):
        gifs.append(gif.replace('\\', '/'))

    domtIndex = randint(0, len(gifs)-1)
    domtCard = gifs[domtIndex]
    print(domtCard)
    return domtCard