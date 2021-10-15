from os import write
from PIL import Image, ImageDraw, ImageFont
import json
import discord
from glob import glob
# from include import MAP_STRUCTURE

MAP_STRUCTURE = {
    "path":"",
    "positions":{},
    "diff":0
}

extension = ".jpg"
image_type = "JPEG"

# Inits
mappings = {}
alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
currentMap = "currentMap.json"

for i, letter in enumerate(alph):
    mappings.update({letter:int(i)})

def loadJSON(file):
    with open(file, "r") as f:
        data = json.load(f)
    
    return data

def writeJSON(file, jsonString):
    with open(file, "w") as f:
        f.write(jsonString)

    return

def addGrid(image, boxes):
    width, height = image.size
    diff = int(width/boxes)

    # This detects variations in the original image and corrects them
    # (prevents missaligned grids if a grid is already present)
    error = height % diff
    if error != 0:
        height -= error
        image = image.resize((width, height))

    pointsize = int(diff/5)
    shadowcolor = "black"
    draw = ImageDraw.Draw(image)
    font = "arial.ttf"
    font = ImageFont.truetype(font, pointsize)

    # From top to bottom, draw horizontal lines startig at (0, y) and ending at (width, y)
    # (0, y) shoul always be (0, 0) at the start and 'width' is the maximum X value of the image.
    # Diff is the length of a single edge of a box and is used as a step value for the range() function.
    for y in range(0, height, diff):
        draw.line([(0, y), (width, y)], fill=(0, 0, 0))
    
    # From the left to right, draw vertical lines starting at (x, 0) (should be (0, 0)) and end at the maximum Y value of the drawing.
    for x in range(0, width, diff):
        draw.line([(x, 0), (x, height)], fill=(0, 0, 0))
    
    
    rightShift = 5 # Used to rightshift coordinate text e.g. 5 pixels over or so
    positions = {} # Storing what valid positions there are on the map
    for i in range(0, height, diff):
        for j in range(0, width, diff):
            text = f"{alph[int(j/diff)]}{str(int(i/diff))}"

            draw.text((j-1+rightShift, i), text, font=font, fill=shadowcolor)
            draw.text((j+1+rightShift, i), text, font=font, fill=shadowcolor)
            draw.text((j+rightShift, i-1), text, font=font, fill=shadowcolor)
            draw.text((j+rightShift, i+1), text, font=font, fill=shadowcolor)


            draw.text((j+rightShift, i), text, font=font)
            positions.update({text:""})

    # image with the added grid, positions to store what values there are in the grid, and diff for the edge length of a particular box
    return image, positions, diff

# ----- Setters -----

#TODO: This needs to add a map to the structure, not simply just replace the old one.  Will allow for more maps to
# be added instead of constantly replacing maps.  Will need a function to delete old unwanted maps.
def setMap(mapPath, boxes : int):
    # Delete current map data
    writeJSON(currentMap, json.dumps(MAP_STRUCTURE))

    # load fresh data
    data = loadJSON(currentMap)

    with Image.open(mapPath) as im:
        newMapPath = mapPath.split('.', 1)[0]
        newMapPath = newMapPath + "_grid.jpg"
        im, positions, diff = addGrid(im, boxes)
        im = im.convert("RGB")
        im.save(newMapPath, "JPEG")

    data["path"] = newMapPath
    data["positions"] = positions
    data["diff"] = diff

    newData = json.dumps(data)
    writeJSON(currentMap, newData)
    return

def update(player, position):
    data = loadJSON(currentMap)

    # If the spot they want to move to is occupied, then return false
    if data["positions"][position] != "":
        return False

    # Find where the player is.  If the player is not placed yet, then place them at the empty positon they wish to go to.
    location = getPosition(player)
    if location is None:
        data["positions"][position] = player
        newData = json.dumps(data)
        writeJSON(currentMap, newData)
    
    # Erase the player from their current position and place them at the new one.
    else:
        data["positions"][location] = ""
        data["positions"][position] = player
        newData = json.dumps(data)
        writeJSON(currentMap, newData)
    
    return True


tokensPath = 'tokens/'
def render():
    
    data = loadJSON(currentMap)
    diff = data["diff"]
    with Image.open(data["path"]) as im:
        image = im.copy()

    tokens = glob(tokensPath+"*")
    players = getPlayers()

    for token in tokens:
        player = token.replace('\\', '/')
        player = player.split('/')[-1]
        player = player.split('.', 1)[0]

        if player in players.keys():
            with Image.open(token) as im:
                im = im.resize((diff, diff))
                im = im.convert('RGB')
                im.save(tokensPath+'paste.jpg', 'JPEG')
                image.paste(im, getPixelCoordinate(players[player], diff))
                

    image.save("resources/maps/activemap.jpg", "JPEG")

    return "resources/maps/activemap.jpg"

def move(player, position):
    if update(player, position):
        print("Position updated.")
    else:
        print("Could not update position.")
        return False
    
    return True

# ----- Getters -----

# Using the given coordinate, finds the pixel value for the upper left-hand corner of a given square
def getPixelCoordinate(coordinate, diff : int):
    letter = coordinate[0]
    number = coordinate[1:]
    # print(letter, number)
    x = int(mappings[letter]) * diff
    y = int(number) * diff

    return (x, y)

def getPosition(player):
    data = loadJSON(currentMap)

    player_position = ""
    
    for position, item in data["positions"].items():
        if item == player:
            player_position = position
            break
    else:
        return None
    
    return player_position

def getPlayers():
    data = loadJSON(currentMap)

    players = {}
    for key, player in data["positions"].items():
        if player != "":
            players.update({player:key})

    return players
    
# Gets a specific region of the image, to be used in dungeon exploration.
def getRegion(pos1, pos2):
    data = loadJSON(currentMap)
    diff = data['diff']
    with Image.open(data["path"]) as im:
        image = im.copy()

    first = getPixelCoordinate(pos1, diff)
    second = getPixelCoordinate(pos2, diff)

    left = first[0]
    top = first[1]
    right = second[0] + diff
    bottom = second[1] + diff
    box = (left, top, right, bottom)

    region = image.crop(box)
    region.save("resources/maps/region.jpg", "JPEG")

    return "resources/maps/region.jpg"

# ----- Driver Code -----
if __name__ == "__main__":
    writeJSON(currentMap, json.dumps(MAP_STRUCTURE))