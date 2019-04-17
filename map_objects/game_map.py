from entity import Entity

from enum import Enum

import logging

from game_messages import Message

from item_functions import cast_confuse, cast_fireball, cast_lightning, heal

from map_objects.tile import Tile, Wall, Floor
from map_objects.tile import Door as DoorTile

from map_objects.rectangle import Rect

from components.ai import BasicMonster
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs

import random

import shelve

from render_functions import RenderOrder

import libtcodpy as libtcod

from random_utils import from_dungeon_level, random_choice_from_dict

from .directions import Direction

from .map_utils import dig_rect, _intersection_area

from .map_utils import NoMoreSpaceException


class MapPart():

    def __init__(self, xy, available_directions=None):
        # self.x1, self.y1, self.x2, self.y2 = xy
        self.xy = xy
        self.available_directions = available_directions

        # Also keep track of the original available directions (for map
        # generation)
        self._available_directions = available_directions

        # The list of other parts of the map this one is connected to
        # (possibly useful later for pathfinding etc.)
        self.connected_parts = list()

    def has_tile(self, x, y):
        """
        Check if a single tile belongs to this map part
        """

        # Unpack coordinates
        x1, y1, x2, y2 = self.xy

        return x >= x1 and x <= x2 and y >= y1 and y <= y2


    def remove_connection(self, other):
        if other in self.connected_parts:
            self.connected_parts.remove(other)

    def is_connected_to(self, other):
        """
        Returns True if self is connected to other
        """

        return other in self.connected_parts

    def connect_to(self, other):
        if other not in self.connected_parts:
            self.connected_parts.append(other)

    def distance_from(self, other):
        """
        Return the euclidean distance from the centers of the two parts
        """
        x1, y1 = self.center
        x2, y2 = other.center

        return ((x2 - x1)**2 + (y2 - y1)**2)**(0.5)

    def reset_available_directions(self):

        self. available_directions = list(self._available_directions)

    def intersects_with(self, other):
        """
        Returns True if the rectangle specified by other_xy has an intersection
        different than 0 with this map part.
        """

        does_intersect = _intersection_area(self.xy, other.xy) > 0
        if does_intersect:
            text = 'does intersect'
        else:
            text = 'does NOT intersect'

        logger = logging.getLogger()
        logger.debug("{} at {} {} with {} at {}".format(\
                type(self), self.xy,
                text,
                type(other), other.xy,
            ))

        return does_intersect
        # return _intersection_area(self.xy, other.xy) > 0

    def has_available_directions(self):
        return len(self.available_directions) > 0

    def pick_starting_point(self):
        """
        Pick a starting point and direction for the next element in the dungeon.
        The coordinates are supposed to be part of the previous element, i.e.
        walkable space (a Floor tile, NOT a Wall tile).
        """

        d = random.choice(self.available_directions)

        # Unpack coordinates
        x1, y1, x2, y2 = self.xy

        if d == Direction.WEST:
            x = x1
            y = y1 + int((y2 - y1)/2)
        elif d == Direction.EAST:
            x = x2
            y = y1 + int((y2 - y1)/2)
        elif d == Direction.NORTH:
            x = x1 + int((x2- x1)/2)
            y = y1 
        elif d == Direction.SOUTH:
            x = x1 + int((x2- x1)/2)
            y = y2

        # Remove option
        self.available_directions.remove(d)

        return x, y, d

    @property
    def height(self):
        # Unpack coordinates
        y1, y2, = self.xy[1], self.xy[3]

        return y2 - y1 + 1

    @property
    def width(self):
        # Unpack coordinates
        x1, x2, = self.xy[0], self.xy[2]

        return x2 - x1 + 1

    @property
    def center(self):
        """
        Return the rough coordinates of the center of the room
        """

        # Unpack coordinates
        x1, y1, x2, y2 = self.xy

        xc = x1 + int((x2 - x1)/2)
        yc = y1 + int((y2 - y1)/2)

        return xc, yc

    def dig(self, game_map, pad=0):
        """
        Actually dig the map part in the game map.
        """

        # Unpack coordinates
        x1, y1, x2, y2 = self.xy

        logger = logging.getLogger()
        logger.debug("Digging {} at {}".format(
            type(self), [x1+pad, y1+pad, x2-pad, y2-pad]))

        dig_rect(game_map, [x1+pad, y1+pad, x2-pad, y2-pad])

        # TODO
        # Do more than this

class Door(MapPart):
    """
    Represents a door in the dungeon. Can be bigger than one tile (to represent
    large gates).
    Has a state, can be open or closed
    """

    def __init__(self, xy, is_open=False):
        super().__init__(xy)

        self.is_open = is_open

    def dig(self, game_map):
        """
        Create the door in the map
        """

        # Unpack coordinates
        x1, y1, x2, y2 = self.xy

        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                game_map.tiles[x][y] = DoorTile()


