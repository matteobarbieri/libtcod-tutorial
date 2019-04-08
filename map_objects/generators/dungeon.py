"""
Create a dungeon-like map level, using tunnellers
"""

from ..game_map import GameMap

from ..tile import Floor, Tile

import logging


import random

from enum import Enum, auto


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


class Blueprint():
    """
    A blueprint for a room, corridor or other
    """

    def __init__(self, xy):

        self.x1, self.y1, self.x2, self.y2 = xy

    @property
    def xy(self):
        return [self.x1, self.y1, self.x2, self.y2]


class Direction(Enum):

    WEST = (-1, 0)
    NORTH = (0, 1)
    EAST = (1, 0)
    SOUTH = (0, -1)

class Tunneller():

    last_direction = None


    def __init__(self, x, y, min_tunnel_length, max_tunnel_length,
                 tunnel_widths=[3,5]):
        """
        Set tunneller's initial parameters
        """

        # Initial position
        self.x = x
        self.y = y

        # Min and max tunnel length
        self.min_tunnel_length = min_tunnel_length
        self.max_tunnel_length = max_tunnel_length

        # Allowed widths for tunnels
        self.tunnel_widths = tunnel_widths

    def dig_tunnel(self, game_map):
        1/0
        pass

    def pick_direction(self):
        1/0
        pass

    def pick_tunnel_length(self):
        1/0
        pass

    def create_room(self, game_map):
        1/0
        pass

    def create_junction(self, game_map):
        1/0
        pass

    def area_is_available(self, game_map, xy):
        return area_is_available(game_map, xy)

    def commit(self, game_map, blueprint):
        """
        Actually do things on the game map, after verifying that the blueprint
        was viable.
        """

        dig_rect(game_map, blueprint.xy)

    def create_junction_blueprint(self, game_map, d):

        1/0
        # Extract directions parameters
        dx, dy = d

    def create_tunnel_blueprint(self, game_map, d):

        # Extract directions parameters
        # dx, dy = d

        # Pick tunnel length
        tunnel_length = random.randint(
            self.min_tunnel_length, self.max_tunnel_length)

        # Pick tunnel width
        tunnel_width = random.choice(self.tunnel_widths)

        # Generate coordinates of top left and bottom right corner of the
        # rectangle of the tunnel

        # TODO to improve
        if d == Direction.WEST:
            x1 = self.x - 1*(tunnel_length)
            x2 = self.x - 1

            y1 = self.y - 1*(int(tunnel_width/2))
            y2 = self.y + 1*(int(tunnel_width/2))
        elif d == Direction.EAST:
            x1 = self.x + 1
            x2 = self.x + 1*(tunnel_length)

            y1 = self.y - 1*(int(tunnel_width/2))
            y2 = self.y + 1*(int(tunnel_width/2))
        elif d == Direction.NORTH:
            x1 = self.x - 1*(int(tunnel_width/2))
            x2 = self.x + 1*(int(tunnel_width/2))

            y1 = self.y - 1*(tunnel_length)
            y2 = self.y - 1
        elif d == Direction.SOUTH:
            x1 = self.x - 1*(int(tunnel_width/2))
            x2 = self.x + 1*(int(tunnel_width/2))

            y1 = self.y + 1
            y2 = self.y + 1*(tunnel_length)

        # x1 = self.x + dx*(tunnel_length)
        # x2 = self.x + dx

        # y1 = self.y + dy*(int(tunnel_width/2))
        # y2 = self.y + dy*(int(tunnel_width/2))

        # Collect coordinates in a variable
        xy = [x1, y1, x2, y2]

        if self.area_is_available(game_map, xy):
            return Blueprint(xy)

    def create_blueprint(self, game_map, d):
        """
        Create a blueprint for a piece of dungeon

        d: direction
        """

        # self.create_junction_blueprint(game_map, d)
        t_bp = self.create_tunnel_blueprint(game_map, d)

        return t_bp

    def step(self, game_map):
        """
        Perform a step of dungeon creation
        """

        # First collect all possible directions in which to go
        available_directions = list(Direction)

        # Shuffle them
        random.shuffle(available_directions)

        # Try to build something one direction at a time
        for d in available_directions:

            try:
                bp = self.create_blueprint(game_map, d)
                break
            except Exception as e:
                print(e)
                # Tunneller was unable to create anything in that direction; try
                # another one
                pass

        else:
            raise Exception("No more space")
        
        # game_map = self.commit(game_map, bp)
        self.commit(game_map, bp)

def generate_dungeon_level(width, height, min_room_length, max_room_length):

    level = GameMap(width, height)

    start_x = int(width/2) + random.randint(-10, 10)
    start_y = int(height/2) + random.randint(-10, 10)

    # Start with a Junction, roughly in the middle of the map
    # dig_rect(level, [start_x-5, start_y-5, start_x+5, start_y+5])


    t1 = Tunneller(
        start_x, start_y, 
        min_tunnel_length=7, max_tunnel_length=20)

    t1.step(level)


    return level

