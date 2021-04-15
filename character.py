'''
This file's purpose is to contain the classes used to represent a character with that character's stats and   
'''

# character name, player name, class, subclass, level, race, short description, stats list, spells, armor class, proficiencies, saving throws
class Character:
    charName = ""
    playerName = ""
    charClass = ""
    subClass = ""
    level = 1
    race = ""
    attributeScores = {"strength":10, "dexterity":10, "constitution":10, "intelligence":10, "wisdom":10, "charisma":10}
    spellList = {} # Will be something like 'spell':True/False where true/false represents if the spell is prepared or not.
    maxPreparedSpells = 0
    armorClass = 10
    profList = []
    savingThrows = {"strength":False, "dexterity":False, "constitution":False, "intelligence":False, "wisdom":False, "charisma":False}
    def __init__(self, **kwargs):
        return