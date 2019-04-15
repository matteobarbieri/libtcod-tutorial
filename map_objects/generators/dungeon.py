"""
Create a dungeon-like map level, using tunnellers
"""

from ..game_map import GameMap, Corridor, Room, Door, Junction

from ..tile import Floor, Tile, Wall

from ..directions import Direction

import logging

import random

from ..map_utils import area_is_available

class NoMoreSpaceException(Exception):
    pass


class Tunneller():

    last_direction = None


    def __init__(self,
                 min_tunnel_length=9, max_tunnel_length=20,
                 tunnel_widths=[1, 3, 5],
                 min_room_size=5, max_room_size=9,
                 min_junction_size=5, max_junction_size=9,
                 max_step_retries=4):
        """
        Set tunneller's initial parameters
        """

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

        # Max number of times of retry for the step function
        self.max_step_retries = max_step_retries

    def move_to(self, map_part):
        """
        Move the tunneller to a new part of the map
        """
        self.current_location = map_part


    def create_starting_junction(self, x, y, game_map):

        # Pick junction dimensions
        size = random.randint(self.min_junction_size, self.max_junction_size)

        # Room coordinates
        x1 = x - int(size/2)
        x2 = x1 + size
        y1 = y - int(size/2)
        y2 = y1 + size 

        # Collect coordinates in a variable
        xy = [x1, y1, x2, y2]

        # Create the junction object
        junction = Junction(xy, list(Direction))

        # Actually dig the empty space in the map
        junction.dig(game_map)

        # Add the junction to the map
        game_map.add_junction(junction)

        # Set current location as this junction
        self.move_to(junction)

    def commit(self, game_map, blueprint):
        """
        Actually do things on the game map, after verifying that the blueprint
        was viable.
        """

        for part in blueprint:
            game_map.add_part(part)
            # part.dig(game_map)

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

        junction = Junction(xy, list(Direction))

        # Determine if the area can be dug based on map and blueprint
        # can_dig = area_is_available(game_map, xy)
        can_dig = game_map.can_place(junction)

        if can_dig:
            for part in blueprint:
                if junction.intersects_with(part):
                    can_dig = False
                    break

        if can_dig:

            return junction 
        else:
            raise NoMoreSpaceException("Unavailable area")

    def create_room_blueprint(self, game_map, x, y, d, blueprint):
        """
        blueprint: list
            A list of elements created to that point

        x, y : int
            Position of the door tile leading to the room

        d : Direction
            The direction of the room w.r.t. the element where it was created
        """

        # Pick room dimensions
        w = random.randint(self.min_room_size, self.max_room_size)
        h = random.randint(self.min_room_size, self.max_room_size)

        # Generate coordinates of top left and bottom right corner of the
        # room

        # Room coordinates
        # TODO to improve
        if d == Direction.NORTH:
            x1 = x - 1*(int(w/2))
            x2 = x1 + w

            y1 = y - h + 1
            y2 = y 
        elif d == Direction.SOUTH:
            x1 = x - 1*(int(w/2))
            x2 = x1 + w

            y1 = y
            y2 = y + h - 1
        elif d == Direction.WEST:
            x1 = x - w + 1
            x2 = x

            y1 = y - 1*(int(h/2))
            y2 = y1 + h - 1
        elif d == Direction.EAST:
            x1 = x
            x2 = x + w - 1

            y1 = y - 1*(int(h/2))
            y2 = y1 + h - 1

        # Collect coordinates in a variable
        xy = [x1, y1, x2, y2]

        room = Room(xy, list(Direction))

        # Determine if the area can be dug based on map and blueprint
        # can_dig = area_is_available(game_map, xy)
        can_dig = game_map.can_place(room)

        # Also check the door, because why not
        # can_dig = can_dig and area_is_available(
            # game_map, [x, y, x, y])

        if can_dig:
            for part in blueprint:
                if room.intersects_with(part):
                    can_dig = False
                    break

        if can_dig:

            # Also specify the door
            door = Door([x, y, x, y])

            logging.getLogger().info(
                "Creating Room")
            return room, door
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
        # rectangle of the corridor

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

        # Setup available directions for corridor
        if horizontal:
            corridor_available_directions = [
                Direction.WEST, Direction.EAST]
        else:
            corridor_available_directions = [
                Direction.NORTH, Direction.SOUTH]

        corridor = Corridor(xy, corridor_available_directions, horizontal)

        # Determine if the area can be dug based on map and blueprint
        # can_dig = area_is_available(game_map, xy)
        can_dig = game_map.can_place(corridor)

        if can_dig:
            for part in blueprint:
                if corridor.intersects_with(part):
                    can_dig = False
                    break

        if can_dig:
            logging.getLogger().info(
                "Creating Corridor heading {} of length {}".format(
                    d, tunnel_length))
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
        for _ in range(self.max_step_retries):
            while self.current_location.has_available_directions():
                try:
                    x, y, d = self.current_location.pick_starting_point()
                    corridor = self.create_corridor_blueprint(game_map, x, y, d, blueprint)
                    break
                except NoMoreSpaceException:
                    # This direction didn't work, try another one
                    pass
            else:
                self.current_location.reset_available_directions()
                continue

            break
                
        else:
            raise NoMoreSpaceException("No more space when creating corridor")

        ################################
        ######## Create Rooms ##########
        ################################

        # Try 4 times for a suitable place
        for _ in range(self.max_step_retries):
            try:
                x, y, d = corridor.pick_room_starting_point()
                room, door = self.create_room_blueprint(game_map, x, y, d, blueprint)

                # Add room and door to current blueprint
                blueprint.append(room)
                blueprint.append(door)
                break
            except NoMoreSpaceException:
                pass


        # Add the corridor to current blueprint
        blueprint.append(corridor)

        # Change tunneller's location to the newly created corridor
        self.move_to(corridor)

        ################################
        ####### Create Junction ########
        ################################
        while self.current_location.has_available_directions():
            try:
                x, y, d = self.current_location.pick_starting_point()
                junction = self.create_junction_blueprint(game_map, x, y, d, blueprint)
                logging.getLogger().info("Creating junction")
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

        self.current_location.reset_available_directions()

        for i in range(self.max_step_retries):
            try:
                old_location = self.current_location
                bp = self.create_blueprint(game_map)

                # Commit changes to the map
                self.commit(game_map, bp)
                break

            except NoMoreSpaceException as e:
                self.current_location = old_location
                self.current_location.reset_available_directions()
                print(e)
                # Tunneller was unable to create anything in that direction; try
                # another one
        else:
            # TODO improve this, possibly change Exception Type
            raise NoMoreSpaceException("Max number of retries hit")

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

