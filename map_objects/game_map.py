from entity import Entity

from enum import Enum

from game_messages import Message

from item_functions import cast_confuse, cast_fireball, cast_lightning, heal

from map_objects.tile import Tile, Wall, Floor
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


class MapPart():

    def __init__(self, xy):
        # self.x1, self.y1, self.x2, self.y2 = xy
        self.xy = xy
        self.available_directions = list()

        # The list of other parts of the map this one is connected to
        # (possibly useful later for pathfinding etc.)
        self.connected_parts = list

    def intersects_with(self, other):
        """
        Returns True if the rectangle specified by other_xy has an intersection
        different than 0 with this map part.
        """

        return _intersection_area(self.xy, other.xy) > 0

    def has_available_directions(self):
        return len(self.available_directions) > 0

    def pick_starting_point(self):
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

        return y2 - y1

    @property
    def width(self):
        # Unpack coordinates
        x1, x2, = self.xy[0], self.xy[2]

        return x2 - x1

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

    def create(self, game_map):
        """
        Actually create the map part in the game map.
        """
        dig_rect(game_map, self.xy)

        # TODO
        # Do more than this

class Room(MapPart):

    def __init__(self, xy, door_xy=None):
        super().__init__(xy)

        self.door_xy = door_xy

    def create(self, game_map):
        """
        Actually create the map part in the game map.
        """

        super().create(game_map)

        # Also dig the door, if there is one
        if self.door_xy is not None:
            x, y = self.door_xy

            dig_rect(game_map, [x, y, x, y])



class Junction(MapPart):

    def __init__(self, xy):
        super().__init__(xy)


