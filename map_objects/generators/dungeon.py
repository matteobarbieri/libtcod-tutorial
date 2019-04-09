"""
Create a dungeon-like map level, using tunnellers
"""

from ..game_map import GameMap, Corridor, Room, Junction

from ..tile import Floor, Tile

from ..directions import Direction

import logging

import random

from ..map_utils import area_is_available


class NoMoreSpaceException(Exception):
    pass


class Tunneller():

    last_direction = None


    def __init__(self, x, y, 
                 min_tunnel_length, max_tunnel_length, tunnel_widths=[3,5],
                 min_room_size=5, max_room_size=13,
                 min_junction_size=5, max_junction_size=10):
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

        # Junction minimum and maximum lateral dimensions
        self.min_junction_size = min_junction_size
        self.max_junction_size = max_junction_size

    def move_to(self, map_part):
        """
        Move the tunneller to a new part of the map
        """
        self.current_location = map_part


    def create_starting_room(self, game_map):

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

        # Create the room object
        room = Room(xy)
        room.available_directions = list(Direction)

        # Actually dig the empty space in the map
        room.create(game_map)

        # Add the room to the map
        game_map.add_room(room)

        # Set current location as this room
        self.move_to(room)

    def commit(self, game_map, blueprint):
        """
        Actually do things on the game map, after verifying that the blueprint
        was viable.
        """

        for part in blueprint:
            part.create(game_map)

    def create_junction_blueprint(self, game_map, x, y, d, blueprint):
        """
        blueprint: list
            A list of elements created to that point
        """

        # Extract directions parameters
        # dx, dy = d

        # Pick tunnel length
        junction_size = random.randint(
            self.min_junction_size, self.max_junction_size)

        # Generate coordinates of top left and bottom right corner of the
        # rectangle of the tunnel

        # TODO to improve
        if d == Direction.WEST:
            x1 = x - 1*(junction_size)
            x2 = x - 1

            y1 = y - 1*(int(junction_size/2))
            y2 = y + 1*(int(junction_size/2))
        elif d == Direction.EAST:
            x1 = x + 1
            x2 = x + 1*(junction_size)

            y1 = y - 1*(int(junction_size/2))
            y2 = y + 1*(int(junction_size/2))
        elif d == Direction.NORTH:
            x1 = x - 1*(int(junction_size/2))
            x2 = x + 1*(int(junction_size/2))

            y1 = y - 1*(junction_size)
            y2 = y - 1
        elif d == Direction.SOUTH:
            x1 = x - 1*(int(junction_size/2))
            x2 = x + 1*(int(junction_size/2))

            y1 = y + 1
            y2 = y + 1*(junction_size)

        # Collect coordinates in a variable
        xy = [x1, y1, x2, y2]

        junction = Junction(xy)

        # Determine if the area can be dug based on map and blueprint
        can_dig = area_is_available(game_map, xy)

        if can_dig:
            for part in blueprint:
                if junction.intersects_with(part):
                    can_dig = False
                    break

        if can_dig:

            # Setup available directions for junction
            junction.available_directions = list(Direction)

            return junction 
        else:
            raise NoMoreSpaceException("Unavailable area")

    def create_corridor_blueprint(self, game_map, x, y, d, blueprint):
        """
        blueprint: list
            A list of elements created to that point
        """

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

            horizontal = True
        elif d == Direction.EAST:
            x1 = x + 1
            x2 = x + 1*(tunnel_length)

            y1 = y - 1*(int(tunnel_width/2))
            y2 = y + 1*(int(tunnel_width/2))

            horizontal = True
        elif d == Direction.NORTH:
            x1 = x - 1*(int(tunnel_width/2))
            x2 = x + 1*(int(tunnel_width/2))

            y1 = y - 1*(tunnel_length)
            y2 = y - 1

            horizontal = False
        elif d == Direction.SOUTH:
            x1 = x - 1*(int(tunnel_width/2))
            x2 = x + 1*(int(tunnel_width/2))

            y1 = y + 1
            y2 = y + 1*(tunnel_length)

            horizontal = False

        # Collect coordinates in a variable
        xy = [x1, y1, x2, y2]

        corridor = Corridor(xy, horizontal)

        # Determine if the area can be dug based on map and blueprint
        can_dig = area_is_available(game_map, xy)

        if can_dig:
            for part in blueprint:
                if corridor.intersects_with(part):
                    can_dig = False
                    break

        if can_dig:

            # Setup available directions for corridor
            if horizontal:
                corridor.available_directions = [
                    Direction.WEST, Direction.EAST]
            else:
                corridor.available_directions = [
                    Direction.NORTH, Direction.SOUTH]

            return corridor
        else:
            raise NoMoreSpaceException("Unavailable area")

    def create_blueprint(self, game_map):
        """
        Create a blueprint for a piece of dungeon
        """

        # TODO connect rooms/corridors/junctions

        blueprint = list()

        ################################
        ####### Create Corridor ########
        ################################
        while self.current_location.has_available_directions():
            try:
                x, y, d = self.current_location.pick_starting_point()
                corridor = self.create_corridor_blueprint(game_map, x, y, d, blueprint)
                break
            except NoMoreSpaceException:
                # This direction didn't work, try another one
                pass
        else:
            raise NoMoreSpaceException("No more space when creating corridor")

        # Add the corridor to current blueprint
        blueprint.append(corridor)

        # Change tunneller's location to the newly created corridor
        self.move_to(corridor)

        ################################
        ######## Create Rooms ##########
        ################################

        # TODO

        ################################
        ####### Create Junction ########
        ################################
        while self.current_location.has_available_directions():
            try:
                x, y, d = self.current_location.pick_starting_point()
                junction = self.create_junction_blueprint(game_map, x, y, d, blueprint)
                break
            except NoMoreSpaceException:
                # This direction didn't work, try another one
                pass
        else:
            raise NoMoreSpaceException("No more space when creating junction")

        # Add the junction to current blueprint
        blueprint.append(junction)

        # Change tunneller's location to the newly created junction
        self.move_to(junction)


        # TODO this will actually be a better thing in the future

        return blueprint

    def step(self, game_map):


        try:
            # TODO
            bp = self.create_blueprint(game_map)

        except NoMoreSpaceException as e:
            print(e)
            # Tunneller was unable to create anything in that direction; try
            # another one
        
        # game_map = self.commit(game_map, bp)
        self.commit(game_map, bp)

        # TODO
        # Update current location
        # self.current_location = new_location

def generate_dungeon_level(width, height, min_room_length, max_room_length):

    level = GameMap(width, height)

    start_x = int(width/2) + random.randint(-10, 10)
    start_y = int(height/2) + random.randint(-10, 10)

    # Start with a Junction, roughly in the middle of the map
    # dig_rect(level, [start_x-5, start_y-5, start_x+5, start_y+5])


    t1 = Tunneller(
        start_x, start_y, 
        min_tunnel_length=7, max_tunnel_length=20)

    t1.create_starting_room(level)

    t1.step(level)


    return level

