import libtcodpy as libtcod

from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level

from entity import Entity

from game_messages import MessageLog

from game_states import GameStates

from map_objects.game_map import GameMap

from render_functions import RenderOrder


def get_constants():
    window_title = 'Roguelike Tutorial Revised'

    # Size of the game screen
    screen_width = 80
    screen_height = 50

    # Size of the panel containing health bar and log
    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    # Parameters for the log panel
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    # Size of the playing map
    map_width = 80
    map_height = 43

    # Parameters for rooms generation
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

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

    # Fighter component for player
    fighter_component = Fighter(hp=100, defense=1, power=4)
    
    # Inventory component for the player
    inventory_component = Inventory(26)

    # The level component for leveling up
    level_component = Level()

    # The equipment component, for equippable items
    equipment_component = Equipment()

    # Create the Player object
    player = Entity(
        0,
        0,
        '@',
        libtcod.white,
        'Player',
        blocks=True,
        render_order=RenderOrder.ACTOR,
        fighter=fighter_component,
        inventory=inventory_component,
        level=level_component,
        equipment=equipment_component
    )

    entities = [player]

    # Create the game map
    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(
        constants['max_rooms'], 
        constants['room_min_size'], 
        constants['room_max_size'],
        constants['map_width'], 
        constants['map_height'], 
        player, 
        entities)

    # Initialize message log
    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    # Begin the game in player's turn
    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
