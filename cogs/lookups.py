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
        # Take the passed arguments and put them together to be used for API lookup
        name = ""
        for arg in args:
            # handles spells like Antipathy/Sympathy
            if '/' in arg:
                for part in arg.split('/'):
                    name += part.lower()+'-'
            elif "\'" in arg:
                splits = arg.split(' ')
                for split in splits:
                    split = split.strip('\'')
                    name += split.lower()+'-'
            elif ' ' in arg:
                splits = arg.split(' ')
                for split in splits:
                    name += split.lower()+'-'
            else:
                name += arg.lower()+'-'
        name = name[:-1]

        # Make the request, check if it 404ed or actually got something
        try:
            response = requests.get(API+f'spells/{name}')
            response.raise_for_status()
        # If 404 then try to get a list of spells that match at least part of what the user asked for
        except HTTPError as http_err:
            print(f'HTTP error ocurred: {http_err}')
            
            name_splits = args
            spells = []
            for split in name_splits:
                response = requests.get(API+f'spells/?name={split}')
                response_dict = json.loads(response.text)
                if response_dict['count'] == 0:
                    print(f"Nothing found for {split}")
                else:
                    for item in response_dict['results']:
                        if item not in spells:
                            spells.append(item["name"])
                        else:
                            continue
            
            if spells:
                await ctx.send(f"Did you mean any of these spells?  {spells}")
            else:
                await ctx.send(f"Couldn't find anything for {name}.")

        except Exception as err:
            print(f'Other error occurred: {err}')
            await ctx.send('An error occurred while attempting to grab that information.')
        else:
            print("Success!")
            spell = json.loads(response.text)
            await ctx.send(embed=embedSpell(ctx, spell))

    @commands.command(name='weapon', help='Look up a weapon')
    async def weapon(self, ctx, *args):
        name = ""
        for arg in args:
            if '/' in arg:
                for part in arg.split('/'):
                    name += part.lower()+'-'
            elif "\'" in arg:
                splits = arg.split(' ')
                for split in splits:
                    split = split.strip('\'')
                    name += split.lower()+'-'
            elif ' ' in arg:
                splits = arg.split(' ')
                for split in splits:
                    name += split.lower()+'-'
            else:
                name += arg.lower()+'-'
        name = name[:-1]

        try:
            response = requests.get(API+f'equipment/{name}')
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error ocurred: {http_err}')

            name_splits = args
            equipments = []
            for split in name_splits:
                response = requests.get(API+f'spells/?name={split}')
                response_dict = json.loads(response.text)
                if response_dict['count'] == 0:
                    print(f"Nothing found for {split}")
                else:
                    for item in response_dict['results']:
                        if item not in equipments:
                            equipments.append(item["name"])
                        else:
                            continue
            
            if equipments:
                await ctx.send(f"Did you mean any of these equipments?  {equipments}")
            else:
                await ctx.send(f"Couldn't find anything for {name}.")
        except Exception as err:
            print(f'Other error occurred: {err}')
            await ctx.send('An error occurred while attempting to grab that information.')
        else:
            print("Success!")
            equipment = json.loads(response.text)
            await ctx.send(embed=embedEquipment(ctx, equipment))

#TODO:  Finish this.  Needs to be able to differentiate between armor, weapons, and other items
def embedEquipment(ctx, equipment):
    author = equipment['category_range']+" "+equipment['equipment_category']['name']

    embedVar = discord.Embed(title=equipment['name'], color=0xd93636)
    embedVar.set_author(name=author, icon_url=ctx.author.avatar_url)
    embedVar.add_field(name="")
    return embedVar


    # @commands.command(name='feat', aliases=['feature'], help='Look up a feat')

def setup(bot):
    bot.add_cog(Lookups(bot))