"""
Create a dungeon-like map level, using tunnellers
"""

from ..game_map import GameMap, Corridor, Room

from ..tile import Floor, Tile

from ..directions import Direction

import logging

import random


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


class Tunneller():

    last_direction = None


    def __init__(self, x, y, 
                 min_tunnel_length, max_tunnel_length, tunnel_widths=[3,5],
                 min_room_size=5, max_room_size=10):
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

        # Room minimum and maximum lateral dimensions
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size

    def dig_tunnel(self, game_map):
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

    def dig_starting_room(self, game_map):

        # Pick room dimensions
        w = random.randint(self.min_room_size, self.max_room_size)
        h = random.randint(self.min_room_size, self.max_room_size)

        # Room coordinates
        x1 = self.x - int(w/2)
        x2 = x1 + w
        y1 = self.y - int(h/2)
        y2 = y1 + h 

        # Collect coordinates in a variable
        xy = [x1, y1, x2, y2]

        room = Room(xy)
        room.available_directions = list(Direction)

        dig_rect(game_map, xy)

        # Set current location as this room
        self.current_location = room


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

    def create_tunnel_blueprint(self, game_map, x, y, d):

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
            x1 = x - 1*(tunnel_length)
            x2 = x - 1

            y1 = y - 1*(int(tunnel_width/2))
            y2 = y + 1*(int(tunnel_width/2))
        elif d == Direction.EAST:
            x1 = x + 1
            x2 = x + 1*(tunnel_length)

            y1 = y - 1*(int(tunnel_width/2))
            y2 = y + 1*(int(tunnel_width/2))
        elif d == Direction.NORTH:
            x1 = x - 1*(int(tunnel_width/2))
            x2 = x + 1*(int(tunnel_width/2))

            y1 = y - 1*(tunnel_length)
            y2 = y - 1
        elif d == Direction.SOUTH:
            x1 = x - 1*(int(tunnel_width/2))
            x2 = x + 1*(int(tunnel_width/2))

            y1 = y + 1
            y2 = y + 1*(tunnel_length)

        # x1 = self.x + dx*(tunnel_length)
        # x2 = self.x + dx

        # y1 = self.y + dy*(int(tunnel_width/2))
        # y2 = self.y + dy*(int(tunnel_width/2))

        # Collect coordinates in a variable
        xy = [x1, y1, x2, y2]

        if self.area_is_available(game_map, xy):
            return Blueprint(xy)
        else:
            raise Exception("Unavailable area")

    def create_blueprint(self, game_map, x, y, d):
        """
        Create a blueprint for a piece of dungeon

        d: direction
        """

        # self.create_junction_blueprint(game_map, d)
        t_bp = self.create_tunnel_blueprint(game_map, x, y, d)

        return t_bp

    def step(self, game_map):

        x, y, d = self.current_location.pick_starting_point()

        try:
            # TODO
            bp = self.create_blueprint(game_map, x, y, d)
            # new_location, bp = self.create_blueprint(game_map, x, y, d)

        except Exception as e:
            print(e)
            # Tunneller was unable to create anything in that direction; try
            # another one
            pass
        
        # game_map = self.commit(game_map, bp)
        self.commit(game_map, bp)

        # TODO
        # Update current location
        # self.current_location = new_location

    def step2(self, game_map):
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

    t1.dig_starting_room(level)

    t1.step(level)


    return level

