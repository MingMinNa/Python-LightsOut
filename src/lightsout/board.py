from __future__ import annotations

from collections.abc import Sequence
from copy import deepcopy
from typing import NamedTuple

from .consts import *
from .exception import *

Grid = list[bool]

class Position(NamedTuple):
    row : int
    col : int


class Board:

    __height : int
    __width  : int
    __grid   : Grid

    # Magic methods

    def __init__(self, height: int, width: int, grid: Grid | None = None) -> None:

        _check_length(height, "height")
        _check_length(width, "width")

        if grid is None:
            grid = [OFF] * height * width

        _check_grid(height, width, grid)

        self.__height = height
        self.__width  = width
        self.__grid   = deepcopy(grid)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return NotImplemented
        return (
            self.__height == other.get_height() and 
            self.__width  == other.get_width() and 
            self.__grid   == other.get_grid()
        )

    def __repr__(self) -> str:
        return f"Board(height={self.__height}, width={self.__width}, grid={self.__grid})"

    def __str__(self) -> str:
    
        height = self.__height
        width  = self.__width
        grid   = self.__grid
 
        col_width = len(str(width - 1)) + 1
        row_label_width = len(str(height - 1))

        header = " " * (row_label_width + 1) + "".join(
            f"{c:>{col_width}}" for c in range(width)
        )
 
        lines = [header]
 
        for r in range(height):
            row_cells = []

            for c in range(width):
                index = calc_index(width, r, c)
                cell_char = ON_CHAR if grid[index] is ON else OFF_CHAR
                row_cells.append(f"{cell_char:>{col_width}}")

            lines.append(f"{r:>{row_label_width}} " + "".join(row_cells))
 
        return "\n".join(lines)

    # Class methods

    @classmethod
    def from_2d_grid(cls, grid_2d: Sequence[Sequence[bool]]) -> Board:
 
        if type(grid_2d) not in (list, tuple):
            raise InvalidGrid(
                f"the data type of grid_2d must be list or tuple, "
                f"got {type(grid_2d).__name__}"
            )

        width  = -1
        height = len(grid_2d)
        grid: Grid = []
 
        for row in grid_2d:

            if type(row) not in (list, tuple) or (width >= 0 and len(row) != width):
                raise InvalidGrid(
                    f"the data type or the size of row doesn't match, "
                    f"got {type(row).__name__}, {row}"
                )
            
            width = len(row)
            grid.extend(row)
 
        return cls(height, width, grid)

    # Getters

    def get_grid(self) -> Grid:
        return self.__grid

    def get_height(self) -> int:
        return self.__height

    def get_width(self) -> int:
        return self.__width

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

        height = self.__height
        width  = self.__width
        base   = calc_index(width, row, col)

        if row < 0 or row >= height:
            raise IndexError(
                f"the value range of row must be in [{0}, {height - 1}], "
                f"got {row}."
            )

        if col < 0 or col >= width:
            raise IndexError(
                f"the value range of column must be in [{0}, {width - 1}], "
                f"got {col}."
            )

        self.__grid[base] = bool(not self.__grid[base])

        for dir in Direction.get_dirs():
            r, c = row + dir[0], col + dir[1]

            if 0 <= r < height and 0 <= c < width:
                index = calc_index(width, r, c)
                self.__grid[index] = bool(not self.__grid[index])

    def copy(self) -> Board:
        return Board(
            self.__height,
            self.__width, 
            self.__grid
        )


# Helper functions

def calc_index(width: int, row: int, col: int) -> int:
    return row * width + col

def _check_length(length: int, var_name: str) -> None:
    
    if type(length) is not int:
        raise TypeError(
            f"the data type of {var_name} must be integer, "
            f"got {type(length).__name__}."
        )

    if length <= 0: 
        raise ValueError(
            f"{var_name} must be positive, "
            f"got {length}."
        )

def _check_grid(height: int, width: int, grid: Grid) -> None:

    if type(grid) is not list:
        raise InvalidGrid(
            f"the data type of grid must be {Grid}, "
            f"got {type(grid).__name__}."
        )

    if len(grid) != height * width:
        raise InvalidGrid(
            f"the size of grid doesn't match, "
            f"{len(grid)} != {height * width}"
        )

    for cell in grid:
        if type(cell) is not bool:
            raise InvalidGrid(
                f"there are cells containing invalid value, "
                f"got {cell}."
            )