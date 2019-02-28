# Brad Yarbro
# Chopsticks - Basic Rules Solution

import numpy as np
import pandas as pd

col_names = ['p1l', 'p1r', 'p2l', 'p2r']

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
    """ Function to find the previous round winning gamestates where P1 can make a move to put P2 in losing state """
    winning = []
    for hands in losing : # look at the losing gamestate, then see what P1 hand could have been to make P2 allLosing
    # need to add in condition to make sure p1 does not play onto p2 zero hand
        if hands[0] != 0 :
            if (hands[2] - hands[0]) % 5 != 0 :
            winning.append([hands[0],hands[1],(hands[2] - hands[0]) % 5,hands[3]]) # P1 left hand play onto P2 left hand to win
            if (hands[3] - hands[0]) % 5 != 0 :
            winning.append([hands[0],hands[1],hands[2],(hands[3] - hands[0]) % 5]) # p1 left hand play onto p2 right hand to win
        if hands[1] != 0 :
            if (hands[2] - hands[1]) % 5 != 0 :
            winning.append([hands[0],hands[1],(hands[2] - hands[1]) % 5,hands[3]]) # p1 right hand play onto p2 left hand to win
            if (hands[3] - hands[1]) % 5 != 0 :
            winning.append([hands[0],hands[1],hands[2],(hands[3] - hands[1]) % 5]) # p1 right hand play onto p2 right hand to win

#############################################
    # here convert winning to DataFrame then drop the duplicates, then convert back to an array
    winning = pd.DataFrame(winning, columns = col_names)
    winning.drop_duplicates()
    winning = np.asarray(winning)

    return winning

# to find the losing states I need to find all the possible previous states, then find the ones that all the possible moves result in losing states

def findLosingStates(winning, allWinning):
    possible = []
    losing = []
    for hands in winning :
        if hands[2] != 0 : # p2 left hand nonzero
            if (hands[0] - hands[2]) % 5 != 0 : # p1 left hand nonzero
                possible.append([(hands[0] - hands[2]) % 5,hands[1],hands[2],hands[3]]) # possible modulo math to make it more general
            if (hands[1] - hands[2]) % 5 != 0 : # p1 right hand nonzero
                possible.append([hands[0],(hands[1] - hands[2]) % 5,hands[2],hands[3]])
        if hands[3] != 0 : # p2 right hand nonzero
            if (hands[0] - hands[3]) % 5 != 0 :
                possible.append([(hands[0] - hands[3]) % 5,hands[1],hands[2],hands[3]]) # possible modulo math to make it more general
            if (hands[1] - hands[3]) % 5 != 0 :
                possible.append([hands[0],(hands[1] - hands[3]) % 5,hands[2],hands[3]])

    # convert possible to DataFrame then drop duplicates, then convert back to array
    possible = pd.DataFrame(possible, columns = col_names)
    possible.drop_duplicates()
    possible = np.asarray(possible)

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
            if hands[0] != 0 :
                ll = [(hands[0] + hands[2]) % 5, hands[1], hands[2], hands[3]]
            if hands[1] != 0 :
                lr = [hands[0], (hands[1] + hands[2]) % 5, hands[2], hands[3]]
        if hands[3] != 0 :
            if hands[0] != 0 :
                rl = [(hands[0] + hands[3]) % 5, hands[1], hands[2], hands[3]]
            if hands[1] != 0 :
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

    losing = pd.DataFrame(losing, columns = col_names)
    losing.drop_duplicates()
    losing = np.asarray(losing)

    return losing


print((0 - 1) % 5)


# even number is winning; odd is losing
allLosing = gs_Round_N_End

roundNminus1 = findWinningStates(gs_Round_N_End)
#print(roundNminus1) #test

allWinning = roundNminus1

roundNminus2 = findLosingStates(roundNminus1, allWinning)
#print(roundNminus2)

allLosing = np.concatenate((allLosing, roundNminus2))
print("allLosing after round N-2")
print(allLosing)

roundNminus3 = findWinningStates(allLosing)
allWinning = np.concatenate((allWinning, roundNminus3))
print("allWinning after round N-3")
print(allWinning)
#
#roundNminus4 = findLosingStates(allWinning, allWinning)
##print(roundNminus4)
#
#allLosing = np.concatenate((allLosing, np.asarray(roundNminus4)))
##print(allLosing)
#
#roundNminus5 = findWinningStates(allLosing)
#allWinning = np.concatenate((allWinning, np.asarray(roundNminus5)))
##print("All Winning N-5")
##print(allWinning)
#
#roundNminus6 = findLosingStates(allWinning, allWinning)
#allLosing = np.concatenate((allLosing, np.asarray(roundNminus6)))
##print("All Losing N-6")
##print(allLosing)
#
#roundNminus7 = findWinningStates(allLosing)
#allWinning = np.concatenate((allWinning, np.asarray(roundNminus7)))
##print("All Winning N-7")
##print(allWinning)
#
#roundNminus8 = findLosingStates(allWinning, allWinning)
#allLosing = np.concatenate((allLosing, np.asarray(roundNminus8)))
##print("All Winning N-8")
##print(allLosing)
#
#roundNminus9 = findWinningStates(allLosing)
#allWinning = np.concatenate((allWinning, np.asarray(roundNminus9)))
##print("All Winning N-9")
##print(allWinning)
#
#roundNminus10 = findLosingStates(allWinning, allWinning)
#allLosing = np.concatenate((allLosing, np.asarray(roundNminus10)))
##print("All Losing N-10")
##print(allLosing)
#
#roundNminus11 = findWinningStates(allLosing)
#allWinning = np.concatenate((allWinning, np.asarray(roundNminus11)))
##print("All Winning N-11")
##print(allWinning)
#
#roundNminus12 = findLosingStates(allWinning, allWinning)
#allLosing = np.concatenate((allLosing, np.asarray(roundNminus12)))
##print("All Losing N-12")
##print(allLosing)
#
##roundNminus13 = findWinningStates(allLosing)
##allWinning = np.concatenate((allWinning, np.asarray(roundNminus13)))
##print("All Winning N-13")
##print(allWinning)
##
##roundNminus14 = findLosingStates(allWinning, allWinning)
##allLosing = np.concatenate((allLosing, np.asarray(roundNminus14)))
##print("All Losing N-14")
##print(allLosing)
#
#
##########################################################
startingHands = np.asarray([1,1,1,1])

print((allWinning == startingHands).all(1).any())
print((allLosing == startingHands).all(1).any())


#roundNminus4 = findLosingStates(roundNminus3, allWinning)
#print("Losing states in round N-4")
#print(roundNminus4)

#allLosing = allLosing + roundNminus4
#print("All the losing hands after Rn-4")
#print(np.asarray(allLosing))

#roundNminus5 = findWinningStates(roundNminus4)
#print("rN-5 Winning")
#print(np.asarray(roundNminus5))
#
#print()
