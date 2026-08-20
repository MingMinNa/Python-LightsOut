from __future__ import annotations

from collections.abc import Sequence
from copy import deepcopy
from typing import NamedTuple

from .consts import *
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

        check_length(length)

        if grid is None:
            grid = [OFF] * length * length

        check_grid(length, grid)

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
            raise InvalidGrid(
                f"the data type of grid_2d must be list or tuple, "
                f"got {type(grid_2d).__name__}"
            )
 
        length = len(grid_2d)
        grid: Grid = []
 
        for row in grid_2d:

            if not isinstance(row, Sequence) or len(row) != length:
                raise InvalidGrid(
                    f"the data type or the size of row doesn't match, "
                    f"got {type(row).__name__}, {row}"
                )
 
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

        if type(row) is not int or type(col) is not int:
            raise TypeError(
                f"the data type of row and col must be integer, "
                f"got {type(row).__name__} and {type(col).__name__}."
            )
    
        length = self.__length
        base   = calc_index(length, row, col)

        if row < 0 or row >= length or col < 0 or col >= length:
            raise IndexError(
                f"the value range of row and col must be in [{0}, {length - 1}], "
                f"got {row} and {col}."
            )

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

def check_length(length: int) -> None:
    
    if type(length) is not int:
        raise TypeError(
            f"the data type of length must be integer, "
            f"got {type(length).__name__}."
        )

    if length <= 0: 
        raise ValueError(
            f"the length must be positive, "
            f"got {length}."
        )

def check_grid(length: int, grid: Grid) -> None:

    if type(grid) is not list:
        raise InvalidGrid(
            f"the data type of grid must be {Grid}, "
            f"got {type(grid).__name__}."
        )

    if len(grid) != length * length:
        raise InvalidGrid(
            f"the size of grid doesn't match, "
            f"{len(grid)} != {length * length}"
        )

    for cell in grid:
        if type(cell) is not bool:
            raise InvalidGrid(
                f"there are cells containing invalid value, "
                f"got {cell}."
            )
    
    return True