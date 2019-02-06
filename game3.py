# Nicholas Czaban
# The following functions run a game with randomly-generated actions. The two possible actions
# are healing and attacking. Both players begin with 25 hit points. An attack removes 5 hit points,
# and healing restores 4 hit points. The first player has a 50-50 chance of either action. The second
# player has a randomly generated "agressiveness" value, determining how likely they are to heal.
from random import random
import os, sys
import pygame

from time import sleep
from menu import Menu

# ------------------------------------------
# Functions from the pygame tutorial
# ------------------------------------------
if not pygame.font: print("Fonts are unavailable and have been disabled")
if not pygame.mixer: print("Sounds are unavailable and have been disabled")

font_file = 'SadanaSquare.ttf'

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
    character_path = os.path.join('sprites', 'PlayerTest.png')
    ending_path = os.path.join('sprites', 'GameOver.png')
    menu_path = os.path.join('sprites', 'Blue.png')
    
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, screen.get_size())
    ending = pygame.image.load(ending_path).convert()
    ending = pygame.transform.scale(ending, screen.get_size())
    character = pygame.image.load(character_path).convert_alpha()
    character = pygame.transform.scale(character, (128, 256))
    
    hitPoints = [25, 25]
    turnCounter = 0
    isPlayer0Turn = True
    agressiveness = random()
    healthLevels = []
    healthLevels.append(hitPoints.copy())
    newAction = ''

    menu_items = ['Attack', 'Heal']
    ability = Menu('Abilities', menu_path, (160, 100), font_file, (75, 75))
    for item in menu_items:
        ability.add_item(item)

    player = PlayerAvatar(1)
    enemy = PlayerAvatar(1)
    while True:
        screen.blit(background, min_coord)
        screen.blit(character, (300, 400))
        game_over = False
        while not game_over:
            stat_string1 = "Player 1: " + str(hitPoints[0]) + "   "
            stat_string2 = "Player 2: " + str(hitPoints[1])
            if player.healTurns > 0:
                menu_items = ['Attack', 'Strong Attack', 'Parry', 'Heal']
            else:
                menu_items = ['Attack', 'Strong Attack', 'Parry']
            ability = Menu(stat_string1 + stat_string2, menu_path, (500, 350), font_file, (250, 25))
            for item in menu_items:
                ability.add_item(item)
            turnCounter += 1
            if(isPlayer0Turn):
                display_menu=True
                player.isParrying = False
                while display_menu:
                    ability.show(screen)
                    pygame.display.flip()
                    event = pygame.event.wait()
                    user_input = ability.check_input(event)
                    if(user_input == menu_items[3] and hitPoints[0] <= 25):
                        hitPoints[0] += 4
                        if(hitPoints[0] > 25):
                            hitPoints[0] = 25
                        print("Player healed")
                        display_menu = False
                    elif(user_input == menu_items[0]):
                        if enemy.isParrying:
                            hitPoints[0] -= 3
                            print("Player attacked, but the enemy parried!")
                            print("Player lost 3 HP")
                        else:
                            hitPoints[1] -= 5
                            print("Player attacked")
                            print("Enemy lost 5 HP")
                        display_menu = False
                    elif(user_input == menu_items[1]):
                        r=random()
                        if r<.7:
                            hitPoints[1] -= 7
                            print("Player made a strong attack!")
                            print("Enemy lost 7 HP")
                        else:
                            print("Player made a strong attack, but missed!")
                        display_menu = False
                    elif(user_input == menu_items[2]):
                        player.isParrying = True
                        print("Player is preparing to parry")
                        display_menu = False
                        
            else:
                sleep(.5)
                enemy.isParrying = False
                newAction = enemy.helperAIFunc(hitPoints[0])
                if(newAction == 'H'):
                    hitPoints[1] += 4
                    if(hitPoints[1] > 25):
                        hitPoints[1] = 25
                    print("Enemy healed")
                elif(newAction == 'A'):
                    if player.isParrying:
                        hitPoints[1] -= 3
                        print("Enemy attacked, but the player parried!")
                        print("Enemy lost 3 HP")
                    else:
                        hitPoints[0] -= 5
                        print("Enemy attacked")
                        print("Player lost 5 HP")
                elif(newAction == 'S'):
                    r=random()
                    if r<.7:
                        hitPoints[0] -= 7
                        print("Enemy made a strong attack")
                        print("Player lost 7 HP")
                    else:
                        print("Enemy made a strong attack, but missed!")
                elif(newAction == 'P'):
                    enemy.isParrying = True
                    print("Enemy is preparing to parry")
            isPlayer0Turn = not isPlayer0Turn
            healthLevels.append(hitPoints.copy())

            player.hp = hitPoints[0]
            enemy.hp = hitPoints[1]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_over = True
            if hitPoints[0]<1 or hitPoints[1]<1:
                game_over = True
            pygame.display.flip()
        break
    screen.blit(ending, min_coord)
    pygame.display.flip()
    sleep(3)
    output = [hitPoints[0], hitPoints[1], turnCounter, agressiveness]

        
class PlayerAvatar:
    def __init__(self, model):
        self.hp = 25
        self.maxHP = 25
        self.healTurns = 2
        self.isParrying = False
        self.aggressiveness = .25
        self.AI_MODEL = model

    # AI Helper Function - Picks the appropriate function to call, and passes the correct
    # information
    def helperAIFunc(self, enemyHP):
        if self.AI_MODEL == 1:
            return self.randomAI()
        elif self.AI_MODEL == 2:
            return self.aggressiveRandomAI()
        elif self.AI_MODEL == 3:
            return self.fiftyPercentAI()
        elif self.AI_MODEL == 4:
            return self.comparitiveAI(enemyHP)
        else:
            return self.limitedRandomAI()
            
    # AI Model 1 - Ramdonly choose to attack or heal. If no heal turns remain, the AI does a
    # normal attack
    def limitedRandomAI(self):
        newAction = ""
        r=random()
        if r<.5 and self.healTurns > 0:
            newAction = "H"
        else:
            newAction = "A"
        return newAction
    
    # AI Model 2 - Randomly choose between 4 actions: Attack, Strong Attack, Parry, and Heal.
    # If no heal turns remain, the AI does a normal attack
    def randomAI(self):
        newAction = ""
        r=random()
        if(r<.25 and self.healTurns > 0):
            newAction = "H"
        elif(r<.5):
            newAction = "A"
        elif(r<.75):
            newAction = "S"
        elif():
            newAction = "P"
        return newAction

    # AI Model 3 - Use agressiveness statistic to determine how frequently the AI attacks.
    # Only the basic attack is available in this model.
    def aggressiveRandomAI(self):
        newAction = ""
        r=random()
        if r<self.aggressiveness and self.healTurns > 0:
            newAction = "H"
        else:
            newAction = "A"
        return newAction

    # AI Model 4 - Whenever the HP of the AI drops below 50%, the AI heals if possible.
    def fiftyPercentAI(self):
        newAction = ""
        if (1.0*self.hp/self.maxHP < .5) and (self.healTurns > 0):
            newAction = "H"
        else:
            newAction = "A"

    # AI Model 5 - Whenever the HP of the AI drops below the HP of the opponent, 
            
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
