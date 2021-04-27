# embeds.py

from character import *

def embedCharacter(player, character):
    embedVar = discord.Embed(title=getInfo(player, character, "CharacterName"), color=0x3399ff)

    embedVar.set_image(url=getInfo(player, character, "CHARACTER IMAGE"))

    embedVar.add_field(name="Class/Level", value=getInfo(player, character, "ClassLevel"), inline=True)
    embedVar.add_field(name="Background", value=getInfo(player, character, "Background"), inline=True)
    embedVar.add_field(name="Player", value=getInfo(player, character, "PlayerName"), inline=True)

    embedVar.add_field(name="Race", value=getInfo(player, character, "Race "), inline=True)
    embedVar.add_field(name="Alignment", value=getInfo(player, character, "Alignment"), inline=True)
    embedVar.add_field(name="XP", value=getInfo(player, character, "XP"), inline=True)

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