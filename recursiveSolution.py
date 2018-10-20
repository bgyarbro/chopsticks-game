import numpy as np
import pandas as pd

endStates = np.asarray([[0,0,1,0,0],
                        [0,0,2,0,0],
                        [0,0,3,0,0],
                        [0,0,4,0,0],
                        [0,1,0,0,0],
                        [0,1,1,0,0],
                        [0,1,2,0,0],
                        [0,1,3,0,0],
                        [0,1,4,0,0],
                        [0,2,0,0,0],
                        [0,2,1,0,0],
                        [0,2,2,0,0],
                        [0,2,3,0,0],
                        [0,2,4,0,0],
                        [0,3,0,0,0],
                        [0,3,1,0,0],
                        [0,3,2,0,0],
                        [0,3,3,0,0],
                        [0,3,4,0,0],
                        [0,4,0,0,0],
                        [0,4,1,0,0],
                        [0,4,2,0,0],
                        [0,4,3,0,0],
                        [0,4,4,0,0]])

#print(endStates[endStates[:,0] == 0])

def main(L, W, n):
    tempL = L[L[:,0] == 0]
    for state in tempL :
        tempHands = findPrevWinning(state)
        #if W.shape == (5,) : # if W.shape == (0,)
        #    W = np.concatenate((W, tempHands)) # W = tempHands
        if W.shape == (0,) :
            W = tempHands
        elif len(tempHands) == 1:
            if not (W == tempHands):
                W = np.concatenate((W, tempHands))
        else:
            for hands in tempHands:
                #print(hands)
                if not (W == hands).all(1).any():
                    #print("test")
                    W = np.concatenate((W, [hands]))
            #for i in range(0,len(tempHands)):
            #    if not (W == tempHands[i]).all(1).any():
            #        W = np.concatenate((W, tempHands[i]))

        #if W.any() == False:
        #    W = np.concatenate((W, tempHands))

            #for hands in tempHands :
            #    if len(hands) > 0:
            #        if (W == hands).all(1).any() == False or (W == hands) == False:
            #            W = np.concatenate((W, hands))
            #
            #if W != []:
            #    if (W == hands) == False:
            #        W = np.concatenate((W, tempHands))
            #    else (W == tempHands).all(1).any() == False:
            #        W = np.concatenate((W, tempHands))

    L[:,0] = 1 # Mark the Losing States as Checked

    #-----------------------------------------So far, so good------------------------#
    #print("This is W after the first run")
    #print(W)
    #print("L should be 1s in first column")
    #print(L)


    #print(L)

    #return 0
    #print("w3")
    #print(W[1])
    #print("test findPrevPossible")
    #print(findPrevPossible(W[1]))

    #return 0

    # now, take the Winning states that have not been checked -> tempW
    # initialize possible, loop through the states in tempW to find all Possible prev steps
    #

    # find all possible prev L from unchecked W
    tempW = W[W[:,0] == 0]
    possible = np.asarray([])
    for state in tempW :
        tempHands = findPrevPossible(state)
        if possible.shape == (0,):
            possible = tempHands
        elif len(tempHands) == 1:
            if not (possible == tempHands).all(1).any():
                possible = np.concatenate((possible, tempHands))
        else:
            for hands in tempHands :
                if not (possible == hands).all(1).any():
                    possible = np.concatenate((possible, [hands]))

    W[:,0] = 1

    #print("this is possible")
    #print(possible)
    #return 0

    confirmed = np.asarray([])
    for state in possible :
        if confirmStateIsLosing(state, W):
            if confirmed.shape == (0,):
                confirmed = np.asarray([state])
            else:
                confirmed = np.concatenate((confirmed, [state]))
        #tempHands = confirmStateIsLosing(state)
        #if tempHands :
        #    if (L == state).all(1).any() == False :
        #        L = np.concatenate((L, state))

    if len(confirmed) > 0:
        confirmed[:,0] = 0
        L = np.concatenate((L, confirmed))

    print("winning")
    print(W)
    print("losing")
    print(L)

    if (W == startingHands).all(1).any():
        print("Player 1 Wins")
    elif (L == startingHands).all(1).any():
        print("Player 2 Wins")
    elif n < 100:
        print("round " + str(n))
        main(L, W, n+1)

