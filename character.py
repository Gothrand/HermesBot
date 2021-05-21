'''
This file's purpose is to contain the classes used to represent a character with that character's stats and   
'''
import json, PyPDF2
import discord
from include import dataStructure, modifiableAttrs
#TODO: Add a table of contents for attributes that the player can use to see what attributes they can modify
#TODO: Attunements list function
#TODO: Smarter character sheet algorithms e.g. Read attribute scores and correct character sheet wherever necessary

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
def findCharacter(player, character : str, data=None):
    if data is not None:
        charIndex = -1
        for i, item in enumerate(data[player]):
            if item["CharacterName"] == character:
                charIndex = i
                break
        else:
            return None
    else:
        data = loadJSON(fileName)
        charIndex = -1
        for i, item in enumerate(data[player]):
            if item["CharacterName"] == character:
                charIndex = i
                break
        else:
            return None
    
    return charIndex

def getCharacters(player):
    data = loadJSON(fileName)
    result = []
    for character in data[player]:
        result.append(character["CharacterName"])
    
    return result

# updates certain keys about a character with the corresponding value.  Returns false if the character is not found.
def updateChar(player, character, key, value):
    data = loadJSON(fileName)

    try:
        # order of access: player discord tag, that player's character, value for that character to be modified
        data[player][findCharacter(player, character)][key] = value
        newData = json.dumps(data)
        writeJSON(fileName, newData)

    except:
        return False

    return True

# an image representing what the character looks like seems important enough to warrant it's own function, also because "CHARACTER IMAGE"
# is dumb to type out fully when updating the value
def setImage(player, character, value):
    data = loadJSON(fileName)

    try:
        data[player][findCharacter(player, character)]["CHARACTER IMAGE"] = value
        newData = json.dumps(data)
        writeJSON(fileName, newData)
    except:
        return False
    
    return True

# Returns information about the value about a character corresponding to the key
def getInfo(player, character, key):
    data = loadJSON(fileName)    
    item = data[player][findCharacter(player, character)][key] if data[player][findCharacter(player, character)][key] != "" else "null"
    return item

# Creates a new character underneath the corresponding discord tag.
def addCharacter(player, character):
    data = loadJSON(fileName)
    if len(data) == 0:
        data = {player:[dataStructure]}
        data[player][0]["CharacterName"] = character
    elif player not in data:
        data.update({player:[dataStructure]})
        data[player][0]["CharacterName"] = character
    else:
        data[player].append(dataStructure)
        data[player][-1]["CharacterName"] = character
    
    newData = json.dumps(data)
    writeJSON(fileName, newData)
    
    return

def addPlayer(player):
    data = loadJSON(fileName)
    data.update({player:[]})
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

def importFromPDF(player, character):
    data = loadJSON(fileName)

    if player not in data:
        data.update({player:[dataStructure]})
        data[player][0]["CharacterName"] = character
    elif player in data:
        data[player].append(dataStructure)
        data[player][-1]["CharacterName"] = character
    
    pdfFileObj = open('characterSheet.pdf', 'rb')
    pdf = PyPDF2.PdfFileReader(pdfFileObj)

    fields = pdf.getFields()
    for field_name, value in fields.items():
        field_value = value.get('/V')
        
        if field_name == "CharacterName":
            continue

        index = findCharacter(player, character, data=data)
        data[player][index][str(field_name)] = str(field_value)

    newData = json.dumps(data)
    writeJSON(fileName, newData)
    pdfFileObj.close()
    return

def listAttributes():
    keys = []
    for key in modifiableAttrs:
        keys.append(key)
    
    return keys

# Driver code
if __name__ ==  "__main__":
    y = json.dumps({})
    writeJSON(fileName, y)