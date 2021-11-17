import discord
from discord.embeds import Embed
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

    @commands.command(name='gear', aliases=['equip', 'equipment', 'weapon', 'armor'], help='Look up a weapon')
    async def equipment(self, ctx, *args):
        name = cleanInputEquipment(args)

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

# Required function for cog to work.
def setup(bot):
    bot.add_cog(Lookups(bot))

"""------  Begin helper methods ------"""

#TODO:  Finish this.  Needs to be able to differentiate between armor, weapons, and other items
def embedEquipment(ctx, equipment) -> discord.Embed:
    match equipment['equipment_category']['name']:
        case "Adventuring Gear":
            embedVar = embedGearLookup(ctx, equipment)
        case "Weapon":
            embedVar = embedWeaponLookup(ctx, equipment)
        case "Armor":
            embedVar = embedArmorLookup(ctx, equipment)
        case _:
            raise ValueError

    return embedVar

def embedGearLookup(ctx, equipment: dict) -> discord.Embed:
    description = [sentence+'\n' for sentence in equipment['desc']]

    embed = discord.Embed(title=equipment['name'], description="".join(description), color=0x3dd1eb)
    embed.set_author(name="Adevnturing Gear", icon_url=ctx.author.avatar_url)

    cost = [str(value) for value in equipment['cost'].values()]
    embed.add_field(name="Cost", value="".join(cost))

    return embed

def embedWeaponLookup(ctx, equipment: dict) -> discord.Embed:
    try:
        description = [sentence+'\n' for sentence in equipment['special']]
        embed = discord.Embed(title=equipment['name'], description="".join(description), color=0xd93636)
    except KeyError:
        embed = discord.Embed(title=equipment['name'], color=0xd93636)
        print("No special description found.  Moving on.")
    
    embed.set_author(name=equipment['category_range']+" "+equipment['equipment_category']['name'], icon_url=ctx.author.avatar_url)

    try:
        embed.add_field(name="Damage", value=equipment['damage']['damage_dice'] + ' ' + equipment['damage']['damage_type']['name'])
    except KeyError:
        embed.add_field(name="Damage", value="None")

    if equipment['properties']:
        propertyList = []
        for prop in equipment['properties']:
            match prop['name']:
                case 'Thrown':
                    propertyList.append(prop['name'] + f" ({equipment['throw_range']['normal']}/{equipment['throw_range']['long']})")
                case 'Versatile':
                    propertyList.append(prop['name'] + f" ({equipment['two_handed_damage']['damage_dice']})")
                case _:
                    propertyList.append(prop['name'])
        
        embed.add_field(name="Properties", value=", ".join(propertyList))
    else:
        embed.add_field(name="Properties", value="None")

    embed.add_field(name='Cost', value=str(equipment['cost']['quantity']) + ' '+ str(equipment['cost']['unit']))

    weight = str(equipment['weight']) + " lbs" if equipment['weight'] > 1 else str(equipment['weight']) + " lb"
    embed.add_field(name='Weight', value=weight)

    return embed

def embedArmorLookup(ctx, equipment: dict) -> discord.Embed:
    embed = discord.Embed(title=equipment['name'], color=0x3d4b80)

    author = equipment['armor_category']+" Armor"
    embed.set_author(name=author, icon_url=ctx.author.avatar_url)

    armorClass = equipment['armor_class']
    armorValue = f"{armorClass['base']} + Dex Modifier (max {armorClass['max_bonus']})" if armorClass['dex_bonus'] else f"{armorClass['base']}"
    embed.add_field(name='Armor Class', value=armorValue)

    cost = [str(value) for value in equipment['cost'].values()]
    embed.add_field(name='Cost', value=" ".join(cost))

    weight = str(equipment['weight']) + " lbs" if equipment['weight'] > 1 else str(equipment['weight']) + " lb"
    embed.add_field(name='Weight', value=weight)

    if equipment['stealth_disadvantage']:
        embed.add_field(name='Stealth', value="Wearing this armor gives you disadvantage on stealth checks.")

    embed.add_field(name='Strength Requirement', value=equipment['str_minimum'])

    return embed

# def embedClass(ctx, arch) -> discord.Embed:
#     embedVar = discord.Embed(title=arch['name'])

#     return embedVar


'''
This function cleans up input for the weapon lookup command.
This is needed due to the nature of certain items contained within the database
for weapons such as hand crossbows being listed as "crossbow-hand".
'''
# TODO:  Add functionality to deal with "example" and 'example' type inputs.
def cleanInputEquipment(args) -> str:
    clean_args = []
    for arg in args:
        arg = arg.lower().replace(',', "").replace('\'', "")

        if ' ' in arg:
            for split in arg.split(' '):
                clean_args.append(split)
        else:
            clean_args.append(arg)
    
    if 'crossbow' in clean_args:
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