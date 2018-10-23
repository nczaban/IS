# Nicholas Czaban
# The following functions run a game with randomly-generated actions. The two possible actions
# are healing and attacking. Both players begin with 25 hit points. An attack removes 5 hit points,
# and healing restores 4 hit points.
from random import random

def gameLoop():
    hitPoints = [25, 25]
    turnCounter = 0
    isPlayer0Turn = True
    player0Actions = []
    player1Actions = []
    newAction = ''
    while (hitPoints[0]>0) and (hitPoints[1]>0):
        turnCounter += 1
        if(random()>0.5):
            newAction = 'A'
        else:
            newAction = 'H'
        if(isPlayer0Turn):
            if(newAction == 'H'):
                hitPoints[0] += 4
                if(hitPoints[0] > 25):
                    hitPoints[0] = 25
            else:
                hitPoints[1] -= 5
            player0Actions.append(newAction)
        else:
            if(newAction == 'H'):
                hitPoints[1] += 4
                if(hitPoints[1] > 25):
                    hitPoints[1] = 25
            else:
                hitPoints[0] -= 5
            player1Actions.append(newAction)
        isPlayer0Turn = not isPlayer0Turn
    output = [hitPoints[0], hitPoints[1], turnCounter]
    for i in player0Actions:
        output.append(i)
    output.append('x')
    for i in player1Actions:
        output.append(i)
    line = ','.join(str(x) for x in output)
#    print(line)
    with open('gameSims.csv', 'a') as file:
        file.write(line)
        file.write('\n')

for x in range(500):
    gameLoop()

