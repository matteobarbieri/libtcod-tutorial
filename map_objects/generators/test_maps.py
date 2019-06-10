"""
Create a dungeon-like map level, using tunnellers
"""

from ..game_map import GameMap, Room

from ..tile import Tile, Wall

from components.stairs import Stairs

from ..directions import Direction

import logging

import random

# import libtcodpy as libtcod
import tcod as libtcod

from render_functions import RenderOrder

from entity import Entity

from prefabs.orc import make_orc

from components.ai import MonsterAi

def add_walls(level):
    """
    Creates walls in all Tile-type tiles adjacent to something non-Tile
    """

    for X in range(level.width):
        for Y in range(level.height):
            for x in range(max(X-1, 0), min(X+2, level.width)):
                for y in range(max(Y-1, 0), min(Y+2, level.height)):
                    if (type(level.tiles[X][Y]) == Tile and \
                       (type(level.tiles[x][y]) not in [Tile, Wall])):
                       ## Create wall
                       level.tiles[X][Y] = Wall.create_from_palette()

def add_monsters(level):
    """
    Add stairs for previous and next dungeon level
    """

    for room in level.rooms:
        # TODO for now, just generate an orc in every room
        if random.random() < 2:

            monster = make_orc(room, MonsterAi)

            level.entities.append(monster)


def generate_dungeon_level(width, height, min_room_length, max_room_length):
    # TODO add parameters (and use them!)

    level = GameMap(width, height)

    xc = int(width/2)
    yc = int(height/2)

    # Collect coordinates in a variable
    xy = [xc-10, yc-6, xc+10, yc+6]

    entry_room = Room(xy, list(Direction))
    level.add_part(entry_room)

    # Add an external layer of walls to rooms
    logging.getLogger().info("Adding walls")
    add_walls(level)

    # Populate Dungeon with entities
    # Monsters
    add_monsters(level)

    # Create and add entry stairs '<'
    entry_x, entry_y = entry_room.center

    up_stairs_component = Stairs(level.dungeon_level - 1)
    up_stairs = Entity(
        entry_x, entry_y, '<',
        libtcod.white, 'Stairs up', render_order=RenderOrder.STAIRS,
        components=dict(stairs=up_stairs_component))

    level.entities.append(up_stairs)

    return level
