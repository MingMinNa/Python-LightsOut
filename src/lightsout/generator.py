import random
from .consts    import *
from .board     import *
from .exception import *


# Lights Out Generator
class Generator:

    __length: int   # the side length of grid
    __board : Board

    def __init__(self, length: int, random_seed: int | None = None) -> None:

        check_length(length)

        self.__length = length
        self.reset_seed(random_seed)
        self.regenerate()

    def reset_seed(self, random_seed: int | None = None) -> None:
        self.__rng = random.Random(random_seed)

    def regenerate(self) -> None:

        length = self.__length
        size   = length * length
        done   = False

        while not done:

            board = Board(length)
            times = self.__rng.randint(1, size)

            for _ in range(times):
                r = self.__rng.randint(0, length - 1)
                c = self.__rng.randint(0, length - 1)
                board.press(r, c)

            # avoid turning off all the lights.
            if not board.is_all_off():
                done = True

        self.__board = board

    def get_puzzle(self) -> Board:
        return self.__board.copy()