# Nicholas Czaban
# The following functions run a game with randomly-generated actions. The two possible actions
# are healing and attacking. Both players begin with 25 hit points. An attack removes 5 hit points,
# and healing restores 4 hit points. The first player has a 50-50 chance of either action. The second
# player has a randomly generated "agressiveness" value, determining how likely they are to heal.
from random import random
import os, sys
import pygame

from time import sleep

# ----------
# Functions from the pygame tutorial
# ----------
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



# Begin my code sections
min_coord = (0, 0)
max_coord = (720, 720)
screen_res = max_coord
delay = 100 # milliseconds
interval = 50 # milliseconds

def main():
    pygame.init()
    pygame.display.set_caption("Cave Escape")
    pygame.key.set_repeat(delay, interval)
    screen = pygame.display.set_mode(screen_res)
    background_path = os.path.join('sprites', 'CaveTest.png')
    player_path = os.path.join('sprites', 'PlayerTest.png')
    ending_path = os.path.join('sprites', 'GameOver.png')
    
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, screen.get_size())
    ending = pygame.image.load(ending_path).convert()
    ending = pygame.transform.scale(ending, screen.get_size())
    player = pygame.image.load(player_path).convert_alpha()
    player = pygame.transform.scale(player, (128, 256))

    hitPoints = [25, 25]
    turnCounter = 0
    isPlayer0Turn = True
    agressiveness = random()
    healthLevels = []
    healthLevels.append(hitPoints.copy())
    newAction = ''

    while True:
        screen.blit(background, min_coord)
        screen.blit(player, (300, 400))
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_over = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    game_over = True
            pygame.display.flip()
        break
    screen.blit(ending, min_coord)
    pygame.display.flip()
    sleep(5)

class PlayerAvatar:
    def __init__(self):
        self.hp = 25
        self.healTurns = 4
        
            
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

main()
