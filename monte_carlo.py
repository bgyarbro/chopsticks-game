# Chopsticks Monte Carlo

import collections
import random
import math
from ChopsticksGameDeepLearning import has_winner, available_moves, apply_move


def monte_carlo_sample(game_state, side):
    """Sample a single rollout from the current game state and side."""

    result = has_winner(game_state)
    if result != 0:
        return result, None
    moves = available_moves(game_state)
    if not moves:
        return 0, None


    # select a random move
    move = random.choice(moves)
    result, next_move = monte_carlo_sample(apply_move(game_state, move, side), -side)
    return result, move


def monte_carlo_tree_search(game_state, side, number_of_samples):
    """Evaluate the best from the current game state for the given side using monte carlo sampling."""

    move_wins = collections.defaultdict(int)
    move_samples = collections.defaultdict(int)
    for _ in range(number_of_samples):
        result, move = monte_carlo_sample(game_state, side)
        # store the result and a count of the number of times we have tried this move
        if result == side:
            move_wins[move] += 1
        move_samples[move] += 1

    # get the move with the best average result
    move = max(move_wins, key=lambda x: move_wins.get(x) / move_samples[move])


    return move_wins[move] / move_samples[move], move


def _upper_confidence_bounds(payout, samples_for_this_machine, log_total_samples):
    return payout / samples_for_this_machine + math.sqrt((2 * log_total_samples) / samples_for_this_machine)


def monte_carlo_tree_search_uct(game_state, side, number_of_samples):
    """Evaluate the best from the current game state for the given side using monte carlo sampling
    with upper confidence bounds for trees"""

    state_results = collections.defaultdict(float)
    state_samples = collections.defaultdict(float)

    for _ in range(number_of_samples):
        current_side = side
        current_game_state = game_state
        first_unvisited_node = True
        rollout_path = []
        result = 0

        while result == 0:
            move_states = {move: apply_move(current_game_state, move, current_side)
                           for move in available_moves(current_game_state)}

            if not move_states:
                result = 0
                break


            if all((state in state_samples) for _, state in move_states.items()):
                log_total_samples = math.log(sum(state_samples[s] for s in move_states.values()))
                move, state = max(move_states, key=lambda _, s: _upper_confidence_bounds(state_results[s],
                                                                                         state_samples[s],
                                                                                         log_total_samples))

            else:
                move = random.choice(list(move_states.keys()))

            current_game_state = move_states[move]

            if first_unvisited_node:
                rollout_path.append((current_game_state, current_side))
                if current_game_state not in state_samples:
                    first_unvisited_node = False

            current_side = -current_side

            result = has_winner(current_game_state)

        for path_game_state, path_side in rollout_path:
            state_samples[path_game_state] += 1.
            result *= path_side
            # normalize the results to be between 0 and 1 before this it between -1 and 1
            result /= 2
            result += .5
            state_results[path_game_state] += result

    move_states = {move: apply_move(game_state, move, side) for move in available_moves(game_state)}

    move = max(move_states, key=lambda x: state_results[move_states[x]] / state_samples[move_states[x]])

    return state_results[move_states[move]] / state_samples[move_states[move]], move


if __name__ == '__main__':
    game_state = (1,1,1,1,1)

    print(monte_carlo_tree_search_uct(game_state, -1, 1000))
