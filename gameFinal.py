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
    player_parry_path = os.path.join('sprites', 'PlayerTest_Parry.png')
    loss_path = os.path.join('sprites', 'GameOver.png')
    win_path = os.path.join('sprites', 'Victory.png')
    menu_path = os.path.join('sprites', 'Blue.png')
    
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, screen.get_size())
    loss = pygame.image.load(loss_path).convert()
    loss = pygame.transform.scale(loss, screen.get_size())
    win = pygame.image.load(win_path).convert()
    win = pygame.transform.scale(win, screen.get_size())
    character = pygame.image.load(character_path).convert_alpha()
    character = pygame.transform.scale(character, (128, 256))
    player_parry = pygame.image.load(player_parry_path).convert_alpha()
    player_parry = pygame.transform.scale(player_parry, (128, 256))
    
    player = PlayerAvatar(1)
    enemy = PlayerAvatar(3)

    while True:
        menu_items = ['Goblin', 'Troll', 'Orc', 'Elf', 'Magician', 'Beserker', 'Knight']
        menu = Menu("Choose an Opponent", menu_path, screen_res, font_file, (350, 75))
        for item in menu_items:
            menu.add_item(item)
        display_menu = True
        ai_model = 0
        while display_menu:
            menu.show(screen)
            pygame.display.flip()
            event = pygame.event.wait()
            ai_model = menu.check_input(event)
            if ai_model == menu_items[0]:
                enemy = PlayerAvatar(1)
                enemy_path = os.path.join('sprites', 'Goblin.png')
                enemy_sprite = pygame.image.load(enemy_path).convert_alpha()
                enemy_sprite = pygame.transform.scale(enemy_sprite, (128, 256))
                guard_path = os.path.join('sprites', 'Goblin_Parry.png')
                guard_sprite = pygame.image.load(guard_path).convert_alpha()
                guard_sprite = pygame.transform.scale(guard_sprite, (128, 256))
                display_menu = False
            elif ai_model == menu_items[1]:
                enemy = PlayerAvatar(2)
                enemy_path = os.path.join('sprites', 'Troll.png')
                enemy_sprite = pygame.image.load(enemy_path).convert_alpha()
                enemy_sprite = pygame.transform.scale(enemy_sprite, (128, 256))
                display_menu = False
            elif ai_model == menu_items[2]:
                enemy = PlayerAvatar(3)
                enemy_path = os.path.join('sprites', 'Orc.png')
                enemy_sprite = pygame.image.load(enemy_path).convert_alpha()
                enemy_sprite = pygame.transform.scale(enemy_sprite, (128, 256))
                display_menu = False
            elif ai_model == menu_items[3]:
                enemy = PlayerAvatar(4)
                enemy_path = os.path.join('sprites', 'Elf.png')
                enemy_sprite = pygame.image.load(enemy_path).convert_alpha()
                enemy_sprite = pygame.transform.scale(enemy_sprite, (128, 256))
                guard_path = os.path.join('sprites', 'Elf_Parry.png')
                guard_sprite = pygame.image.load(guard_path).convert_alpha()
                guard_sprite = pygame.transform.scale(guard_sprite, (128, 256))
                display_menu = False

            elif ai_model == menu_items[4]:
                enemy = PlayerAvatar(5)
                enemy_path = os.path.join('sprites', 'Magician.png')
                enemy_sprite = pygame.image.load(enemy_path).convert_alpha()
                enemy_sprite = pygame.transform.scale(enemy_sprite, (128, 256))
                guard_path = os.path.join('sprites', 'Magician_Parry.png')
                guard_sprite = pygame.image.load(guard_path).convert_alpha()
                guard_sprite = pygame.transform.scale(guard_sprite, (128, 256))
                display_menu = False

            elif ai_model == menu_items[5]:
                enemy = PlayerAvatar(6)
                enemy_path = os.path.join('sprites', 'Beserker.png')
                enemy_sprite = pygame.image.load(enemy_path).convert_alpha()
                enemy_sprite = pygame.transform.scale(enemy_sprite, (128, 256))
                display_menu = False

            elif ai_model == menu_items[6]:
                enemy = PlayerAvatar(7)
                enemy_path = os.path.join('sprites', 'Knight.png')
                enemy_sprite = pygame.image.load(enemy_path).convert_alpha()
                enemy_sprite = pygame.transform.scale(enemy_sprite, (128, 256))
                guard_path = os.path.join('sprites', 'Knight_Parry.png')
                guard_sprite = pygame.image.load(guard_path).convert_alpha()
                guard_sprite = pygame.transform.scale(guard_sprite, (128, 256))
                display_menu = False

        game_over = False

        hitPoints = [25, 25]
        turnCounter = 0
        isPlayer0Turn = True
        healthLevels = []
        healthLevels.append(hitPoints.copy())
        actions = []
        newAction = ''

        while not game_over:
            screen.blit(background, min_coord)
            if player.isParrying:
                screen.blit(player_parry, (100, 400))
            else:
                screen.blit(character, (100, 400))

            if enemy.isParrying:
                screen.blit(guard_sprite, (500, 400))
            else:
                screen.blit(enemy_sprite, (500, 400))

            stat_string1 = "Player: " + str(hitPoints[0]) + "   "
            stat_string2 = "Enemy: " + str(hitPoints[1])
            stat_string3 = "Heal (" + str(player.healTurns) + " left)"
            menu_items = ['Attack', 'Strong Attack', 'Parry', stat_string3]
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
                    screen.blit(background, min_coord)
                    if player.isParrying:
                        screen.blit(player_parry, (100, 400))
                    else:
                        screen.blit(character, (100, 400))
                    if enemy.isParrying:
                        screen.blit(guard_sprite, (500, 400))
                    else:
                        screen.blit(enemy_sprite, (500, 400))

                    if(user_input == menu_items[3] and hitPoints[0] <= 25 and player.healTurns>0):
                        hitPoints[0] += 4
                        if(hitPoints[0] > 25):
                            hitPoints[0] = 25
                        print("Player healed")
                        actions.append('H')
                        damage = Menu("+4 HP", menu_path, (100, 100), font_file, (150, 380))
                        damage.show(screen)
                        pygame.display.flip()
                        sleep(.2)
                        player.healTurns -= 1
                        display_menu = False
                    elif(user_input == menu_items[0]):
                        actions.append('A')
                        if enemy.isParrying:
                            hitPoints[0] -= 3
                            damage = Menu("-3 HP", menu_path, (100, 100), font_file, (150, 380))
                            damage.show(screen)
                            pygame.display.flip()
                            sleep(.2)
                            print("Player attacked, but the enemy parried!")
                            print("Player lost 3 HP")
                        else:
                            hitPoints[1] -= 5
                            damage = Menu("-5 HP", menu_path, (100, 100), font_file, (550, 380))
                            damage.show(screen)
                            pygame.display.flip()
                            sleep(.2)
                            print("Player attacked")
                            print("Enemy lost 5 HP")
                        display_menu = False
                    elif(user_input == menu_items[1]):
                        r=random()
                        actions.append('S')
                        if r<.6:
                            hitPoints[1] -= 7
                            damage = Menu("-7 HP", menu_path, (100, 100), font_file, (550, 380))
                            damage.show(screen)
                            pygame.display.flip()
                            sleep(.2)
                            print("Player made a strong attack!")
                            print("Enemy lost 7 HP")
                        else:
                            damage = Menu("Miss!", menu_path, (100, 100), font_file, (550, 380))
                            damage.show(screen)
                            pygame.display.flip()
                            sleep(.2)
                            print("Player made a strong attack, but missed!")
                        display_menu = False
                    elif(user_input == menu_items[2]):
                        player.isParrying = True
                        actions.append('P')
                        print("Player is preparing to parry")
                        screen.blit(background, min_coord)
                        if player.isParrying:
                            screen.blit(player_parry, (100, 400))
                        else:
                            screen.blit(character, (100, 400))

                        if enemy.isParrying:
                            screen.blit(guard_sprite, (500, 400))
                        else:
                            screen.blit(enemy_sprite, (500, 400))
                        display_menu = False
            else:
                sleep(.5)
                enemy.isParrying = False
                newAction = enemy.helperAIFunc(hitPoints[0], player.isParrying)
                actions.append(newAction)
                if(newAction == 'H'):
                    hitPoints[1] += 4
                    if(hitPoints[1] > 25):
                        hitPoints[1] = 25
                    damage = Menu("+4 HP", menu_path, (100, 100), font_file, (550, 380))
                    damage.show(screen)
                    pygame.display.flip()
                    sleep(.7)
                    print("Enemy healed")
                    enemy.healTurns -= 1
                elif(newAction == 'A'):
                    if player.isParrying:
                        hitPoints[1] -= 3
                        damage = Menu("-3 HP", menu_path, (100, 100), font_file, (550, 380))
                        damage.show(screen)
                        pygame.display.flip()
                        sleep(.7)
                        print("Enemy attacked, but the player parried!")
                        print("Enemy lost 3 HP")
                    else:
                        hitPoints[0] -= 5
                        damage = Menu("-5 HP", menu_path, (100, 100), font_file, (150, 380))
                        damage.show(screen)
                        pygame.display.flip()
                        sleep(.7)
                        print("Enemy attacked")
                        print("Player lost 5 HP")
                elif(newAction == 'S'):
                    r=random()
                    if r<.6:
                        hitPoints[0] -= 7
                        damage = Menu("-7 HP", menu_path, (100, 100), font_file, (150, 380))
                        damage.show(screen)
                        pygame.display.flip()
                        sleep(.7)
                        print("Enemy made a strong attack")
                        print("Player lost 7 HP")
                    else:
                        damage = Menu("Miss!", menu_path, (100, 100), font_file, (150, 380))
                        damage.show(screen)
                        pygame.display.flip()
                        sleep(.7)
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
        
        if hitPoints[0]<=0:
            screen.blit(loss, min_coord)
            pygame.display.flip()
            sleep(3)
        else:
            screen.blit(win, min_coord)
            pygame.display.flip()
            sleep(3)
        player.healTurns = 2
        output = [ai_model, hitPoints, turnCounter]
