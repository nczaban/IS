# Nicholas Czaban
# The following functions run a game with randomly-generated actions. The two possible actions
# are healing and attacking. Both players begin with 25 hit points. An attack removes 5 hit points,
# and healing restores 4 hit points. The first player has a 50-50 chance of either action. The second
# player has a randomly generated "agressiveness" value, determining how likely they are to heal.
from random import random
import os, sys
import pygame

if not pygame.font: print("Fonts are unavailable and have been disabled")
if not pygame.mixer: print("Sounds are unavailable and have been disabled")

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print("Cannot load image: ", name)
        raise SystemExit
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print("Cannot load sound: ", name)
        raise SystemExit
    return sound

def gameLoop():
    hitPoints = [25, 25]
    turnCounter = 0
    isPlayer0Turn = True
    agressiveness = random()
    healthLevels = []
    healthLevels.append(hitPoints.copy())
    
    newAction = ''
    while (hitPoints[0]>0) and (hitPoints[1]>0):
        turnCounter += 1
        r = random()
        if(isPlayer0Turn):
            newAction = userInput(hitPoints)
            if(newAction == 'H' and hitPoints[0] <= 25):
                hitPoints[0] += 4
                if(hitPoints[0] > 25):
                    hitPoints[0] = 25
            else:
                hitPoints[1] -= 5
        else:
            if(r<.5):
                newAction = 'A'
            else:
                newAction = 'H'
            if(newAction == 'H' and hitPoints[1] <= 25):
                hitPoints[1] += 4
                if(hitPoints[1] > 25):
                    hitPoints[1] = 25
            else:
                hitPoints[0] -= 5
        isPlayer0Turn = not isPlayer0Turn
        healthLevels.append(hitPoints.copy())
    output = [hitPoints[0], hitPoints[1], turnCounter, agressiveness]
#    writeGame(output, healthLevels)

def writeGame(output, healthLevels):
    for i in healthLevels:
        output.append(i)
    # output.append('x')
    line = ','.join(str(x) for x in output)
    with open('gameSims3.csv', 'a') as file:
        file.write(line)
        file.write('\n')

def userInput(hitPoints):
    print("----------------------------------")
    print("Player 1: ", hitPoints[0])
    print("Player 2: ", hitPoints[1])
    action = input("Type A to attack, H to heal: ")
    action = action.upper()
    return action

gameLoop()