def findPrevWinning(hands):
    prev = []
    if hands[1] != 0 : # check if P1 left hand is zero
        if (hands[3] - hands[1]) % 5 != 0 : # check if p1 would play onto P2 left hand zero
            prev.append([0,hands[1],hands[2],(hands[3] - hands[1]) % 5,hands[4]]) # P1 Right hand play onto P2 left hand to win
        if (hands[4] - hands[1]) % 5 != 0 : # check that p2 hand was not zero
            prev.append([0,hands[1],hands[2],hands[3],(hands[4] - hands[1]) % 5]) # p1 right hand play onto p2 right hand to win
    if hands[2] != 0 : # check if p1 right hand is zero
        if (hands[3] - hands[2]) % 5 != 0 : # check that p2 hand was not zero
            prev.append([0,hands[1],hands[2],(hands[3] - hands[2]) % 5,hands[4]]) # p1 left hand play onto p2 left hand to win
        if (hands[4] - hands[2]) % 5 != 0 : # check that p2 hand was not zero
            prev.append([0,hands[1],hands[2],hands[3],(hands[4] - hands[2]) % 5]) # p1 left hand play onto p2 right hand to win
    return np.asarray(prev)


def findPrevPossible(hands):
    prev = []
    # need to switch p1 and p2
    if hands[3] != 0 : # check if P2 left hand is zero
        if (hands[1] - hands[3]) % 5 != 0 : # check if p2 would play onto P1 left hand zero
            prev.append([1,(hands[1] - hands[3]) % 5,hands[2],hands[3],hands[4]]) # P2 Right hand play onto P1 left hand
        if (hands[2] - hands[3]) % 5 != 0 : # check that p1 hand was not zero
            prev.append([1,hands[1],(hands[2] - hands[3]) % 5,hands[3],hands[4]]) #
    if hands[4] != 0 : # check if p1 right hand is zero
        if (hands[1] - hands[4]) % 5 != 0 : # check that p1 hand was not zero
            prev.append([1,(hands[1] - hands[4]) % 5,hands[2],hands[3],hands[4]]) #
        if (hands[2] - hands[4]) % 5 != 0 : # check that p1 hand was not zero
            prev.append([1,hands[1],(hands[2] - hands[4]) % 5,hands[3],hands[4]]) #
    return np.asarray(prev)


def confirmStateIsLosing(state, W):
    # take state and find all possible resulting states from p2 moves
    RR = True
    RL = True
    LR = True
    LL = True

    if state[4] != 0 and state[2] != 0:
        rr = np.asarray([[1,state[1], (state[2] + state[4]) % 5, state[3], state[4]]])
        RR = (W == rr).all(1).any()
    if state[4] != 0 and state[1] != 0:
        rl = np.asarray([[1,(state[1] + state[4]) % 5, state[2], state[3], state[4]]])
        RL = (W == rl).all(1).any()
    if state[3] != 0 and state[2] != 0:
        lr = np.asarray([[1,state[1], (state[2] + state[3]) % 5, state[3], state[4]]])
        LR = (W == lr).all(1).any()
    if state[3] != 0 and state[1] != 0:
        ll = np.asarray([[1,(state[1] + state[3]) % 5, state[2], state[3], state[4]]])
        LL = (W == ll).all(1).any()

    if RR and RL and LR and LL:
        return True
    else:
        return False



#winning = np.asarray([[1,0,0,0,0]])
winning = np.asarray([])

startingHands = np.asarray([[1,1,1,1,1]])

main(endStates, winning, 1)

#print(winning.shape)
