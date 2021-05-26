# This represents what a character's information looks like.  A discord user will have a list of these
# data blocks under their tag for each character they own.
dataStructure = {
    "ClassLevel":"",
    "Background":"",
    "PlayerName":"",
    "CharacterName":"",
    "Race ":"",  # Space
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
    "Equipment":"Equipment",
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

proficiencies = [
    "Acrobatics",
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
    "Survival"
]

# Format: { user_friendly_attr_name : pdf_attr_name }
# Some of the original attribute names in the pdf have spaces at the end of them and the JSON detects those
# so in the future some work could be done to cut off those spaces at will.
modifiableAttrs = {
    "ClassLevel":"ClassLevel",
    "Background":"Background",
    "PlayerName":"PlayerName",
    "CharacterName":"CharacterName",
    "Race ":"Race ",
    "Alignment":"Alignment",
    "XP":"XP",
    "Inspiration":"Inspiration",
    "ProfBonus":"ProfBonus",
    "AC":"AC", # Armor Class
    "Initiative":"Initiative",
    "Speed":"Speed",
    "HPMax":"HPMax",
    "HPCurrent":"HPCurrent",
    "HPTemp":"HPTemp",
    "HitDice":"HD", # Hit dice
    "Str":"STR",
    "Dex":"DEX",
    "Con":"CON",
    "Int":"INT",
    "Wis":"WIS",
    "Cha":"CHAR",
    "STRmod":"STRmod",
    "DEXmod":"DEXmod ", # Space
    "CONmod":"CONmod",
    "INTmod":"INTmod",
    "WISmod":"WISmod",
    "CHAmod":"CHamod",
    "ST Prof Strength":"Check Box 11", # Strength Saving Throw Prof, each follows as suit.  Value is either 'None' or '/Yes'
    "ST Prof Dexterity":"Check Box 18",
    "ST Prof Constitution":"Check Box 19",
    "ST Prof Intelligence":"Check Box 20",
    "ST Prof Wisdom":"Check Box 21",
    "ST Prof Charisma":"Check Box 22",
    "ST Strength":"ST Strength", # Saving Throws
    "ST Dexterity":"ST Dexterity",
    "ST Constitution":"ST Constitution",
    "ST Intelligence":"ST Intelligence",
    "ST Wisdom":"ST Wisdom",
    "ST Charisma":"ST Charisma",
    "Acrobatics":"Acrobatics",
    "Animal":"Animal",
    "Arcana":"Arcana",
    "Athletics":"Athletics",
    "Deception":"Deception ", # Space
    "History":"History ", # Space
    "Insight":"Insight",
    "Intimidation":"Intimidation",
    "Investigation":"Investigation ", # Space
    "Medicine":"Medicine",
    "Nature":"Nature",
    "Perception":"Perception ", # Space
    "Performance":"Performance",
    "Persuasion":"Persuasion",
    "Religion":"Religion",
    "SleightofHand":"SleightofHand",
    "Stealth":"Stealth ", # Space
    "Survival":"Survival",
    "Weapon1Name":"Wpn Name",
    "Weapon1AtkBonus":"Wpn1 AtkBonus",
    "Weapon1Damage":"Wpn1 Damage",
    "Weapon2Name":"Wpn Name 2 ", # Space
    "Weapon2AtkBonus":"Wpn2 AtkBonus ", # Space
    "Weapon2Damage":"Wpn2 Damage ", # Space
    "Weapon3Name":"Wpn Name 3",
    "Weapon3AtkBonus":"Wpn3 AtkBonus  ", # Double Space
    "Weapon3Damage":"Wpn3 Damage ", # Space
    "Attacks&Spellcasting":"AttacksSpellcasting",
    "Equipment":"Equipment",
    "FeaturesTraits":"Features and Traits",
    "PassivePerception":"Passive", # Passive Perception
    "CP":"CP",
    "SP":"SP",
    "EP":"EP",
    "GP":"GP",
    "PP":"PP",
    "ProfsLanguages":"ProficienciesLang",
    "Age":"Age",
    "Height":"Height",
    "Weight":"Weight",
    "Eyes":"Eyes",
    "Skin":"Skin",
    "Hair":"Hair",
    "PersonalityTraits":"PersonalityTraits",
    "Ideals":"Ideals",
    "Bonds":"Bonds",
    "Flaws":"Flaws"
}

DOMT_DESCRIPTIONS = {
    "Balance":"Your mind suffers a wrenching alteration, causing your alignment to change.  Lawful becomes chaotic, good becomes evil, and vice versa.  If you are true neutral or uinaligned, this card has no effect on you.",
    "Comet":"If you single-handedly defeat the next hostile monster or group of monsters you encounter, you gain experience points enough to gain one level.  Otherwise, this card has no effect.",
    "Donjon":"You disappear and become entombed in a state of suspended animation in an extradimensional sphere.  Everything you were wearing and carrying stays behind in the space you occupied when you disappeared.  You remain imprisoned until you are found and removed from the sphere.  You can't be located by any divination magic, but a wish spell can reveal the location of your prison.  You draw no more cards.",
    "Euryale":"The card's medusa-like visage curses you.  You take a -2 penalty on saving throws while cursed in this way.  Only a god or the magic of *The Fates* card can end this curse.",
    "The Fates":"Reality's fabric unravels and spins anew, allowing you to avoid or erase one event as if it never happened.  You can use the card's magic as soon as you draw the card or at any other time before you die.",
    "Flames":"A powerful devil becomes your enemy.  The devil seeks your ruin and plagues your life, savoring your suffering before attempting to slay you.  This enmity lasts until either you or the devil dies.",
    "Fool":"You lose 10,000 XP, discard this card, and draw from the deck again, counting both draws as one of your declared draws.  If losing that much XP would cause yo to lose a level, you instead lose an amount that leaves you with just enough XP to keep your level.",
    "Gem":"Twenty-five pieces of jewelry worth 2,000 gp each or fifty gems worth 1,000 gp each appear at your feet.",
    "Idiot":"Permanently reduce your Intelligence by 1d4+1 (to a minimum score of 1).  You can draw one additional card beyond your declared draws.",
    "Jester":"You gain 10,000 XP, or you can draw two additional cards beyond your declared draws.",
    "Key":"A rare or rarer magic weapon with which you are proficient appears in your hands.  The GM chooses the weapon.",
    "Knight":"You gain the service of a 4th level fighter who appears in a space you choose within 30 feet of you.  The figher is of the same race as you and serves you loyally until death, believing the fates have drawn him or her to you.  You control this character.",
    "Moon":"You are granted the ability to cast the *wish* spell 1d3 times.",
    "Rogue":"A nonplayer character of the GM's choice becomes hostile toward you.  The identity of your new enemy isn't known until the NPC or someone else reveals it.  Nothing less than a wish spell or divine intervention can end the NPC's hostility toward you.",
    "Ruin":"All forms of wealth that you carry or own, other than magic items, are lost to you.  Portable property vanishes.  Businesses, buildings, and land you own are lost in a way that alters reality the least.  Any documentation that proves you should own something lost to this card also disappears.",
    "Skull":"You summon an avatar of death - a ghostly humanoid skeleton clad in a tattered black robe and carrying a spectral scythe.  It apperas in a space of the GM's choice within 10 feet of you and attacks you, warning all others that you must win the battle alone.  The avatar fights until you die or it drops to 0 hit points, whereupon it disappears.  If anyone tries to help you, the hlper summons its own avatar of death.  A creature slain by an avatar of death can't be restored to life.",
    "Star":"Increase one of your ability scores by 2.  The score can exceed 20 but can't exceed 24.",
    "Sun":"You gain 50,000 XP, and a wondrous item (which the GM determines randomly) appears in your hands.",
    "Talons":"Every magic item you wear or carry disintegrates.  Artifacts in your possession aren't destroyed but do vanish.",
    "Throne":"You gain proficiency in the Persuasion skill, and you double your proficiency bonus on checks made with that skill.  In addition, you gain rightful ownership of a small keep somewhere in the world.  However, the keep is currently in the hands of monsters, which you must clear out before you can claim the keep as yours.",
    "Vizier":"At any time you choose within one year of drawing this card, you can ask a question in meditation and mentally receive a truthful answer to that question.  Besides information, the answer helps you solve a puzzling problem or other dilemma.  In other words, the knowledge comes with wisdom on how to apply it.",
    "Void":"This black card spells disaster.  Your soul is drawn from yourbody and contained in an object in a place of the GM's choice.  One or more powerful beings guard the place.  While your soul is trapped in this way, your body is incapacitated.  A wish spell can't restore your soul, but the spell reveals the location of the object that holds it.  You draw no more cards."
}