#        writeGame(output, actions)


        
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
    def helperAIFunc(self, enemyHP, isParrying):
        if self.AI_MODEL == 1:
            return self.randomAI()
        elif self.AI_MODEL == 2:
            return self.aggressiveRandomAI()
        elif self.AI_MODEL == 3:
            return self.fiftyPercentAI()
        elif self.AI_MODEL == 4:
            return self.comparativeAI(enemyHP)
        elif self.AI_MODEL == 5:
            return self.scalingDifficulty(enemyHP)
        elif self.AI_MODEL == 6:
            return "A"
        elif self.AI_MODEL == 7:
            return self.parryCountering(enemyHP, isParrying)
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
        else:
            newAction = "P"
        return newAction

    # AI Model 3 - Use agressiveness statistic to determine how frequently the AI attacks.
    # If the AI is randomly chosen to heal, but has expended all healing turns, it uses a
    # strong attack instead.
    def aggressiveRandomAI(self):
        newAction = ""
        r=random()
        if r<self.aggressiveness and self.healTurns > 0:
            newAction = "H"
        elif r<self.aggressiveness:
            newAction = "S"
        else:
            newAction = "A"
        return newAction
    
    # AI Model 4 - Whenever the HP of the AI drops below 50%, the AI heals if possible. Else,
    # the AI does a normal
    def fiftyPercentAI(self):
        newAction = ""
        if (1.0*self.hp/self.maxHP < .5) and (self.healTurns > 0):
            newAction = "H"
        else:
            newAction = "A"
        return newAction

    # AI Model 5 - Whenever the HP of the AI drops below the HP of the opponent, the AI tries
    # to heal. If no heal turns remain, do a strong attack
    def comparativeAI(self, enemyHP):
        newAction = ""
        if (self.hp < enemyHP) and (self.healTurns > 0):
            newAction = "H"
        elif (self.hp < enemyHP):
            newAction = "P"
        else:
            newAction = "A"
        return newAction

    # AI Model 6 - When the AI's HP first drops below 50% of maxHP, Heal. After that, 
    # when HP drops below 50% and the AI HP is lower than the player's HP, it heals a
    # second time. If the AI is below 50% but above the player, they use Strong Attacks.
    # If the AI is below the player but has no heal turns, they Parry.
    def scalingDifficulty(self, enemyHP):
        newAction = ""
        if (1.0*self.hp/self.maxHP < .5) and (self.healTurns == 2):
            newAction = "H"
        elif (1.0*self.hp/self.maxHP >= .5):
            newAction = "A"
        elif (self.hp < enemyHP) and (self.healTurns == 1):
            newAction = "H"
        elif (self.hp >= enemyHP) and (1.0*self.hp/self.maxHP < .5):
            newAction = "S"
        elif (self.hp < enemyHP) and (self.healTurns == 0):
            newAction = "P"
        else:
            newAction = "A"
        return newAction

    # AI Model 7: When the player uses a parry, the AI uses a strong attack rather than a
    # normal attack. Otherwise, the AI uses the same decision as the scalingDifficulty AI
    # in model 6.
    def parryCountering(self, enemyHP, isParrying):
        newAction = ""
        if (isParrying == True):
            newAction = "S"
        elif (1.0*self.hp/self.maxHP < .5) and (self.healTurns == 2):
            newAction = "H"
        elif (1.0*self.hp/self.maxHP >= .5 and isParrying == False):
            newAction = "A"
        elif (self.hp < enemyHP) and (self.healTurns == 1):
            newAction = "H"
        elif (self.hp >= enemyHP) and (1.0*self.hp/self.maxHP < .5):
            newAction = "S"
        elif (self.hp < enemyHP) and (self.healTurns == 0):
            newAction = "P"
        else:
            newAction = "S"
        return newAction

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