def generate_dungeon_level(width, height, min_room_length, max_room_length):

    level = GameMap(width, height)

    start_x = int(width/2) + random.randint(-10, 10)
    start_y = int(height/2) + random.randint(-10, 10)

    # Start with a Junction, roughly in the middle of the map
    # dig_rect(level, [start_x-5, start_y-5, start_x+5, start_y+5])

    t1 = Tunneller(
        min_tunnel_length=9, max_tunnel_length=20)
    t2 = Tunneller(
        min_tunnel_length=9, max_tunnel_length=20)
    t3 = Tunneller(
        min_tunnel_length=9, max_tunnel_length=20)
    t4 = Tunneller(
        min_tunnel_length=9, max_tunnel_length=20)

    # Start from a central room
    t1.create_starting_junction(start_x, start_y, level)

    # Move the other three to the same room
    t2.move_to(t1.current_location)
    t3.move_to(t1.current_location)
    t4.move_to(t1.current_location)

    tunnellers_list = [t1, t2, t3, t4]

    # Step a few times
    N_STEPS = 4 
    for _ in range(N_STEPS):

        for t in tunnellers_list:
            try:
                t.step(level)
                # t1.step(level)
                # t2.step(level)
                # t3.step(level)
                # t4.step(level)
            except NoMoreSpaceException as e:
                print(e)

    add_walls(level)

    return level

