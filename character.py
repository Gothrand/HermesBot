'''
This file's purpose is to contain the classes used to represent a character with that character's stats and   
'''
import json, PyPDF2
import discord

# This represents what a character's information looks like.  A discord user will have a list of these
# data blocks under their tag for each character they own.
dataStructure = {
    "ClassLevel":"",
    "Background":"",
    "PlayerName":"",
    "CharacterName":"",
    "Race ":"",
    "Alignment":"",
    "XP":"",
    "Inspiration":"",
    "ProfBonus":"2",
    "AC":"10", # Armor Class
    "Initiative":"",
    "Speed":"0",
    "HPMax":"0",
    "HPCurrent":"",
    "HPTemp":"0",
    "HD":"", # Hit dice
    "STR":"10",
    "DEX":"10",
    "CON":"10",
    "INT":"10",
    "WIS":"10",
    "CHAR":"10",
    "STRmod":"",
    "DEXmod ":"", # Space
    "CONmod":"",
    "INTmod":"",
    "WISmod":"",
    "CHamod":"",
    "Check Box 11":"", # Strength Saving Throw Prof, each follows as suit.  Value is either 'None' or '/Yes'
    "Check Box 18":"",
    "Check Box 19":"",
    "Check Box 20":"",
    "Check Box 21":"",
    "Check Box 22":"",
    "ST Strength":"", # Saving Throws
    "ST Dexterity":"",
    "ST Constitution":"",
    "ST Intelligence":"",
    "ST Wisdom":"",
    "ST Charisma":"",
    "Acrobatics":"",
    "Animal":"",
    "Arcana":"",
    "Athletics":"",
    "Deception ":"", # Space
    "History ":"", # Space
    "Insight":"",
    "Intimidation":"",
    "Investigation ":"", # Space
    "Medicine":"",
    "Nature":"",
    "Perception ":"", # Space
    "Performance":"",
    "Persuasion":"",
    "Religion":"",
    "SleightofHand":"",
    "Stealth ":"", # Space
    "Survival":"",
    "Wpn Name":"",
    "Wpn1 AtkBonus":"",
    "Wpn1 Damage":"",
    "Wpn Name 2 ":"", # Space
    "Wpn2 AtkBonus ":"", # Space
    "Wpn2 Damage ":"", # Space
    "Wpn Name 3":"",
    "Wpn3 AtkBonus  ":"", # Space
    "Wpn3 Damage ":"", # Space
    "AttacksSpellcasting":"",
    "Passive":"", # Passive Perception
    "CP":"",
    "SP":"",
    "EP":"",
    "GP":"",
    "PP":"",
    "ProficienciesLang":"",
    "Age":"",
    "Height":"",
    "Weight":"",
    "Eyes":"",
    "Skin":"",
    "Hair":"",
    "PersonalityTraits":"",
    "Ideals":"",
    "Bonds":"",
    "Flaws":""
}

#TODO: Add a table of contents for attributes that the player can use to see what attributes they can modify
#TODO: Add functions for printing proficiency lists
#TODO: Add function for printing ability score list
#TODO: Attunements list function
#TODO: Smarter character sheet algorithms e.g. Read attribute scores and correct character sheet wherever necessary

# where we are storing character data
fileName = "charSheet.json"

proficiencies = ["Acrobatics",
                 "Animal",
                 "Arcana",
                 "Athletics",
                 "Deception ", # Space
                 "History ", # Space
                 "Insight",
                 "Intimidation",
                 "Investigation ", # Space
                 "Medicine",
                 "Nature",
                 "Perception ", # Space
                 "Performance",
                 "Persuasion",
                 "Religion",
                 "SleightofHand",
                 "Stealth ", # Space
                 "Survival"]

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

# Driver code
if __name__ ==  "__main__":
    y = json.dumps({})
    writeJSON(fileName, y)