'''
This file's purpose is to contain the classes used to represent a character with that character's stats and   
'''
import json

dataStructure = {
    "charName":"",
    "playerName":"",
    "charClass":"",
    "subClass":"",
    "level":"1",
    "race":"",
    "attrStr":"10",
    "attrDex":"10",
    "attrCon":"10",
    "attrInt":"10",
    "attrWis":"10",
    "attrChar":"10",
    "spellList":"", # Will be something like 'spell':True/False where true/false represents if the spell is prepared or not.
    "maxPreparedSpells":"0",
    "armorClass":"10",
    "profList":"",
    "savingThrows":"",
    "profBonus":"2",
    "charImage":"",
    "maxHP":"0",
    "speed":"0",
    "tempHP":"0",
    "hitDice":"",
    "background":""
}
# character name, player name, class, subclass, level, race, short description, stats list, spells, armor class, proficiencies, saving throws

fileName = "charSheet.json"

def updateChar(player, key, value):
    with open(fileName, "r") as f:
        data = json.load(f)

    try:
        data[player][0][key] = value
        newData = json.dumps(data)
        with open(fileName, "w") as f:
            f.write(newData)
    except AttributeError:
        print("fuck")
        return None

    return

def getInfo(player, key):
    with open(fileName, "r") as f:
        data = json.load(f)
    
    try:
        return data[player][0][key]
    except AttributeError:
        print("fuck 2.0")
        return None

def addCharacter(playerName):
    with open(fileName, "r") as f:
        data = json.load(f)
    
    data.update({playerName:[dataStructure]})
    newData = json.dumps(data)
    with open(fileName, "w") as f:
        f.write(newData)

def removeCharacter(playerName):
    with open(fileName, "r") as f:
        data = json.load(f)
    
    del data[playerName]
    newData = json.dumps(data)
    with open(fileName, "w") as f:
        f.write(newData)

if __name__ ==  "__main__":
    y = json.dumps({})
    with open(fileName, "w") as f:
        f.write(y)

    addCharacter("Gothrand#9375")
    updateChar("Gothrand#9375", "charName", "Gothrand")
    print(getInfo("Gothrand#9375", "charName"))