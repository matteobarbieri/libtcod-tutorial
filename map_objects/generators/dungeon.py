"""
Create a dungeon-like map level, using tunnellers
"""

from ..game_map import GameMap

from ..tile import Floor

import random

def dig_rect(game_map, xy):
    """
    Dig a rectangle of empty space in the map
    """

    x1 = xy[0]
    y1 = xy[1]
    x2 = xy[2]
    y2 = xy[3]

    for x in range(x1, x2+1):
        for y in range(y1, y2+1):

            game_map.tiles[x][y] = Floor()

def generate_dungeon_level(width, height, min_room_length, max_room_length):

    level = GameMap(width, height)

    start_x = int(width/2) + random.randint(-10, 10)
    start_y = int(height/2) + random.randint(-10, 10)

    # Dig entrance room
    dig_rect(level, [start_x-5, start_y-5, start_x+5, start_y+5])

    return level

