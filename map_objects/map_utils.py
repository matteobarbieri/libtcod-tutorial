import logging

from .tile import Tile, Floor

def area_is_available(game_map, xy):
    """
    Check that an area is made of actually empty space
    """

    # Extract coordinates
    x1, y1, x2, y2 = xy

    for x in range(x1, x2+1):
        for y in range(y1, y2+1):

            if type(game_map.tiles[x][y]) != Tile:
                return False

    return True

def dig_rect(game_map, xy):
    """
    Dig a rectangle of empty space in the map
    """

    # Extract coordinates
    x1, y1, x2, y2 = xy

    logging.basicConfig(level=logging.DEBUG)

    logger = logging.getLogger()
    logger.debug("Digging rectangle from ({}, {}) to ({}, {})".format(*xy))

    for x in range(x1, x2+1):
        for y in range(y1, y2+1):

            game_map.tiles[x][y] = Floor()

    return game_map