class Room(MapPart):

    def __init__(self, xy, available_directions):
        super().__init__(xy, available_directions)

    def dig(self, game_map):
        """
        Actually dig the map part in the game map.
        """

        super().dig(game_map, pad=1)

        # # Also dig the door, if there is one
        # if self.door_xy is not None:
            # x, y = self.door_xy

            # dig_rect(game_map, [x, y, x, y])


class Junction(MapPart):

    def __init__(self, xy, available_directions):
        super().__init__(xy, available_directions)


class Corridor(MapPart):

    def __init__(self, xy, available_directions, horizontal):
        super().__init__(xy, available_directions)

        # Save the information about the placement of the tunnel
        self.horizontal = horizontal

    @property
    def vertical(self):
        return not self.horizontal

    def pick_room_starting_point(self):
        """
        Pick a starting point for a viable room
        """

        # Unpack coordinates
        x1, y1, x2, y2 = self.xy

        if self.horizontal:
            if random.random() < 0.5:
                # Room on top
                d = Direction.NORTH
                y = y1 - 1
                x = random.randint(x1+1, x2-1)
            else:
                # Room on bottom
                d = Direction.SOUTH
                y = y2 + 1
                x = random.randint(x1+1, x2-1)
        else:
            if random.random() < 0.5:
                # Room on the left
                d = Direction.WEST
                x = x1 - 1
                y = random.randint(y1+1, y2-1)
            else:
                # Room on the right
                d = Direction.EAST
                x = x2 + 1
                y = random.randint(y1+1, y2-1)

        return x, y, d


class GameMap:


    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dungeon_level = dungeon_level

        # Initialize the empty lists of rooms, corridors and junctions
        self.rooms = list()
        self.doors = list()
        self.corridors = list()
        self.junctions = list()

        # Initialize an empty list for entities in this level
        self.entities = list()

    @property
    def all_parts(self):
        """
        Returns the list of all major map parts
        (excludes doors)
        """
        return self.junctions + self.corridors + self.rooms

    def get_player_starting_coords(self):
        
        # TODO!!!
        for e in self.entities:
            if e.char == '<':
                return e.x, e.y

    def place_player(self, player):
        """
        Place player in the map
        """

        # TODO
        # Should place him/her in an entry/exit tile (depending on where they
        # came from).
        # starting_room = random.choice(self.rooms)
        
        x, y = self.get_player_starting_coords()
        player.x = x
        player.y = y

        # Add player to list of entities
        self.entities.append(player)

    def add_part(self, part):
        """
        Add a part to the map and also dig it
        """
        if ( type(part) == Corridor):
            self.add_corridor(part)
        elif type(part) == Junction:
            self.add_junction(part)
        elif type(part) == Room:
            self.add_room(part)
        elif type(part) == Door:
            self.add_door(part)

        # Create the tiles accordingly
        part.dig(self)

    def add_corridor(self, corridor):
        """
        """

        self.corridors.append(corridor)

    def add_junction(self, junction):
        """
        """

        self.junctions.append(junction)

    def add_door(self, door):
        """
        """

        self.doors.append(door)

    def add_room(self, room):
        """
        """

        self.rooms.append(room)

    def can_place(self, part):
        """
        Returns True if part can be placed in map (i.e. doesn't intersect with
        anything which is already present.

        Also needs to be in a valid tile

        Does not depend on tiles array
        """

        # First check that coordinates refer to a valid tile in the map
        # Unpack coordinates
        x1, y1, x2, y2 = part.xy

        # Check that it lies within the whole map
        geometry_check = (
            x1 > 0 and y1 > 0 and \
            x2 < (self.width - 1) and y2 < (self.height - 1)
        )

        if not geometry_check:
            return False

        # Then check for potential intersections with other elements of the map
        
        # Build the list of alla placed parts
        placed_parts = self.rooms + self.junctions + self.corridors

        for other in placed_parts:
            if part.intersects_with(other):
                return False

        return True

    def initialize_tiles(self):
        tiles = [
                [
                    Tile(True) for y in range(self.height)
                ] for x in range(self.width)
        ]

        return tiles

    def export_shelf(self, destination):
        with shelve.open(destination) as db:
            db['level'] = self

    def export_txt(self, txt_file):

        entities_dict = dict()

        for e in self.entities:
            entities_dict[(e.x, e.y)] = e

        with open(txt_file, 'w') as tf:
            for y in range(self.height):
                for x in range(self.width):

                    e = entities_dict.get((x, y))

                    # If there is an entity, show that
                    if e is not None:
                        tf.write(e.char)

                    # Else show the terrain element
                    else:
                        t = self.tiles[x][y]
                        if type(t) == Floor:
                            tf.write(".")
                        elif type(t) == DoorTile:
                            tf.write("+")
                        elif type(t) == Wall:
                            tf.write("#")
                        else:
                            tf.write(" ")

                tf.write("\n")


    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

