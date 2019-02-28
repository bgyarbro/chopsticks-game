import numpy as np
import pandas as pd

count = 0

gamestates = []

# i: player whose turn it is to move
# j: player 0 left hand
# k: player 0 right hand
# j2: player 1 left hand
# k2: player 1 right hand

for i in range(0,2):
    for j in range(0,5):
        for k in range(0,5):
            for j2 in range(0,5):
                for k2 in range(0,5):
                    count += 1
                    #print('Gamestate ' + str(count))
                    #print('Player ' + str(i) + ' to move.')
                    #print('P1 Hands: (' + str(j) + ',' + str(k) + ')')
                    #print('P2 Hands: (' + str(j2) + ',' + str(k2) + ')')
                    gamestates.append([i,j,k,j2,k2])

print(gamestates)

#gamestates = np.asarray(gamestates)

gamestates = gamestates[1:len(gamestates)]

#print(gamestates)


endstates = []

for gs in gamestates:
    if gs[1] == 0 == gs[2]:
        endstates.append(gs)
    if gs[3] == 0 == gs[4]:
        endstates.append(gs)

print(endstates)

class GameState:
    def __init__(self, arr):
        self.pTurn = arr[0]
        self.p0Hands = arr[1:3]
        self.p1Hands = arr[3:5]

    def printState(self):
        print("Player " + str(self.pTurn) + " to move.")
        print(self.p0Hands)
        print(self.p1Hands)

    def findPreviousPossibleStates(self):



test = GameState(endstates[1])
test.printState()
