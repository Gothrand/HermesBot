# embeds.py
import discord
from cogs.character_helpers import getInfo
from include import proficiencies

def embedCharacter(player, character):
    embedVar = discord.Embed(title=getInfo(player, character, "CharacterName"), color=0x3399ff)

    imageURL = getInfo(player, character, "CHARACTER IMAGE")
    if imageURL != "None" and imageURL != "null":
        print(imageURL)
        embedVar.set_image(url=imageURL)

    embedVar.add_field(name="Class/Level", value=getInfo(player, character, "ClassLevel"), inline=True)
    embedVar.add_field(name="Background", value=getInfo(player, character, "Background"), inline=True)
    embedVar.add_field(name="Player", value=getInfo(player, character, "PlayerName"), inline=True)

    embedVar.add_field(name="Race", value=getInfo(player, character, "Race "), inline=True)
    embedVar.add_field(name="Alignment", value=getInfo(player, character, "Alignment"), inline=True)
    embedVar.add_field(name="XP", value=getInfo(player, character, "XP"), inline=True)

    embedVar.add_field(name="Armor Class", value=getInfo(player, character, "AC"), inline=True)
    embedVar.add_field(name="Initiative", value=getInfo(player, character, "Initiative"), inline=True)
    embedVar.add_field(name="Speed", value=getInfo(player, character, "Speed"), inline=True)

    embedVar.add_field(name="Hit Dice", value=getInfo(player, character, "HD"), inline=True)
    embedVar.add_field(name="Current HP", value=getInfo(player, character, "HPCurrent"), inline=True)
    embedVar.add_field(name="Max HP", value=getInfo(player, character, "HPMax"), inline=True)

    return embedVar

# Needs formatting but this will work for now.
def embedAttributes(player, character):
    embedVar = discord.Embed(title=getInfo(player, character, "CharacterName"), color=0x42f560)

    textValue = '\N{BLACK DIAMOND}\t' + getInfo(player, character, "ST Strength") if getInfo(player, character, "Check Box 11") == "/Yes" else '\N{WHITE DIAMOND}\t' + getInfo(player, character, "ST Strength")
    embedVar.add_field(name="Str", value=getInfo(player, character, "STR"), inline=True)
    embedVar.add_field(name="Mod", value=getInfo(player, character, "STRmod"), inline=True)
    embedVar.add_field(name="ST", value=textValue, inline=True)

    textValue = '\N{BLACK DIAMOND}\t' + getInfo(player, character, "ST Dexterity") if getInfo(player, character, "Check Box 18") == "/Yes" else '\N{WHITE DIAMOND}\t' + getInfo(player, character, "ST Dexterity")
    embedVar.add_field(name="Dex", value=getInfo(player, character, "DEX"), inline=True)
    embedVar.add_field(name="Mod", value=getInfo(player, character, "DEXmod "), inline=True) # DEXmod has a space at the end, go figure
    embedVar.add_field(name="ST", value=textValue, inline=True)

    textValue = '\N{BLACK DIAMOND}\t' + getInfo(player, character, "ST Constitution") if getInfo(player, character, "Check Box 19") == "/Yes" else '\N{WHITE DIAMOND}\t' + getInfo(player, character, "ST Constitution")
    embedVar.add_field(name="Con", value=getInfo(player, character, "CON"), inline=True)
    embedVar.add_field(name="Mod", value=getInfo(player, character, "CONmod"), inline=True)
    embedVar.add_field(name="ST", value=textValue, inline=True)

    textValue = '\N{BLACK DIAMOND}\t' + getInfo(player, character, "ST Intelligence") if getInfo(player, character, "Check Box 20") == "/Yes" else '\N{WHITE DIAMOND}\t' + getInfo(player, character, "ST Intelligence")
    embedVar.add_field(name="Int", value=getInfo(player, character, "INT"), inline=True)
    embedVar.add_field(name="Mod", value=getInfo(player, character, "INTmod"), inline=True)
    embedVar.add_field(name="ST", value=textValue, inline=True)

    textValue = '\N{BLACK DIAMOND}\t' + getInfo(player, character, "ST Wisdom") if getInfo(player, character, "Check Box 21") == "/Yes" else '\N{WHITE DIAMOND}\t' + getInfo(player, character, "ST Wisdom")
    embedVar.add_field(name="Wis", value=getInfo(player, character, "WIS"), inline=True)
    embedVar.add_field(name="Mod", value=getInfo(player, character, "WISmod"), inline=True)
    embedVar.add_field(name="ST", value=textValue, inline=True)

    textValue = '\N{BLACK DIAMOND}\t' + getInfo(player, character, "ST Charisma") if getInfo(player, character, "Check Box 22") == "/Yes" else '\N{WHITE DIAMOND}\t' + getInfo(player, character, "ST Charisma")
    embedVar.add_field(name="Cha", value=getInfo(player, character, "CHAR"), inline=True)
    embedVar.add_field(name="Mod", value=getInfo(player, character, "CHamod"), inline=True) # Charisma goes against the grain and wants to be called 'CHamod' instead of 'CHAmod'
    embedVar.add_field(name="ST", value=textValue, inline=True)

    return embedVar

