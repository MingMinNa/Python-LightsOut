from importlib.metadata import PackageNotFoundError, version

from .board import Board, Position
from .consts import OFF, ON
from .exception import InvalidGrid, UnsolvablePuzzle
from .generator import Generator
from .solver import Solver

__all__ = [
    "OFF",
    "ON",
    "Board",
    "Generator",
    "InvalidGrid",
    "Position",
    "Solver",
    "UnsolvablePuzzle"
]

try:
    __version__ = version("python-lightsout")
except PackageNotFoundError:
    __version__ = "0.0.0"