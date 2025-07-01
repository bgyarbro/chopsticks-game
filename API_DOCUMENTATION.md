# Chopsticks Game - API Documentation

## Overview

The Chopsticks game is a Python implementation of the traditional hand game using reinforcement learning techniques. This project includes game logic, Monte Carlo search algorithms, and neural network implementations for AI players.

## Table of Contents

1. [Core Game Module (`chopsticks_game.py`)](#core-game-module)
2. [Monte Carlo Module (`monte_carlo.py`)](#monte-carlo-module)
3. [Game Runner (`play_game.py`)](#game-runner)
4. [Jupyter Notebooks](#jupyter-notebooks)

---

## Core Game Module

The `chopsticks_game.py` module contains the fundamental game logic and utilities.

### Game State Representation

The game state is represented as a tuple of tuples:
```python
board_state = ((player1_left, player1_right), (player2_left, player2_right))
```

Each hand can have 0-4 fingers. A hand with 0 fingers is "out" and cannot be used.

### Public Functions

#### `new_board()`

Creates a new starting board state.

**Returns:**
- `tuple`: Starting board state `((1,1), (1,1))`

**Example:**
```python
from chopsticks_game import new_board

board = new_board()
print(board)  # Output: ((1, 1), (1, 1))
```

#### `apply_move(board_state, move, side)`

Applies a move to the current board state and returns the resulting state.

**Parameters:**
- `board_state` (tuple): Current game state
- `move` (tuple): Move to apply as `(attacking_hand, 0)` where:
  - `(1,0)`: Left hand attacks opponent's left hand
  - `(2,0)`: Left hand attacks opponent's right hand  
  - `(3,0)`: Right hand attacks opponent's left hand
  - `(4,0)`: Right hand attacks opponent's right hand
- `side` (int): Player making the move (`1` for player 1, `-1` for player 2)

**Returns:**
- `tuple`: New board state after applying the move

**Example:**
```python
from chopsticks_game import new_board, apply_move

board = new_board()
# Player 1 uses left hand to attack player 2's left hand
new_board = apply_move(board, (1, 0), 1)
print(new_board)  # Output: ((1, 1), (2, 1))
```

#### `available_moves(board_state, side)`

Generator that yields all legal moves for a given player.

**Parameters:**
- `board_state` (tuple): Current game state
- `side` (int): Player to get moves for (`1` or `-1`)

**Returns:**
- `generator`: Generator yielding valid move tuples

**Example:**
```python
from chopsticks_game import new_board, available_moves

board = new_board()
moves = list(available_moves(board, 1))
print(moves)  # Output: [(1, 0), (2, 0), (3, 0), (4, 0)]
```

#### `has_winner(board_state)`

Checks if the game has ended and returns the winner.

**Parameters:**
- `board_state` (tuple): Current game state

**Returns:**
- `int`: 
  - `1` if player 1 wins
  - `-1` if player 2 wins
  - `0` if game continues

**Example:**
```python
from chopsticks_game import has_winner

# Player 2 has no fingers left
losing_board = ((1, 1), (0, 0))
winner = has_winner(losing_board)
print(winner)  # Output: 1 (player 1 wins)
```

#### `play_game(plus_player_func, minus_player_func)`

Orchestrates a complete game between two player functions.

**Parameters:**
- `plus_player_func` (function): Function for player 1 that returns `(score, move)`
- `minus_player_func` (function): Function for player 2 that returns `(score, move)`

**Returns:**
- `int`: Winner of the game (`1`, `-1`, or `0` for draw)

**Example:**
```python
from chopsticks_game import play_game, random_player

def simple_random_player(board_state, side, samples=None):
    """Wrapper for random player to match expected signature"""
    move = random_player(board_state, side)
    return (0, move)  # Return (score, move) tuple

winner = play_game(simple_random_player, simple_random_player)
print(f"Winner: {winner}")
```

#### `random_player(board_state, side)`

Simple random player implementation.

**Parameters:**
- `board_state` (tuple): Current game state
- `side` (int): Player side

**Returns:**
- `tuple`: Randomly selected move

**Example:**
```python
from chopsticks_game import new_board, random_player

board = new_board()
move = random_player(board, 1)
print(move)  # Output: Random move like (1, 0)
```

---

## Monte Carlo Module

The `monte_carlo.py` module implements Monte Carlo Tree Search algorithms for intelligent gameplay.

### Public Functions

#### `monte_carlo_sample(board_state, side)`

Performs a single Monte Carlo rollout from the current position.

**Parameters:**
- `board_state` (tuple): Current game state
- `side` (int): Player to move (`1` or `-1`)

**Returns:**
- `tuple`: `(result, first_move)` where:
  - `result`: Game outcome (`1`, `-1`, or `0`)
  - `first_move`: First move in the rollout sequence

**Example:**
```python
from monte_carlo import monte_carlo_sample
from chopsticks_game import new_board

board = new_board()
result, move = monte_carlo_sample(board, 1)
print(f"Sample result: {result}, First move: {move}")
```

#### `monte_carlo_tree_search(board_state, side, number_of_samples)`

Evaluates the best move using basic Monte Carlo sampling.

**Parameters:**
- `board_state` (tuple): Current game state
- `side` (int): Player to move (`1` or `-1`)
- `number_of_samples` (int): Number of rollouts to perform

**Returns:**
- `tuple`: `(win_rate, best_move)` where:
  - `win_rate`: Average win rate for the best move
  - `best_move`: Recommended move

**Example:**
```python
from monte_carlo import monte_carlo_tree_search
from chopsticks_game import new_board

board = new_board()
win_rate, move = monte_carlo_tree_search(board, 1, 1000)
print(f"Best move: {move}, Win rate: {win_rate}")
```

#### `monte_carlo_tree_search_uct(board_state, side, number_of_samples)`

Advanced Monte Carlo Tree Search with Upper Confidence bounds for Trees (UCT).

**Parameters:**
- `board_state` (tuple): Current game state
- `side` (int): Player to move (`1` or `-1`)
- `number_of_samples` (int): Number of simulations to run

**Returns:**
- `tuple`: `(confidence_score, best_move)` where:
  - `confidence_score`: Confidence in the best move (0-1)
  - `best_move`: Recommended move

**Example:**
```python
from monte_carlo import monte_carlo_tree_search_uct
from chopsticks_game import new_board

board = new_board()
confidence, move = monte_carlo_tree_search_uct(board, 1, 5000)
print(f"UCT Best move: {move}, Confidence: {confidence}")

# Use in a game
def uct_player(board_state, side, samples=1000):
    return monte_carlo_tree_search_uct(board_state, side, samples)

# Play against random
from chopsticks_game import play_game, random_player

def random_wrapper(board_state, side, samples=None):
    from chopsticks_game import random_player
    return (0, random_player(board_state, side))

winner = play_game(uct_player, random_wrapper)
```

---

## Game Runner

The `play_game.py` module provides a simple entry point to run games.

### Usage

```python
# Run a game between two UCT players
from play_game import *

# The script automatically runs:
# play_game(monte_carlo_tree_search_uct, monte_carlo_tree_search_uct)
```

To customize:
```python
from chopsticks_game import play_game
from monte_carlo import monte_carlo_tree_search_uct, monte_carlo_tree_search

# Play UCT vs basic Monte Carlo
winner = play_game(monte_carlo_tree_search_uct, monte_carlo_tree_search)
print(f"Winner: {winner}")
```

---

## Jupyter Notebooks

### `chopsticks_colab.ipynb`

Interactive notebook for playing and experimenting with the game.

**Key Features:**
- Complete game implementation in notebook cells
- Interactive gameplay
- Monte Carlo algorithms
- Example games and analysis

**Usage:**
1. Open in Google Colab: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bgyarbro/chopsticks/blob/master/chopsticks_colab.ipynb)
2. Run cells sequentially
3. Modify parameters and experiment

### `chopsticks_colab_nn.ipynb` 

Neural network implementation using TensorFlow for policy gradient learning.

**Key Features:**
- TensorFlow 1.x neural network implementation
- Policy gradient training
- Hyperparameter configuration
- Training loop with performance monitoring

**Neural Network Architecture:**
```python
# Hyperparameters
HIDDEN_NODES = (100, 100, 100)  # 3 hidden layers
INPUT_NODES = 4  # 2x2 board state
BATCH_SIZE = 100
LEARN_RATE = 1e-4
```

**Training Example:**
```python
# The notebook includes a complete training loop
# Monitor progress with win rate tracking
episode_number = 1
while True:
    reward = play_game(neural_net_player, random_player)
    # Training updates every BATCH_SIZE episodes
```

---

## Game Rules

### Objective
Eliminate both of your opponent's hands by reducing their finger count to zero.

### Basic Rules
1. Each player starts with 1 finger on each hand
2. Players take turns attacking opponent's hands
3. When attacking, add your attacking hand's finger count to the target hand
4. If a hand reaches 5+ fingers, it becomes 0 (modulo 5 arithmetic)
5. A hand with 0 fingers is "dead" and cannot attack or be attacked
6. First player to lose both hands loses the game

### Move Notation
- `(1,0)`: Left hand attacks opponent's left hand
- `(2,0)`: Left hand attacks opponent's right hand  
- `(3,0)`: Right hand attacks opponent's left hand
- `(4,0)`: Right hand attacks opponent's right hand

---

## Advanced Usage Examples

### Creating Custom Players

```python
def defensive_player(board_state, side, samples=1000):
    """Player that prioritizes not losing over winning"""
    moves = list(available_moves(board_state, side))
    
    # Evaluate each move
    best_move = None
    best_score = -float('inf')
    
    for move in moves:
        new_state = apply_move(board_state, move, side)
        # Simple heuristic: avoid states where opponent can win quickly
        score = evaluate_position(new_state, side)
        if score > best_score:
            best_score = score
            best_move = move
    
    return (best_score, best_move)

def evaluate_position(board_state, side):
    """Simple position evaluation"""
    if side == 1:
        my_fingers = sum(board_state[0])
        opp_fingers = sum(board_state[1])
    else:
        my_fingers = sum(board_state[1])
        opp_fingers = sum(board_state[0])
    
    return my_fingers - opp_fingers
```

### Tournament Play

```python
def run_tournament(players, games_per_match=100):
    """Run a round-robin tournament"""
    results = {}
    
    for i, player1 in enumerate(players):
        for j, player2 in enumerate(players):
            if i != j:
                wins = 0
                for _ in range(games_per_match):
                    winner = play_game(player1, player2)
                    if winner == 1:
                        wins += 1
                
                match_key = (player1.__name__, player2.__name__)
                results[match_key] = wins / games_per_match
    
    return results

# Example tournament
players = [random_wrapper, defensive_player, uct_player]
tournament_results = run_tournament(players, 50)
```

### Performance Analysis

```python
import time

def benchmark_player(player_func, board_state, side, iterations=100):
    """Benchmark player performance"""
    start_time = time.time()
    
    for _ in range(iterations):
        score, move = player_func(board_state, side, 1000)
    
    avg_time = (time.time() - start_time) / iterations
    print(f"{player_func.__name__}: {avg_time:.4f}s per move")

# Benchmark different algorithms
board = new_board()
benchmark_player(monte_carlo_tree_search, board, 1)
benchmark_player(monte_carlo_tree_search_uct, board, 1)
```

---

## Error Handling

The game includes basic error handling:

- **Invalid moves**: Automatically handled by `available_moves()` function
- **Game state validation**: `has_winner()` checks for terminal states
- **Player function errors**: Game awards win to opponent if player makes illegal move

### Best Practices

1. **Always validate moves** using `available_moves()` before applying
2. **Check for game end** with `has_winner()` after each move
3. **Handle timeouts** in AI players for real-time play
4. **Use appropriate sample sizes** for Monte Carlo methods (1000-10000)

---

## Dependencies

- `random`: For random number generation
- `itertools`: For combination utilities  
- `collections`: For defaultdict in Monte Carlo algorithms
- `math`: For mathematical operations in UCT
- `numpy`: For neural network implementation (notebooks only)
- `tensorflow`: For neural network training (notebooks only)

## Installation

```bash
# Clone repository
git clone https://github.com/bgyarbro/chopsticks.git
cd chopsticks

# No additional dependencies needed for basic game
python play_game.py

# For neural network notebooks:
pip install tensorflow numpy jupyter
```

This documentation covers all public APIs and provides comprehensive examples for using the Chopsticks game implementation.