class Corridor(MapPart):

    def __init__(self, xy, horizontal):
        super().__init__(xy)

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
        self.corridors = list()
        self.junctions = list()


    def add_corridor(self, corridor):
        """
        """

        self.corridors.append(corridor)

    def add_junction(self, junction):
        """
        """

        self.junctions.append(junction)

    def add_room(self, room):
        """
        """

        self.rooms.append(room)

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
        with open(txt_file, 'w') as tf:
            for y in range(self.height):
                for x in range(self.width):

                    # c = self.tiles[x][y].fg_symbol
                    # if c == 250:
                        # tf.write(".")
                    # elif c == '#':
                        # tf.write("#")
                    # else:
                        # tf.write(" ")

                    t = self.tiles[x][y]
                    if type(t) == Floor:
                        tf.write(".")
                    elif type(t) == Wall:
                        tf.write("#")
                    else:
                        tf.write(" ")

                tf.write("\n")


    def make_map(self, max_rooms, 
                 room_min_size, room_max_size,
                 map_width, map_height, 
                 player, entities):

        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            # random width and height
            w = random.randint(room_min_size, room_max_size)
            h = random.randint(room_min_size, room_max_size)

            # random position without going out of the boundaries of the map
            x = random.randint(0, map_width - w - 1)
            y = random.randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this
            # one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if random.randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)


    def create_room(self, room):

        ### Create passable terrain in room space
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y] = Floor()

        ### Create walls around the room

        # Top and bottom
        for x in range(room.x1, room.x2+1):
            for y in [room.y1, room.y2]:

                # Only create walls in unassigned tiles
                if type(self.tiles[x][y]) == Tile:
                    # self.tiles[x][y] = Wall.create()
                    self.tiles[x][y] = Wall.create_from_palette()

        # Left and right
        for x in [room.x1, room.x2]:
            for y in range(room.y1+1, room.y2):

                # Only create walls in unassigned tiles
                if type(self.tiles[x][y]) == Tile:
                    # self.tiles[x][y] = Wall.create()
                    self.tiles[x][y] = Wall.create_from_palette()


    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y] = Floor()

            # Make borders Wall classes
            self.tiles[x][y-1] = \
                Wall.create_from_palette() if type(self.tiles[x][y-1]) == Tile \
                else self.tiles[x][y-1]
            self.tiles[x][y+1] = \
                Wall.create_from_palette() if type(self.tiles[x][y+1]) == Tile \
                else self.tiles[x][y+1]


    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y] = Floor()

            # Make borders Wall classes
            self.tiles[x-1][y] = \
                Wall.create_from_palette() if type(self.tiles[x-1][y]) == Tile \
                else self.tiles[x-1][y]

            self.tiles[x+1][y] = \
                Wall.create_from_palette() if type(self.tiles[x+1][y]) == Tile \
                else self.tiles[x+1][y]

    def place_entities(self, room, entities):
            
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)


        # Get a random number of monsters
        number_of_monsters = random.randint(0, max_monsters_per_room)
        number_of_items = random.randint(0, max_items_per_room)

        # Define chances for individual monsters/items

        monster_chances = {
            'orc': 80,
            'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
        }

        item_chances = {
            'healing_potion': 35,
            'sword': from_dungeon_level(
                [[5, 4]], self.dungeon_level),
            'shield': from_dungeon_level(
                [[15, 8]], self.dungeon_level),
            'lightning_scroll': from_dungeon_level(
                [[25, 4]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level(
                [[25, 6]], self.dungeon_level),
            'confusion_scroll': from_dungeon_level(
                [[10, 2]], self.dungeon_level)
        }


        # Spawn monsters in the room
        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any(
                    [entity for entity in entities if entity.x == x and entity.y == y]):

                # Pic a random monster
                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == 'orc':

                    # Spawn an orc
                    fighter_component = Fighter(
                        hp=20, defense=0, power=4, xp=35)
                    ai_component = BasicMonster()

                    monster = Entity(
                        x, y,
                        'o', libtcod.desaturated_green,
                        'Orc',
                        blocks=True,
                        render_order=RenderOrder.ACTOR,
                        fighter=fighter_component,
                        ai=ai_component
                    )

                else:
                    # Spawn a Troll

                    fighter_component = Fighter(hp=30, defense=2, power=8, xp=100)
                    ai_component = BasicMonster()

                    monster = Entity(
                        x, y,
                        'T', libtcod.darker_green,
                        'Troll',
                        blocks=True,
                        render_order=RenderOrder.ACTOR,
                        fighter=fighter_component,
                        ai=ai_component
                    )

                entities.append(monster)

        # Spawn items in the room
        for i in range(number_of_items):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            # Only in empty spaces
            if not any(
                    [entity for entity in entities if entity.x == x and entity.y == y]):
 
                # item_chance = random.randint(0, 100)
                item_choice = random_choice_from_dict(
                    item_chances)

                # Spawn a healing potion
                if item_choice == 'healing_potion':

                    item_component = Item(
                        use_function=heal, amount=40)
                    item = Entity(
                        x, y, '!', libtcod.violet,
                        'Healing Potion',
                        render_order=RenderOrder.ITEM,
                        item=item_component)

                # Spawn a sword
                elif item_choice == 'sword':
                    equippable_component = Equippable(
                        EquipmentSlots.MAIN_HAND, power_bonus=3)
                    item = Entity(
                        x, y, '/', libtcod.sky, 
                        'Sword', equippable=equippable_component)

                # Spawn a shield
                elif item_choice == 'shield':
                    equippable_component = Equippable(
                        EquipmentSlots.OFF_HAND, defense_bonus=1)
                    item = Entity(
                        x, y, '[', libtcod.darker_orange, 
                        'Shield', 
                        equippable=equippable_component)

                # Spawn a Fireball scroll
                elif item_choice == 'fireball_scroll':

                    item_component = Item(
                        use_function=cast_fireball, 
                        targeting=True, 
                        targeting_message=Message(
                            'Left-click a target tile for the fireball, or right-click to cancel.', 
                            libtcod.light_cyan),
                        damage=25, radius=3)
                    item = Entity(
                        x, y, '#', libtcod.red, 
                        'Fireball Scroll', 
                        render_order=RenderOrder.ITEM,
                        item=item_component)

                # Spawn a "Confuse monster" scroll
                elif item_choice == 'confusion_scroll':

                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan))
                    item = Entity(x, y, '#', libtcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                else:
                    item_component = Item(
                        use_function=cast_lightning, 
                        damage=40, maximum_range=5)

                    item = Entity(
                        x, y, '#', libtcod.yellow, 
                        'Lightning Scroll', render_order=RenderOrder.ITEM,
                        item=item_component)

                entities.append(item)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False


    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(
            constants['max_rooms'], 
            constants['room_min_size'], 
            constants['room_max_size'],
            constants['map_width'], 
            constants['map_height'], 
            player, 
            entities)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        return entities
