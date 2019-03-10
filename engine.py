import libtcodpy as libtcod

from components.fighter import Fighter

from entity import Entity, get_blocking_entities_at_location
from input_handlers import handle_keys
from fov_functions import initialize_fov, recompute_fov
from render_functions import clear_all, render_all, RenderOrder
from map_objects.game_map import GameMap
from game_states import GameStates
from death_functions import kill_monster, kill_player

from game_messages import MessageLog

def main():

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

    # Colors for rooms in and out of fov
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    # Fighter component for player
    fighter_component = Fighter(hp=30, defense=2, power=5)

    # Create the Player object
    player = Entity(
            0,
            0,
            '@',
            libtcod.white,
            'Player',
            blocks=True,
            render_order=RenderOrder.ACTOR,
            fighter=fighter_component
    )

    entities = [player]

    # Set font
    libtcod.console_set_custom_font(
            'data/fonts/arial10x10.png', 
            libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
    )

    # Initialize main window
    libtcod.console_init_root(
            screen_width, 
            screen_height, 
            'libtcod tutorial revised', 
            False
    )

    # The main game screen
    con = libtcod.console_new(screen_width, screen_height)

    # The UI screen
    panel = libtcod.console_new(screen_width, panel_height)

    # Create the game map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(
            max_rooms, 
            room_min_size, 
            room_max_size, 
            map_width, 
            map_height, 
            player,
            entities,
            max_monsters_per_room
    )

    # When the game starts the fov must be computed for the first time
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    # Initialize message log
    message_log = MessageLog(message_x, message_width, message_height)

    # Handles for keyboard and mouse inputs
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Begin the game in player's turn
    game_state = GameStates.PLAYERS_TURN

    # Main loop
    while not libtcod.console_is_window_closed():

        # Wait for an event
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # If the fov needs to be recomputed (for instance, because the player
        # moved, do it
        if fov_recompute:
            recompute_fov(
                    fov_map, 
                    player.x, 
                    player.y, 
                    fov_radius, 
                    fov_light_walls, 
                    fov_algorithm
            )

        # Render all entities on the map
        # render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, screen_width, screen_height,
                   # bar_width, panel_height, panel_y, colors)
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width,
                   screen_height, bar_width, panel_height, panel_y, colors)

        # Reset fov_recompute to False
        fov_recompute = False

        # ACtually print stuff on screen
        libtcod.console_flush()

        clear_all(con, entities)

        # Detect player's action
        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        player_turn_results = []

        # If it is player's turn and it is a move action, do it
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            
            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                # There is a blocking entity in destination tile
                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)

                # Destination tile is empty, can move
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        # if key.vk == libtcod.KEY_ESCAPE:
        if exit:
            return True

        # Toggle full screen
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # Loop through all results
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                message_log.add_message(message)

            # Handle death of entities
            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

        # Enemies' turn
        if game_state == GameStates.ENEMY_TURN:

            # Loop through all entities
            for entity in entities:

                # Only do something for those having an AI component,
                # For very obvious reasons
                if entity.ai:

                    # Get the results of an enemy's action
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        # Player's dead
                        break

            # for-else loop end: switch back to player's turn after all entities
            # have performed their action
            else:
                game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()
