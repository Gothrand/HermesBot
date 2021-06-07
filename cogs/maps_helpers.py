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

# Inits
mappings = {}
alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
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

def addGrid(image, diff):
    width, height = image.size
    diff = int(width/diff)

    # This detects variations in the original image and corrects them
    # (prevents missaligned grids if a grid is already present)
    error = height % diff
    if error != 0:
        height -= error
        image = image.resize((width, height))

    pointsize=int(diff/5)
    shadowcolor = "black"
    draw = ImageDraw.Draw(image)
    font="arial.ttf"
    font = ImageFont.truetype(font, pointsize)

    for y in range(0, height, diff):
        draw.line([(0, y), (width, y)], fill=(0, 0, 0))
        
    for x in range(0, width, diff):
        draw.line([(x, 0), (x, height)], fill=(0, 0, 0))
    
    rightShift = 5
    positions = {}
    for i in range(0, height, diff):
        for j in range(0, width, diff):
            text = f"{alph[int(j/diff)]}{str(int(i/diff))}"

            draw.text((j-1+rightShift, i), text, font=font, fill=shadowcolor)
            draw.text((j+1+rightShift, i), text, font=font, fill=shadowcolor)
            draw.text((j+rightShift, i-1), text, font=font, fill=shadowcolor)
            draw.text((j+rightShift, i+1), text, font=font, fill=shadowcolor)


            draw.text((j+rightShift, i), text, font=font)
            positions.update({text:""})

    return image, positions, diff

def getPixelCoordinate(coordinate, diff : int):
    letter = coordinate[0]
    number = coordinate[1:]
    print(letter, number)
    x = int(mappings[letter]) * diff
    y = int(number) * diff

    return (x, y)

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

    location = findPosition(player)
    if location is None:
        data["positions"][position] = player
        newData = json.dumps(data)
        writeJSON(currentMap, newData)
        
    else:
        data["positions"][location] = ""
        data["positions"][position] = player
        newData = json.dumps(data)
        writeJSON(currentMap, newData)
    
    return True


tokensPath = 'resources/tokens/'
def render():
    
    data = loadJSON(currentMap)
    diff = data["diff"]
    with Image.open(data["path"]) as im:
        image = im.copy()

    tokens = glob(tokensPath+"*")
    players = getPlayers()

    print(tokens, players)
    for token in tokens:
        print("COCK AND BALL TORTURE")
        player = token.replace('\\', '/')
        player = player.split('/')[-1]
        player = player.split('.', 1)[0]

        print(players.keys())
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

def findPosition(player):
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
        
if __name__ == "__main__":
    writeJSON(currentMap, json.dumps(MAP_STRUCTURE))