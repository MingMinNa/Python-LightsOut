from __future__ import annotations
from copy       import deepcopy
from typing     import NamedTuple, Sequence
from .consts    import *
from .exception import *

Grid = list[bool]


class Position(NamedTuple):
    row  : int
    col  : int


class Board:

    __length: int
    __grid  : Grid

    # Magic methods

    def __init__(self, length: int, grid: Grid | None = None) -> None:

        if type(length) is not int:
            raise TypeError(
                f"the data type of length must be integer, "
                f"got {type(length).__name__}"
            )

        if length <= 0: 
            raise ValueError(
                f"the length must be positive, "
                f"got {length}"
            )

        if grid is None:
            grid = [OFF] * length * length

        if not valid_grid(length, grid):
            raise InvalidGrid

        self.__length = length
        self.__grid   = deepcopy(grid)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return NotImplemented
        return (
            self.__length == other.get_length() and 
            self.__grid   == other.get_grid()
        )

    def __repr__(self) -> str:
        return f"Board(length={self.__length}, grid={self.__grid})"

    def __str__(self) -> str:
    
        length = self.__length
        grid   = self.__grid
 
        col_width = len(str(length - 1)) + 1
        row_label_width = len(str(length - 1))

        header = " " * (row_label_width + 1) + "".join(
            f"{c:>{col_width}}" for c in range(length)
        )
 
        lines = [header]
 
        for r in range(length):
            row_cells = []

            for c in range(length):
                index = calc_index(length, r, c)
                cell_char = ON_CHAR if grid[index] is ON else OFF_CHAR
                row_cells.append(f"{cell_char:>{col_width}}")

            lines.append(f"{r:>{row_label_width}} " + "".join(row_cells))
 
        return "\n".join(lines)

    # Class methods

    @classmethod
    def from_2d_grid(cls, grid_2d: Sequence[Sequence[bool]]) -> Board:
 
        if not isinstance(grid_2d, Sequence):
            raise InvalidGrid
 
        length = len(grid_2d)
        grid: Grid = []
 
        for row in grid_2d:

            if not isinstance(row, Sequence) or len(row) != length:
                raise InvalidGrid
 
            grid.extend(row)
 
        return cls(length, grid)

    # Getters

    def get_grid(self) -> Grid:
        return self.__grid

    def get_length(self) -> int:
        return self.__length

    def is_all_off(self) -> bool:
        for cell in self.__grid:
            if cell is not OFF:
                return False
        return True 

    def press(self, row: int, col: int) -> None:
    
        length = self.__length
        size   = length * length
        base   = calc_index(length, row, col)

        if base >= size:
            raise IndexError

        self.__grid[base] = bool(not self.__grid[base])

        for dir in Direction.get_dirs():
            r, c = row + dir[0], col + dir[1]

            if 0 <= r < length and 0 <= c < length:
                index = calc_index(length, r, c)
                self.__grid[index] = bool(not self.__grid[index])

    def copy(self) -> Board:
        return Board(
            self.__length, 
            self.__grid
        )


# Helper functions

def calc_index(length: int, row: int, col: int) -> int:
    return row * length + col

def valid_grid(length: int, grid: Grid) -> bool:

    if type(grid) is not list:
        return False

    if len(grid) != length * length:
        return False

    for cell in grid:
        if type(cell) is not bool:
            return False
    
    return True