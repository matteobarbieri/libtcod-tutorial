"""
Create a dungeon-like map level, using tunnellers
"""

from ..game_map import GameMap, Corridor, Room, Door, Junction

from ..tile import Floor, Tile, Wall

from ..directions import Direction

import logging

import random

from ..map_utils import area_is_available

from ..map_utils import NoMoreSpaceException


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

            logging.getLogger().debug("Creating Room at {}".format(room.center))
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
            logging.getLogger().debug(
                "Creating Corridor at {}, heading {} of length {}".format(
                    corridor.center, d, tunnel_length))
            return corridor
        else:
            raise NoMoreSpaceException("Unavailable area")

    def create_blueprint(self, game_map):
        """
        Create a blueprint for a piece of dungeon
        """

        # TODO connect rooms/corridors/junctions

        blueprint = list()

        # Save reference to starting location
        starting_location = self.current_location

        ################################
        ####### Create Corridor ########
        ################################
        self.current_location.reset_available_directions()
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

            # Break the outer for loop
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

                # Connect room and corridor
                corridor.connect_to(room)
                room.connect_to(corridor)
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
        self.current_location.reset_available_directions()
        for _ in range(self.max_step_retries):
            while self.current_location.has_available_directions():
                try:
                    x, y, d = self.current_location.pick_starting_point()
                    junction = self.create_junction_blueprint(game_map, x, y, d, blueprint)
                    logging.getLogger().debug("Creating junction at {}".format(
                        junction.center))
                    break
                except NoMoreSpaceException:
                    # This direction didn't work, try another one
                    pass
            else:
                self.current_location.reset_available_directions()
                continue

            # Break the outer for
            break
        else:
            raise NoMoreSpaceException("No more space when creating junction")

        # Add the junction to current blueprint
        blueprint.append(junction)

        # Connect corridor and junction
        junction.connect_to(corridor)
        corridor.connect_to(junction)

        # Change tunneller's location to the newly created junction
        self.move_to(junction)

        # Connect first corridor to starting location
        corridor.connect_to(starting_location)
        starting_location.connect_to(corridor)

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
                print(e)
                # Tunneller was unable to create anything in that direction; try
                # another one
        else:
            # TODO improve this, possibly change Exception Type
            raise NoMoreSpaceException("Max number of retries hit")

def connect_parts(level, i, j):
    """
    Excavate a tunnel between two map parts
    """
    part_i = level.all_parts[i]
    part_j = level.all_parts[j]

    # logging.getLogger().info(
        # "Trying to connect a {} and a {} (from {} to {})".format(
            # part_i.__class__.__name__, part_j.__class__.__name__,
            # part_i.center, part_j.center))
    
    xi, yi = part_i.center
    xj, yj = part_j.center

    # In case xi is greater than xj, swap coordinates
    if xi > xj:
        xi, xj = xj, xi
        yi, yj = yj, yi

    # Determine y direction
    if yj > yi:
        dy = +1
    else:
        dy = -1

    ### Excavate 1-wide tunnel
    
    # A list containing the coordinates of the skeleton of the 
    # tunnel
    tunnel_skeleton = list()

    # Start from the left element
    x = xi
    y = yi

    # Move horizontally first
    while(x != xj):
        x += 1
        # print("{} {}".format(x, xj))
        if type(level.tiles[x][y]) != Tile:
            # If it has already been excavated AND it does not belong to one
            # of the two other parts, raise an exception
            if not part_i.has_tile(x, y) and not part_j.has_tile(x, y):
                raise NoMoreSpaceException("Unable to connect two parts")

        tunnel_skeleton.append((x, y))

    # Then vertically
    while(y != yj):
        y += dy
        # print("{} {}".format(y, yj))
        if type(level.tiles[x][y]) != Tile:
            # If it has already been excavated AND it does not belong to one
            # of the two other parts, raise an exception
            if not part_i.has_tile(x, y) and not part_j.has_tile(x, y):
                raise NoMoreSpaceException("Unable to connect two parts")

        tunnel_skeleton.append((x, y))

    # TODO
    # Enlarge tunnel

    # Do excavate tunnel
    for x, y in tunnel_skeleton:
        level.tiles[x][y] = Floor()

    # Mark the two map parts as connected
    part_i.connect_to(part_j)
    part_j.connect_to(part_i)


def connect_close_parts(level):
    
    # First of all, compute distance matrix
    N_parts = len(level.all_parts)

    distance_list = list()
    # distance_matrix = list()

    for i in range(N_parts):
        # dm_row = list()
        for j in range(i+1, N_parts):

            d = level.all_parts[i].distance_from(level.all_parts[j])
            # dm_row.append(d)

            distance_list.append(((i, j), d))

        # distance_matrix.append(dm_row)

    sorted_distance_list = sorted(distance_list, key=lambda i : i[1])

    n_connected = 0
    max_connected = 10
    max_distance = 12

    for (i, j), d in sorted_distance_list:

        # Stop when distance is too high or reach the maximum number of parts
        # connected
        if d > max_distance or n_connected >= max_connected:
            break

        # Only try to connect those not already connected
        if not level.all_parts[i].is_connected_to(level.all_parts[j]):
            try:
                connect_parts(level, i, j)
                logging.getLogger().debug("Connected parts {} and {}".format(i, j))
                n_connected += 1
            except NoMoreSpaceException as e:
                print("While creating connections:")
                print(e)


    # TODO to complete!

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

    logging.getLogger().info("Initializing tunnelers")

    t1 = Tunneller(
        min_tunnel_length=9, max_tunnel_length=20)
    t2 = Tunneller(
        min_tunnel_length=9, max_tunnel_length=20)
    t3 = Tunneller(
        min_tunnel_length=9, max_tunnel_length=20)
    t4 = Tunneller(
        min_tunnel_length=9, max_tunnel_length=20)

    # Start with a Junction, roughly in the middle of the map
    start_x = int(width/2) + random.randint(-10, 10)
    start_y = int(height/2) + random.randint(-10, 10)

    t1.create_starting_junction(start_x, start_y, level)

    # Move the other three to the same room
    t2.move_to(t1.current_location)
    t3.move_to(t1.current_location)
    t4.move_to(t1.current_location)

    tunnelers_queue = [t1, t2, t3, t4]

    logging.getLogger().info("Creating main dungeon structure")
    while len(tunnelers_queue) > 0:

        t = tunnelers_queue.pop(0)

        try:
            # Perform one step
            t.step(level)

            # Put tunneler at the end of the queue
            tunnelers_queue.append(t)
        except NoMoreSpaceException as e:
            print(e)
            # Simply do not append the tunneler to the queue

    # Improve connectivity
    logging.getLogger().info("Creating additional connections")
    connect_close_parts(level)

    # Add an external layer of walls to rooms
    logging.getLogger().info("Adding walls")
    add_walls(level)

    return level

