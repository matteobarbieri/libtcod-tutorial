import logging

from .tile import Tile, Floor

def area_is_available(game_map, xy):
    """
    Check that an area is made of actually empty space
    """

    # Extract coordinates
    x1, y1, x2, y2 = xy
    
    # Check that it lies within the whole map
    check_map_area = (
        x1 > 0 and y1 > 0 and \
        x2 < (game_map.width - 1) and y2 < (game_map.height - 1)
    )

    if not check_map_area:
        return False

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

def _intersection_area(xy1, xy2):  

    # Unpack coordinates
    x11, y11, x12, y12 = xy1
    x21, y21, x22, y22 = xy2

    dx = min(x12, x22) - max(x11, x21)
    dy = min(y12, y22) - max(y11, y21)

    if (dx>=0) and (dy>=0):
        return dx*dy
    else:
        return 0

