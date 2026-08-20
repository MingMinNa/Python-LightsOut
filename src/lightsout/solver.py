from copy       import deepcopy
from .board     import Board, Position, calc_index
from .consts    import *
from .exception import *


# Lights Out Solver
class Solver:

    def __init__(self, board: Board):

        if not isinstance(board, Board):
            raise TypeError(
                f"the board must be an instance of {Board.__name__}, "
                f"got {type(board).__name__}"
            )

        self.__board  = board.copy()
        self.__length = self.__board.get_length()
        self.__grid   = self.__board.get_grid()

    def solve(self) -> tuple[Position]:

        matrix = self.__build_matrix()
        reduced = self.__forward_elimination(matrix)

        if not self.__is_consistent(reduced):
            raise UnsolvablePuzzle

        length = self.__length
        size   = length * length
        solution = [False] * size

        for row in reduced:
            coeffs = row & ((1 << size) - 1)
            if coeffs == 0:
                continue
            pivot_col = (coeffs & -coeffs).bit_length() - 1
            solution[pivot_col] = bool((row >> size) & 1)

        pressed = tuple(
            Position(i // length, i % length)
            for i in range(size) if solution[i]
        )
        return pressed

    def is_solvable(self):
        matrix = self.__build_matrix()
        reduced = self.__forward_elimination(matrix)
        return self.__is_consistent(reduced)

    # Augmented matrix 
    def __build_matrix(self) -> list[int]:

        length = self.__length
        size   = length * length
        matrix: list[int] = [0] * size

        for row in range(length):
            for col in range(length):

                index = calc_index(length, row, col)
                mask  = 1 << index
                
                for dir in Direction.get_dirs():
                    r, c = row + dir[0], col + dir[1]

                    if 0 <= r < length and 0 <= c < length:
                        mask |= 1 << calc_index(length, r, c)

                matrix[index] = mask

                if self.__grid[index] is ON:
                    matrix[index] |= 1 << size

        return matrix

    # Reduced row echelon form
    def __forward_elimination(self, matrix: list[int]) -> list[int]:

        size = len(matrix)
        rank = 0

        for col in range(size):
            pivot = None

            for row in range(rank, size):
                if (matrix[row] >> col) & 1:
                    pivot = row
                    break

            if pivot is None:
                continue

            # Swap row rank and row pivot
            matrix[rank], matrix[pivot] = \
                matrix[pivot], matrix[rank]

            for row in range(size):
                if row != rank and (matrix[row] >> col) & 1:
                    matrix[row] ^= matrix[rank]
            
            rank += 1
            
        return matrix

    def __is_consistent(self, reduced: list[int]) -> bool:

        size = len(reduced)

        for row in reduced:
            coeffs = row & ((1 << size) - 1)
            augmented = (row >> size) & 1
            if coeffs == 0 and augmented == 1:
                return False
        return True