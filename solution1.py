# Brad Yarbro
# Chopsticks - Basic Rules Solution

import numpy as np

# game states round n end # losing states because it is Player 2 to move
gs_Round_N_End = np.asarray([[0,1,0,0],
                             [0,2,0,0],
                             [0,3,0,0],
                             [0,4,0,0],
                             [1,0,0,0],
                             [1,1,0,0],
                             [1,2,0,0],
                             [1,3,0,0],
                             [1,4,0,0],
                             [2,0,0,0],
                             [2,1,0,0],
                             [2,2,0,0],
                             [2,3,0,0],
                             [2,4,0,0],
                             [3,0,0,0],
                             [3,1,0,0],
                             [3,2,0,0],
                             [3,3,0,0],
                             [3,4,0,0],
                             [4,0,0,0],
                             [4,1,0,0],
                             [4,2,0,0],
                             [4,3,0,0],
                             [4,4,0,0]])

print("Number of possible end states in round N")
print(len(gs_Round_N_End))
print()

z = np.asarray([4,4,0,0])

print((gs_Round_N_End == z).all(1).any())


# Function to find all possible winning states in the previous round
def findWinningStates(losing):
    winning = []
    for hands in losing :
        if hands[0] != 0 :
            winning.append([hands[0],hands[1],(hands[2] - hands[0]) % 5,hands[3]]) # possible modulo math to make it more general
            winning.append([hands[0],hands[1],hands[2],(hands[3] - hands[0]) % 5])
        if hands[1] != 0 :
            winning.append([hands[0],hands[1],(hands[2] - hands[1]) % 5,hands[3]]) # possible modulo math to make it more general
            winning.append([hands[0],hands[1],hands[2],(hands[3] - hands[1]) % 5])

    return winning

# to find the losing states I need to find all the possible previous states, then find the ones that all the possible moves result in losing states

def findLosingStates(winning, allWinning):
    possible = []
    losing = []
    for hands in winning :
        if hands[2] != 0 :
            possible.append([(hands[0] - hands[2]) % 5,hands[1],hands[2],hands[3]]) # possible modulo math to make it more general
            possible.append([hands[0],(hands[1] - hands[2]) % 5,hands[2],hands[3]])
        if hands[3] != 0 :
            possible.append([(hands[0] - hands[3]) % 5,hands[1],hands[2],hands[3]]) # possible modulo math to make it more general
            possible.append([hands[0],(hands[1] - hands[3]) % 5,hands[2],hands[3]])

    for hands in possible :
        ll = []
        lr = []
        rl = []
        rr = []
        LL = True
        LR = True
        RL = True
        RR = True
        # find all moves from the previous possible hands
        if hands[2] != 0 :
            ll = [(hands[0] + hands[2]) % 5, hands[1], hands[2], hands[3]]
            lr = [hands[0], (hands[1] + hands[2]) % 5, hands[2], hands[3]]
        if hands[3] != 0 :
            rl = [(hands[0] + hands[3]) % 5, hands[1], hands[2], hands[3]]
            rr = [hands[0], (hands[1] + hands[3]) % 5, hands[2], hands[3]]
        # check to see if at least one move is not in allWinning
            # if at least one is not in allWinning, then the hands is not in losing
            # if all handss in allWinning then the append hands to losing
        ll = np.asarray(ll)
        lr = np.asarray(lr)
        rl = np.asarray(rl)
        rr = np.asarray(rr)
        if len(ll) > 0 :
            LL = (allWinning == ll).all(1).any()
        if len(lr) > 0 :
            LR = (allWinning == lr).all(1).any()
        if len(rl) > 0 :
            RL = (allWinning == rl).all(1).any()
        if len(rr) > 0 :
            RR = (allWinning == rr).all(1).any()
        if (LL & LR & RL & RR) :
            losing.append(hands)

    return losing


print((0 - 1) % 5)


# even number is winning; odd is losing

roundNminus1 = findWinningStates(gs_Round_N_End)
#print(roundNminus1) #test

allWinning = np.asarray(roundNminus1)

roundNminus2 = findLosingStates(roundNminus1, allWinning)
#print(roundNminus2)

roundNminus3 = findWinningStates(roundNminus2)
rNminus3 = np.asarray(roundNminus3)

allWinning = np.concatenate((allWinning, rNminus3))

roundNminus4 = findLosingStates(roundNminus3, allWinning)

print(roundNminus4)
