import random

from .board import *
from .board import _check_length
from .consts import *
from .exception import *


# Lights Out Generator
class Generator:

    __height : int
    __width  : int   
    __board  : Board

    def __init__(self, height: int, width: int, random_seed: int | None = None) -> None:

        _check_length(height, "height")
        _check_length(width, "width")

        self.__height = height
        self.__width  = width
        
        self.reset_seed(random_seed)
        self.regenerate()

    def reset_seed(self, random_seed: int | None = None) -> None:
        self.__rng = random.Random(random_seed)

    def regenerate(self) -> None:

        height = self.__height
        width  = self.__width

        size = height * width
        done = False

        while not done:

            board = Board(height, width)
            times = self.__rng.randint(1, size)

            for _ in range(times):
                r = self.__rng.randint(0, height - 1)
                c = self.__rng.randint(0, width - 1)
                board.press(r, c)

            # avoid turning off all the lights.
            if not board.is_all_off():
                done = True

        self.__board = board

    def get_puzzle(self) -> Board:
        return self.__board.copy()