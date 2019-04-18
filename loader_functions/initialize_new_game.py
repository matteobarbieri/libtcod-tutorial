import libtcodpy as libtcod

from components.equipment import Equipment
from components.equippable import Equippable
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.item import Item

from entity import Entity

from equipment_slots import EquipmentSlots

from game_messages import MessageLog

from game_states import GameStates

from map_objects.old import GameMap

from render_functions import RenderOrder

from map_objects.generators.dungeon import generate_dungeon_level

def get_constants():
    window_title = 'Roguelike Tutorial Revised'

    # Size of the game screen
    # screen_width = 80
    # screen_height = 50
    screen_width = 110
    screen_height = 60

    # Size of the panel containing health bar and log
    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    # Parameters for the log panel
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    # Size of the playing map
    # Must be greater or equal than screen in order to avoid the "pacman effect"
    map_width = 110
    map_height = 100

    # Parameters for rooms generation
    room_max_size = 10
    room_min_size = 6
    max_rooms = 40

    # Variables for field of view (FOV)
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    # Maximum number of monsters per room
    max_monsters_per_room = 3
    max_items_per_room = 2

    # Colors for rooms in and out of fov
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
        'colors': colors
    }

    return constants


def get_game_variables(constants):

    # TODO use parameters
    game_map = generate_dungeon_level(
        constants['map_width'], constants['map_height'], 10, 20)

    # Fighter component for player
    fighter_component = Fighter(hp=100, defense=1, power=2)
    
    # Inventory component for the player
    inventory_component = Inventory(26)

    # The level component for leveling up
    level_component = Level()

    # The equipment component, for equippable items
    equipment_component = Equipment()

    # Create the Player object
    player = Entity(
        0, 0, # Coordinates - useless here
        '@', libtcod.white, 'Player', # Appearance
        blocks=True,
        render_order=RenderOrder.ACTOR,
        components=dict(
            fighter=fighter_component,
            inventory=inventory_component,
            level=level_component,
            equipment=equipment_component
        )
    )

    # Give a starting item, a dagger
    equippable_component = Equippable(
        EquipmentSlots.MAIN_HAND, power_bonus=2)
    dagger = Entity(
        0, 0, '-', libtcod.sky, 'Dagger',
        components=dict(equippable=equippable_component, item=Item()))
    
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)

    # Place player in the map
    game_map.place_player(player)

    # Initialize message log
    message_log = MessageLog(
        constants['message_x'], constants['message_width'],
        constants['message_height'])

    # Begin the game in player's turn
    game_state = GameStates.PLAYERS_TURN

    return player, game_map, message_log, game_state
