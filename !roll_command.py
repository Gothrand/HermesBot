skill_dict = {"acrobatics": "Dex",
        "animal": "Wis",
        "arcana": "Int",
        "athletics": "Str",
        "deception": "Cha",
        "history": "Int",
        "insight": "Wis",
        "intimidation": "Cha",
        "investigation": "Int",
        "medicine": "Wis",
        "nature": "Int",
        "perception": "Wis",
        "performance": "Cha",
        "persuasion": "Cha",
        "religion": "Int",
        "sleight": "Dex",
        "sleightofhand": "Dex",
        "hand": "Dex",
        "stealth": "Dex",
        "survival": "Wis"
    }

attrbutes = {"Strength": "str",
        "Dexterity": "dex",
        "Constitution": "con",
        "Intelligence": "int",
        "Wisdom": "wis",
        "Charisma": "cha"
    }
import random
import discord
from character import getInfo

@bot.command(name="roll", help="rolls a die depending on whether it's a save, skill, attribute, or straight roll")
async def roll(ctx, *arg):
    mod = 0
    dice = []
    stat = 10
    k_kl = 0
    temp_string = ""
    loop = 1
    adv = 0
    temp_list1 = []
    temp_list2 = []
    final_list = []
    result = []

    if any(map(str.isdigit, arg[0])): # if arg0 contains an int, assume dice roller only
        if "d" not in arg[0]: #checks for multiple sets
            loop = int(arg.pop(0))
        if "k" in arg[-1]: #checks for kl (-) or k (+)
            temp = arg.pop(-1)
            if "l" in temp:
                temp_list = temp.split("l")
                k_kl -= int(temp_list[1])
            else:
                temp_list = temp.split("k")
                k_kl += int(temp_list[1])
        for i in arg: # adds dice to dice list or adds mods
            temp_string += i
        large_temp = temp_string.split("+")
        for i in large_temp:
            if "d" in i:
                temp = i.split("d")
                for j in range(temp[0]):
                    dice.append(int(temp[1]))
            else:
                mod += int(i)

    elif arg[0].lower() == "save" or arg[1].lower() == "save": # checks if saving throw
        dice.append(20)
        for i in attrbutes:
            if (
                (arg[0].lower() in i.lower()) or 
                (arg[1].lower() in i.lower()) or
                (arg[0].lower() in attrbutes[i]) or 
                (arg[1].lower() in attrbutes[i])
                ):
                attr = "ST " + i
                mod += int(getInfo(player, character, attr))

    elif arg[0].capitalize() in attrbutes or arg[0].capitalize() in ["Str", "Dex", "Con", "Int", "Wis", "Cha"]: # if straight stat roll
        if arg[0].capitalize() in attrbutes:
            attr = attrbutes[arg[0].capitalize()]
        else:
            attr = arg[0].capitalize()
        mod += int(getInfo(player, character, attr))

    elif arg[0].capitalize() in skill_dict.capitalize(): # checks if skill check
        dice.append(20)
        if arg[0].lower in ["sleight", "sleightofhand", "hand"]:
            attr = "SleightofHand"
        else:
            attr = arg[0].capitalize()
        mod += int(getInfo(player, character, attr))

    else: #error message if none of previous statments are met
        await ctx.send("word not found")

    for i in arg: # checks for advantage or disadvantage
        if i.lower() == "adv":
            adv += 1
        if i.lower() == "dis":
            adv -= 1

    for i in range(loop): #this loop rolls the dice and sorts them from largest to smallest
        for j in dice:
            temp_list1.append(random.randint(1,j))
            temp_list1.sort(reverse = True)
            if adv != 0:
                temp_list2.append(random.randint(1,j))
                temp_list2.sort(reverse = True)
        if adv != 0:   #if adv or dis, puts the smaller sum first
            if sum(temp_list1) <= sum(temp_list2):
                final_list.append(temp_list1)
                final_list.append(temp_list2)
            else:
                final_list.append(temp_list2)
                final_list.append(temp_list1)
        else:
            final_list.append(temp_list1)
    
    for i in range(len(final_list)):
        if k_kl > 0:
            temp = final_list[i][:k_kl]
        elif k_kl < 0:
            temp = final_list[i][k_kl:]
        else:
            temp = final_list[i]
        result.append(sum(temp) + mod)
    
    output = f"{player} Rolls: \n"
    for i in range(len(final_list)):
        output += final_list[i] + " Result: " + result[i] + "\n"
    await ctx.send(output)
    