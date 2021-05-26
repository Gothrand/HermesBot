import discord, os, glob
from discord.ext import commands
from include import DOMT_DESCRIPTIONS
from random import randint


class CardsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='tarot')
    async def tarot(self, ctx):
        tarotCardPath = pullTarot()
        # tarotCardName = tarotCardPath.rsplit('-')
        file = discord.File(tarotCardPath)
        await ctx.send("You have pulled: ", file=file)

    @commands.command(name='domt')
    async def deck_of_many_things(self, ctx, amount):
        for i in range(int(amount)):
            cardPath = pullDOMT()
            cardName = cardPath.rsplit('.')[0]
            cardName = cardName.rsplit('/', 1)[1]
            print(cardName)
            file = discord.File(cardPath)
            await ctx.send(f"You have pulled: {cardName}. {DOMT_DESCRIPTIONS[cardName]}", file=file)

def setup(bot):
    bot.add_cog(CardsCog(bot))

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

    domtIndex = randint(0, len(gifs))
    domtCard = gifs[domtIndex]
    print(domtCard)
    return domtCard