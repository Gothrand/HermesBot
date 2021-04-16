'''
This file's purpose is to contain the classes used to represent a character with that character's stats and   
'''
import json
from enum import Enum
# This represents what a character's information looks like.  A discord user will have a list of these
# data blocks under their tag for each character they own.
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
    "background":"",
    "alignment":"",
    "imageURL":""
}

# where we are storing character data
fileName = "charSheet.json"

# helper function to load JSON files
def loadJSON(file):
    with open(file, "r") as f:
        data = json.load(f)
    
    return data

# helper function to write to JSON files with a JSON string
def writeJSON(file, jsonString):
    with open(file, "w") as f:
        f.write(jsonString)
    
    return

# Finds a character under the player's discord tag which has a matching character name
# Returns None if the character is not found.
def findCharacter(player, character):
    data = loadJSON(fileName)
    charIndex = -1
    for i, item in enumerate(data[player]):
        if item["charName"] == character:
            charIndex = i
            break
    else:
        return None
    
    return charIndex

# updates certain keys about a character with the corresponding value.  Returns false if the character is not found.
def updateChar(player, character, key, value):
    data = loadJSON(fileName)

    try:
        data[player][findCharacter(player, character)][key] = value
        newData = json.dumps(data)
        writeJSON(fileName, newData)

    except:
        return False

    return True

# Returns information about the value about a character corresponding to the key
def getInfo(player, character, key):
    data = loadJSON(fileName)
    
    try:
        item = data[player][findCharacter(player, character)][key] if data[player][findCharacter(player, character)][key] != "" else "null"
        return item
    except:
        return "null"

# Creates a new character underneath the corresponding discord tag.
def addCharacter(player, character):
    data = loadJSON(fileName)
    print(len(data))
    if len(data) == 0:
        data = {player:[dataStructure]}
        data[player][0]["charName"] = character
        print(data)
    else:
        data[player].append(dataStructure)
        data[player][-1]["charName"] = character
    
    newData = json.dumps(data)
    writeJSON(fileName, newData)
    
    return

# Removes a character from the corresponding player's character list.
def removeCharacter(player, character):
    data = loadJSON(fileName)
    try:
        del data[player][findCharacter(player, character)]
        newData = json.dumps(data)
        writeJSON(fileName, newData)
        return True
    except:
        print("Character not found.  Aborting.")

    return False


# Driver code
if __name__ ==  "__main__":
    y = json.dumps({})
    writeJSON(fileName, y)

    addCharacter("Gothrand#9375", "Gothrand")
    updateChar("Gothrand#9375", "charName", "Gothrand")
    print(getInfo("Gothrand#9375", "charName"))