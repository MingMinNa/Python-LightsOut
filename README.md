# Python Lights Out

![Static Badge](https://img.shields.io/badge/Python-3.13-blue) [![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

A Python package for generating and solving Lights Out puzzles.

## Lights Out (Game)
The game consists of a 5 by 5 grid of lights.  
- When the game starts, a random number of these lights is switched on.  
- Pressing any of the lights will toggle it and the adjacent lights. 

The goal of the puzzle is to switch all the lights off, preferably with as few button presses as possible.

Source: [Wikipedia – Lights Out (game)](https://en.wikipedia.org/wiki/Lights_Out_(game))

### Example

For simplicity, use a 3×3 grid as an example.

```text 
   0 1 2                   0 1 2                   0 1 2                   0 1 2
0  . O .                0  O . O                0  . . O                0  . . .
1  O O O  —— (0, 1) —→  1  O . O  —— (1, 0) —→  1  . O O  —— (1, 2) —→  1  . . .  (complete)
2  O . O                2  O . O                2  . . O                2  . . .
```

## Installation

This package can be installed in two ways:
1. Install directly from this repository.
2. Install via PyPI.

### Install from the repository
```bash
$ git clone https://github.com/MingMinNa/Python-LightsOut.git
$ cd Python-LightsOut
$ pip install .
```

### Install via PyPI
```bash
$ pip install python-lightsout
```

Then, run the following code to verify the installation:

```python
import lightsout
print(lightsout.__version__)
```

## Usage

Here are some simple usage examples.

### Create a Board

```python
from lightsout.board import Board, ON, OFF

# Method 1: Create an empty 5x5 board with all lights off
board = Board(5)
print(board, "\n")

# You can also provide a 1D grid (size must be length * length)
board = Board(3, [
    OFF, ON , OFF,
    ON , OFF, ON ,
    OFF, ON , OFF,
])
print(board, "\n")

# Method 2: Create a board from a 2D grid.
# It will be automatically converted to an internal 1D grid.
board = Board.from_2d_grid([
    [OFF, ON , OFF],
    [ON , OFF, ON ],
    [OFF, ON , OFF],
])
print(board, "\n")

# Press the light at (row, col).
# The selected light and its adjacent lights are toggled.
board.press(1, 1)
print(board, "\n")
```

<details>
<summary>Output</summary>

```text
   0 1 2 3 4
0  . . . . .
1  . . . . .
2  . . . . .
3  . . . . .
4  . . . . . 

   0 1 2
0  . O .
1  O . O
2  . O . 

   0 1 2
0  . O .
1  O . O
2  . O . 

   0 1 2
0  . . .
1  . O .
2  . . . 
```
</details>

### Generate a puzzle

```python
from lightsout.generator import Generator

# Create a 5x5 generator.
# random_seed can be omitted if not needed.
generator = Generator(length=5, random_seed=42)

# Get the current puzzle.
# A copy is returned, so the internal state will not be affected.
puzzle = generator.get_puzzle()
print(puzzle, "\n")

# Generate a new puzzle
generator.regenerate()
puzzle = generator.get_puzzle()
print(puzzle)
```

<details>
<summary>Output</summary>

```text
   0 1 2 3 4
0  . . . . O
1  O . . O .
2  . . . O O
3  . O . O O
4  O O . O . 

   0 1 2 3 4
0  . . O O O
1  O . O . .
2  O . O . .
3  . . . . .
4  O . O . .
```
</details>

### Find a solution

```python
from lightsout import Board, Generator, Solver

puzzle = Generator(length=3).get_puzzle()
solver = Solver(puzzle)
print(puzzle, "\n")

# Check if the puzzle is solvable
if solver.is_solvable():
    solution = solver.solve()  # Returns tuple[Position]
    print("Press the following positions in order:\n")

    for pos in solution:
        print(f"Press ({pos.row}, {pos.col})")
        puzzle.press(pos.row, pos.col)
        print(puzzle, "\n")
else:
    print("This puzzle has no solution.")
```

<details>
<summary>Output</summary>

```text
   0 1 2
0  . O .
1  O . O
2  O . O 

Press the following positions in order:

Press (1, 1)
   0 1 2
0  . . .
1  . O .
2  O O O 

Press (2, 1)
   0 1 2
0  . . .
1  . . .
2  . . . 
```
</details>


### Notes
- If the puzzle is unsolvable, calling `solve()` directly will raise an `UnsolvablePuzzle` exception.
- It is recommended to call `is_solvable()` first or use `try/except`.

## References & Tools
- [Wikipedia – Lights Out (game)](https://en.wikipedia.org/wiki/Lights_Out_(game))
- [pytest-dev/pytest](https://github.com/pytest-dev/pytest)