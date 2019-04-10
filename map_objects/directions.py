from enum import Enum, auto

class Direction(Enum):

    WEST = (-1, 0)
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)

