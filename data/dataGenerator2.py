# Nicholas Czaban
# The following functions run a game with randomly-generated actions. The two possible actions
# are healing and attacking. Both players begin with 25 hit points. An attack removes 5 hit points,
# and healing restores 4 hit points. The first player has a 50-50 chance of either action. The second
# player has a randomly generated "agressiveness" value, determining how likely they are to heal.
from random import random

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
    for i in healthLevels:
        output.append(i)
    # output.append('x')
    line = ','.join(str(x) for x in output)
#    print(line)
    with open('gameSims2.csv', 'a') as file:
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