def embedProfs(player, character):
    embedVar = discord.Embed(title=getInfo(player, character, "CharacterName"), color=0x42f560)
    for i, prof in enumerate(proficiencies):
        textValue = '\N{BLACK DIAMOND}\t' + getInfo(player, character, prof) if getInfo(player, character, f"Check Box {23+i}") == "/Yes" else '\N{WHITE DIAMOND}\t' + getInfo(player, character, prof)
        embedVar.add_field(name=prof, value=textValue, inline=False)

    return embedVar

def embedWeapons(player, character):
    embedVar = discord.Embed(title=getInfo(player, character, "CharacterName"), color=0xd93636)

    embedVar.add_field(name="Weapon 1", value=getInfo(player, character, "Wpn Name"), inline=True)
    embedVar.add_field(name="Modifier", value=getInfo(player, character, "Wpn1 AtkBonus"), inline=True)
    embedVar.add_field(name="Damage", value=getInfo(player, character, "Wpn1 Damage"), inline=True)

    embedVar.add_field(name="Weapon 2", value=getInfo(player, character, "Wpn Name 2"), inline=True)
    embedVar.add_field(name="Modifier", value=getInfo(player, character, "Wpn2 AtkBonus "), inline=True)
    embedVar.add_field(name="Damage", value=getInfo(player, character, "Wpn2 Damage "), inline=True)

    embedVar.add_field(name="Weapon 3", value=getInfo(player, character, "Wpn Name 3"), inline=True)
    embedVar.add_field(name="Modifier", value=getInfo(player, character, "Wpn3 AtkBonus  "), inline=True)
    embedVar.add_field(name="Damage", value=getInfo(player, character, "Wpn3 Damage "), inline=True)

    return embedVar
    

def embedSpell(ctx, spell):
    # Handle the author portion of the embed, which will contain the spell level and magic school of the spell
    author = ""
    if spell['level'] == 0:
        author = f"cantrip {spell['school']['index']}"
    elif spell['level'] == 1:
        author = f"1st level {spell['school']['index']}"
    elif spell['level'] == 2:
        author = f"2nd level {spell['school']['index']}"
    elif spell['level'] == 3:
        author = f"3rd level {spell['school']['index']}"
    else:
        author = f"{spell['level']}th level {spell['school']['index']}"
    
    # Add ritual tag if necessary
    if spell['ritual'] == True:
        author += " (ritual)"

    # Descriptions are split into a list of sentences, so need to handle that
    description = ""
    if isinstance(spell['desc'], list):
        for sentence in spell['desc']:
            description += sentence+'\n'
    else:
        description = spell['desc']

    # Components are also a list of characters but we want them in a row so handle that and add material
    # components if necessary
    components = str(spell['components']).replace("[", "")
    components = components.replace("]", "")
    components = components.replace("'", "")
    try:
        components += f" ({spell['material']})"
        components = components.replace('.', '')
    except:
        print("No material components found.  Moving on.")
    
    # Format the classes that the spell belongs to
    classes = ""
    for item in spell['classes']:
        classes += item["name"]+', '
    classes = classes[:-2]
    
    # Create the embed
    embedVar = discord.Embed(title=spell['name'], description=description, color=0xba4aff)
    embedVar.set_author(name=author, icon_url=ctx.author.avatar_url)
    embedVar.add_field(name="Casting Time", value=spell['casting_time'])
    embedVar.add_field(name="Range", value=spell['range'])
    embedVar.add_field(name="Components", value=components)
    embedVar.add_field(name="Duration", value="C, " + spell["duration"] if spell['concentration'] == True else spell['duration'])
    embedVar.add_field(name="Classes", value=classes)

    # Not all spells have a higher level tag so add those if they are there.
    try:
        embedVar.add_field(name="At Higher Levels", value=spell['higher_level'][0], inline=False)
    except:
        print("No higher level modifier found.  Moving on.")

    return embedVar

# test code
if __name__ == "__main__":
    print("Embed driver code")