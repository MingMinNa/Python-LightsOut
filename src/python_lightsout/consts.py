OFF: bool = False
ON : bool = True

OFF_CHAR = "."
ON_CHAR  = "O"


class Direction:
    # (row, col)
    UP    : tuple[int] = (-1,  0)
    DOWN  : tuple[int] = ( 1,  0)
    LEFT  : tuple[int] = ( 0, -1)
    RIGHT : tuple[int] = ( 0,  1)

    @classmethod
    def get_dirs(cls):
        return (
            Direction.UP, 
            Direction.DOWN, 
            Direction.LEFT, 
            Direction.RIGHT
        )