# Chopsticks Game built like TicTacToe in Python Deep Learning Book

"""Full code for running a game of Chopsticks, using the basic rules.
Two players start with one finger on each hand. The first player to move adds one of his hands to one of the other
player's hands.  Then the second player adds one of his hands to the first players hands.  The first player to have
both hands with 5 fingers on them loses. The game state will be represented by a 1x4 tuple with the first and second
numbers being Player 1's hands and the third and fourth numbers being Player 2's hands. Player 1 = 1 ; Player 2 = -1"""

import random
import itertools

def _new_hands():
    """Return a beginning gamestate

    Returns:
        1x4 tuple of ints
    """
    return((1,1,1,1,1))

def apply_move(game_state, move, side):
    """Returns a copy of the given game state with the given move applied"""

    if side == 1:
        if move == 1:
            return((game_state[0], game_state[1], (game_state[2] + game_state[0]) % 5, game_state[3], -side))
        elif move == 2:
            return((game_state[0], game_state[1], game_state[2], (game_state[3] + game_state[0]) % 5, -side))
        elif move == 3:
            return((game_state[0], game_state[1], (game_state[2] + game_state[1]) % 5, game_state[3], -side))
        elif move == 4:
            return((game_state[0], game_state[1], game_state[2], (game_state[3] + game_state[1]) % 5, -side))
    elif side == -1:
        if move == 1:
            return(((game_state[0] + game_state[2]) % 5, game_state[1], game_state[2], game_state[3], -side))
        elif move == 2:
            return((game_state[0], (game_state[1] + game_state[2]) % 5, game_state[2], game_state[3], -side))
        elif move == 3:
            return(((game_state[0] + game_state[3]) % 5, game_state[1], game_state[2], game_state[3], -side))
        elif move == 4:
            return((game_state[0], (game_state[1] + game_state[3]) % 5, game_state[2], game_state[3], -side))

def available_moves(game_state):
    """Returns a tuple of all the possible legal moves"""

    temp_moves = []

    if game_state[4] == 1:
        if game_state[0] != 0:
            if game_state[2] != 0:
                temp_moves.append(1)
        if game_state[0] != 0:
            if game_state[3] != 0:
                temp_moves.append(2)
        if game_state[1] != 0:
            if game_state[2] != 0:
                temp_moves.append(3)
        if game_state[1] != 0:
            if game_state[3] != 0:
                temp_moves.append(4)
    if game_state[4] == -1:
        if game_state[2] != 0:
            if game_state[0] != 0:
                temp_moves.append(1)
        if game_state[2] != 0:
            if game_state[1] != 0:
                temp_moves.append(2)
        if game_state[3] != 0:
            if game_state[0] != 0:
                temp_moves.append(3)
        if game_state[3] != 0:
            if game_state[1] != 0:
                temp_moves.append(4)

    return(tuple(temp_moves))

def has_winner(game_state):
    """Determine if a player has won in the given game state"""

    if game_state[0] == 0 == game_state[1]:
        return(-1)
    if game_state[2] == 0 == game_state[3]:
        return(1)

    return(0)

def play_game(plus_player_func, minus_player_func, log=False):
    """Run a single game of Chopsticks until the end"""

    game_state = _new_hands()
    player_turn = 1
    i = 1
    while True:
        i += 1
        if i > 100:
            return 0
        _available_moves = available_moves(game_state)

        if len(_available_moves) == 0:
            if log:
                print("No legal moves, someone must have won")
            #return 0
        if player_turn > 0:
            move = plus_player_func(game_state, 1)
        else:
            move = minus_player_func(game_state, -1)

        if move not in _available_moves:
            # if a player makes an invalid move the other player wins
            if log:
                print("illegal move ", move)
            return -player_turn

        game_state = apply_move(game_state, move, player_turn)
        if log:
            print(game_state)

        winner = has_winner(game_state)
        if winner != 0:
            if log:
                print("We have a winner, side: %s" % player_turn)
            return winner
        player_turn = -player_turn

def random_player(game_state, _):
    """A player func that can be used in play_game method. Given a game state it chooses a move randomly from
    the valid moves in the current state."""

    moves = available_moves(game_state)
    return random.choice(moves)


if __name__ == '__main__':
    play_game(random_player, random_player, log=True)


#game = _new_hands()
#
#game1 = apply_move(game, 1, 1)
#
#print(game1)
