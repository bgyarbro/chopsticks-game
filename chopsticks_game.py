import random
import itertools
import collections


def new_board():
    """This function returns a new starting board,
    with hands 1 1 1 1."""
    return ((1,1),
            (1,1))

def apply_move(board_state, move, side):
    """This function takes a move and side which turn it is to play
    and applies it to a given board state and returns the resulting
    board state. move = 1,2,3,or 4 meaning RR, RL, LR, LL"""

    state_list = list(list(s) for s in board_state)
    if side == 1:
        hand_to_move = state_list[0]
        hand_other = state_list[1]
    if side == -1:
        hand_to_move = state_list[1]
        hand_other = state_list[0]
    if move == (1,0):
        hand_other[0] = ( hand_other[0] + hand_to_move[0] ) % 5
    if move == (2,0):
        hand_other[1] = ( hand_other[1] + hand_to_move[0] ) % 5
    if move == (3,0):
        hand_other[0] = ( hand_other[0] + hand_to_move[1] ) % 5
    if move == (4,0):
        hand_other[1] = ( hand_other[1] + hand_to_move[1] ) % 5
    if side == 1:
        new_state_list = [hand_to_move, hand_other]
    if side == -1:
        new_state_list = [hand_other, hand_to_move]

    return tuple(tuple(s) for s in new_state_list)


def available_moves(board_state, side):
    """This function returns all the available moves for a
    given player. Not sure if this should return a list or
    use the yield keyword. And if using yield, should it 
    yield a tuple?"""

    if side == 1:
        if board_state[0][0] != 0:
            if board_state[1][0] != 0:
                yield (1,0)
        if board_state[0][0] != 0:
            if board_state[1][1] != 0:
                yield (2,0)
        if board_state[0][1] != 0:
            if board_state[1][0] != 0:
                yield (3,0)
        if board_state[0][1] != 0:
            if board_state[1][1] != 0:
                yield (4,0)
    if side == -1:  
        if board_state[1][0] != 0:
            if board_state[0][0] != 0:
                yield (1,0)
        if board_state[1][0] != 0:
            if board_state[0][1] != 0:
                yield (2,0)
        if board_state[1][1] != 0:
            if board_state[0][0] != 0:
                yield (3,0)
        if board_state[1][1] != 0:
            if board_state[0][1] != 0:
                yield (4,0)


def has_winner(board_state):
    """"""

    state_list = list(list(s) for s in board_state)
    if (state_list[0][0] == 0 and state_list[0][1] == 0):
        return -1
    if (state_list[1][0] == 0 and state_list[1][1] == 0):
        return 1
    else:
        return 0 # no one has won


def play_game(plus_player_func, minus_player_func):


    board_state = new_board()

    player_turn = 1

    while True:
        
        _available_moves = list(available_moves(board_state, player_turn))
        if not _available_moves:
            print("you broke it, no moves left")
            return 0

        if player_turn > 0:
            move = plus_player_func(board_state, 1, 100)[1]
            #move = tuple(int(x.strip()) for x in input("Make your move " ).split(','))
        else:
            move = minus_player_func(board_state, -1, 100)[1]

        if move not in _available_moves:
            # if a player makes an invalid move the other player wins
            print("illergal move, yer other player wins")
            return -player_turn

        board_state = apply_move(board_state, move, player_turn)
        print("Player " + str(player_turn) + " to move")
        print("plays " + str(move))
        print(board_state)

        winner = has_winner(board_state)

        if winner != 0:
            print("we have a winner: side %s" % player_turn)
            return winner
        player_turn = -player_turn


def random_player(board_state, side):
    moves = list(available_moves(board_state, side))
    return random.choice(moves)


#play_game(random_player, random_player)

#x = []

#def getx(x):
#    for i in x:
#        yield i

#if getx(x):
#    print("success")

#print(list(getx(x)))
