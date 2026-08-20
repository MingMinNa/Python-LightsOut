
class InvalidGrid(Exception):
    """
    A valid grid must have a size of `length * length`, \n
    and all values must be of type `bool`.
    """

class UnsolvablePuzzle(Exception):
    """
    The given puzzle is unsolvable.
    """