import discord
from discord.ext import commands

import requests
from requests.exceptions import HTTPError

import json

from embeds import embedSpell

# The API this cog uses
API = 'https://www.dnd5eapi.co/api/'

class Lookups(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='spell', help='Look up a spell\'s description')
    async def spell(self, ctx, *args):
        name = cleanInputSpells(args)

        # Make the request, check if it 404ed or actually got something
        try:
            response = requests.get(API+f'spells/{name}')
            response.raise_for_status()
        # If 404 then try to get a list of spells that match at least part of what the user asked for
        except HTTPError as http_err:
            print(f'HTTP error ocurred: {http_err}')
            
            spells = queryCategory("spells", args)
            
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

    #TODO:  Fix this so that input such as 'Hand crossbow' is accepted instead of 'crossbow hand'
    @commands.command(name='weapon', help='Look up a weapon')
    async def weapon(self, ctx, *args):
        name = cleanInputWeapon(args)

        try:
            response = requests.get(API+f'equipment/{name}')
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error ocurred: {http_err}')

            equipments = queryCategory("equipment", args)
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
    
    # @commands.command(name='equipment', aliases=['equip'], help='Look up a class')
    # async def archetype(self, ctx, *args):
    #     pass


#TODO:  Finish this.  Needs to be able to differentiate between armor, weapons, and other items
def embedEquipment(ctx, equipment) -> discord.Embed:
    match equipment['equipment_category']['name']:
        case "Adventuring Gear":
            author = equipment['equipment_category']['name']
        case "Weapon":
            author = equipment['category_range']+" "+equipment['equipment_category']['name']
        case "Armor":
            author = equipment['armor_category']+" "+equipment['equipment_category']['name']
        case _:
            raise ValueError

    embedVar = discord.Embed(title=equipment['name'], color=0xd93636)
    embedVar.set_author(name=author, icon_url=ctx.author.avatar_url)
    try:
        embedVar.add_field(name="Damage", value=equipment['damage']['damage_dice'] + ' ' + equipment['damage']['damage_type']['name'])
    except KeyError:
        embedVar.add_field(name="Damage", value="None")

    if equipment['properties']:
        propertyList = ""
        for prop in equipment['properties']:
            match prop['name']:
                case 'Thrown':
                    propertyList += prop['name'] + f" ({equipment['throw_range']['normal']}/{equipment['throw_range']['long']})"+', '
                case 'Versatile':
                    propertyList += prop['name'] + f" ({equipment['two_handed_damage']['damage_dice']})"+', '
                case _:
                    propertyList += prop['name']+', '

        propertyList = propertyList[:-2]
        print(propertyList)
        
        embedVar.add_field(name="Properties", value=propertyList)
    else:
        embedVar.add_field(name="Properties", value="None")

    embedVar.add_field(name='Cost', value=str(equipment['cost']['quantity']) + ' '+ str(equipment['cost']['unit']))
    # embedVar.add_field(name='Type', value=)

    return embedVar

# Required function for cog to work.
def setup(bot):
    bot.add_cog(Lookups(bot))


# def embedClass(ctx, arch) -> discord.Embed:
#     embedVar = discord.Embed(title=arch['name'])

#     return embedVar


'''
This function cleans up input for the weapon lookup command.
This is needed due to the nature of certain items contained within the database
for weapons such as hand crossbows being listed as "crossbow-hand".
'''
# TODO:  Add functionality to deal with "example" and 'example' type inputs.
def cleanInputWeapon(args) -> str:
    clean_args = []
    for arg in args:
        arg = arg.lower().replace(',', "").replace('\'', "")

        if ' ' in arg:
            for split in arg.split(' '):
                clean_args.append(split)
        else:
            clean_args.append(arg)
    
    clean_args.sort() # Needed for cases such as "Crossbow, Hand" and such.  Weapon names are always sorted alphanumerically.

    return "-".join(clean_args)

def cleanInputSpells(args) -> str:
    clean_args = []
    for arg in args:
        arg = arg.lower().replace("\'", "")

        if '/' in arg:
            for split in arg.split('/'):
                clean_args.append(split)
        elif ' ' in arg:
            for split in arg.split(' '):
                clean_args.append(split)
        else:
            clean_args.append(arg)

    return "-".join(clean_args)


# This function takes a category string and a list of arguments and
# queries dnd 5e api for possible corrections based on the given args.
def queryCategory(category: str, args):
    result = []
    for split in args:
        response = requests.get(API+f'{category}/?name={split}')
        response_dict = json.loads(response.text)

        if response_dict['count'] == 0:
            print(f"Nothing found for {split}")
        else:
            for item in response_dict['results']:
                if item not in result:
                    result.append(item["name"])
                else:
                    continue

    return result