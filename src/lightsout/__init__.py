from importlib.metadata import PackageNotFoundError, version
from .consts    import ON, OFF
from .board     import Position, Board
from .exception import InvalidGrid, UnsolvablePuzzle
from .generator import Generator
from .solver    import Solver

__all__ = [
    "ON", "OFF",
    "Position", "Board",
    "InvalidGrid", "UnsolvablePuzzle", 
    "Generator",
    "Solver"
]

try:
    __version__ = version("python-lightsout")
except PackageNotFoundError:
    __version__ = "0.0.0"