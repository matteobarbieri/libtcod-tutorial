import libtcodpy as libtcod

import math

from components.item import Item

from render_functions import RenderOrder


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    # TODO change components to kwargs
    def __init__(self, x, y, char, color, name, blocks=False,
                 block_sight=False, render_order=RenderOrder.CORPSE,
                 components=dict()):

        # The entity's current position
        self.x = x
        self.y = y

        # The ASCII character representing it
        self.char = char

        # Its color
        self.color = color

        # Its name
        self.name = name

        # Is it a blocking entity?
        self.blocks = blocks

        # Does it block LoS?
        self.block_sight = block_sight

        # Render order
        self.render_order = render_order

        self.components = dict()
        # Add components
        for k, v in components.items():
            self.add_component(k, v)

    # Fix the NoneType callable  due to overriding __getattr__ method
    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    def __getattr__(self, name):
        """
        Look through components
        """

        # First check that name is a valid component type
        # TODO to implement
        if True:
            # Return the corresponding component (or None)
            return self.components.get(name)
        else:
            raise AttributeError()

    def add_component(self, component_type, component):
        """
        Add a component to the entity
        """

        def check_component_type(component_type, component):
            """
            Check that the component is of the correct type
            """

            # TODO stub
            return True

        check_component_type(component_type, component)

        component.owner = self
        self.components[component_type] = component

    @property
    def c(self):
        """
        Shortcut to components attribute
        """
        return self.components

    def shoot(self, target):
        return self.fighter.shoot(target)

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def interact_with(self, other):
        """
        Default interaction with another entity

        player <-> monster: attack
        player  -> door: interact
        """

        # TODO check if hostile
        if other.fighter is not None:
            messages = self.fighter.attack(other)
            return messages

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (
            game_map.is_blocked(
                self.x +
                dx,
                self.y +
                dy) or get_blocking_entities_at_location(
                entities,
                self.x +
                dx,
                self.y +
                dy)):
            self.move(dx, dy)

    def move_astar(self, target, entities, game_map):
        # Create a FOV map that has the dimensions of the map
        fov = libtcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(
                    fov,
                    x1,
                    y1,
                    not game_map.tiles[x1][y1].block_sight,
                    not game_map.tiles[x1][y1].blocked)

        # Scan all the objects to see if there are objects that must be
        # navigated around. Check also that the object isn't self or the
        # target (so that the start and the end points are free).
        # The AI class handles the situation if self is next to the target so
        # it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                libtcod.map_set_properties(
                    fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0
        # if diagonal moves are prohibited
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's
        # coordinates
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also if such path is
        # shorter than 25 tiles. The path size matters if you want the monster
        # to use alternative longer paths (for example through other rooms),
        # if for example the player is in a corridor.
        # It makes sense to keep path size relatively low to keep the monsters
        # from running around the map if there's an alternative path really far
        # away
        if not libtcod.path_is_empty(
                my_path) and libtcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no
            # paths (for example another monster blocks a corridor), it will
            # still try to move towards the player (closer to the corridor
            # opening).
            self.move_towards(target.x, target.y, game_map, entities)

            # Delete the path to free memory
        libtcod.path_delete(my_path)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
