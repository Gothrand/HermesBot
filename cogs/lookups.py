import discord
from discord.ext import commands

import requests
from requests.exceptions import HTTPError

import json

from embeds import embedSpell

API = 'https://www.dnd5eapi.co/api/'

class Lookups(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='spell', help='Look up a spell\'s description')
    async def spell(self, ctx, *args):
        name = ""
        for arg in args:
            name += arg.lower()+'-'
        name = name[:-1]

        try:
            response = requests.get(API+f'spells/{name}')
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'HTTP error ocurred: {http_err}')
            
            name_splits = name.split('-')
            spells = []
            for split in name_splits:
                response = requests.get(API+f'spells/?name={split}')
                response_dict = json.loads(response.text)
                if response_dict['count'] == 0:
                    print(f"Nothing found for {split}")
                else:
                    for item in response_dict['results']:
                        spells.append(item["name"])
            
            await ctx.send(f"Did you mean any of these spells?  {spells}")

        except Exception as err:
            print(f'Other error occurred: {err}')
            await ctx.send('An error occurred while attempting to grab that information.')
        else:
            print("Success!")
            spell = json.loads(response.text)
            await ctx.send(embed=embedSpell(ctx, spell))

    # @commands.command(name='feat', aliases=['feature'], help='Look up a feat')

def setup(bot):
    bot.add_cog(Lookups(bot))