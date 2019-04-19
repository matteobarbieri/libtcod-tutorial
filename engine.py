import libtcodpy as libtcod

import argparse

import random

import sys

from entity import get_blocking_entities_at_location
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box
from fov_functions import initialize_fov, recompute_fov
from render_functions import clear_all, render_all
from game_states import GameStates
from death_functions import kill_monster, kill_player

from game_messages import Message

from actions import ShowMenuException

def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--seed', type=int)

    return parser.parse_args()


def play_game(player, game_map, 
              message_log, game_state, 
              terrain_layer, 
              panel, constants):

    # At the beginning of the game, recompute fov
    fov_recompute = True
    redraw_terrain = True
    redraw_entities = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    targeting_item = None

    # entities = game_map.entities

    ############################################
    ############### MAIN LOOP ##################
    ############################################

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        ############################################
        ########### RENDER GAME WINDOW #############
        ############################################
        if fov_recompute:
            recompute_fov(
                fov_map, player.x, player.y, 
                constants['fov_radius'], constants['fov_light_walls'],
                constants['fov_algorithm'])

        render_all(
            terrain_layer, panel, 
            player, game_map, fov_map, fov_recompute, 
            redraw_terrain, redraw_entities, message_log,
            constants, mouse, game_state)

        fov_recompute = False
        redraw_terrain = False
        redraw_entities = False

        libtcod.console_flush()

        if game_state in [GameStates.PLAYERS_TURN,]:

            ############################################
            ############# EXECUTE ACTIONS ##############
            ############################################
            action = handle_keys(key, game_state)

            # TODO to restore
            # mouse_action = handle_mouse(mouse)

            ####### UPDATED

            ####### TO UPDATE
            # move = action.get('move')
            # wait = action.get('wait')
            # pickup = action.get('pickup')
            # show_inventory = action.get('show_inventory')
            # drop_inventory = action.get('drop_inventory')
            # inventory_index = action.get('inventory_index')
            # take_stairs = action.get('take_stairs')
            # level_up = action.get('level_up')
            # exit = action.get('exit')
            # fullscreen = action.get('fullscreen')
            # show_character_screen = action.get('show_character_screen')
            
            # TODO to restore
            # left_click = mouse_action.get('left_click')
            # right_click = mouse_action.get('right_click')

            player_turn_results = []

            # Add all objects required to perform any action
            action.set_context(game_map, player, message_log)

            # Execute it
            try:
                outcome = action.execute()
            except ShowMenuException:
                # Exit main game loop and return to main menu
                return True

            ############################################
            ############# RESOLVE OUTCOME ##############
            ############################################
            if outcome is not None:

                # Update game state
                if outcome.get('next_state') is not None:
                    game_state = outcome.get('next_state')

                # Update results
                if outcome.get('results') is not None:
                    player_turn_results.extend(outcome['results'])
                
                # Determine whether to recompute fov...
                if outcome.get('fov_recompute') is not None:
                    fov_recompute = outcome.get('fov_recompute')

                # Or redraw terrain
                if outcome.get('redraw_terrain') is not None:
                    redraw_terrain = outcome.get('redraw_terrain')

        elif game_state == GameStates.ENEMY_TURN:

            # Simply go back to player's turn state
            game_state = GameStates.PLAYERS_TURN
            redraw_entities = True

        """
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(
                    game_map.entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)

                    fov_recompute = True
                    redraw_terrain = True

                # TODO uncomment
                # game_state = GameStates.ENEMY_TURN

        """

        ### COMMENT FROM HERE ###
        """
        elif wait:
            game_state = GameStates.ENEMY_TURN

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in game_map.entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if (inventory_index is not None and \
            previous_game_state != GameStates.PLAYER_DEAD and \
            inventory_index < len(player.inventory.items)):

            # An item has been selected, either use it or drop it
            # (depending on the context)
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(
                    player.inventory.use(
                        item, entities=game_map.entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        # The player takes the stairs down
        if take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    # TODO redo this part
                    raise Exception("To be implemented")
                    entities = game_map.next_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(terrain_layer)

                    break
            else:
                message_log.add_message(Message('There are no stairs here.', libtcod.yellow))

        # Leveling up
        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            elif level_up == 'str':
                player.fighter.base_power += 1
            elif level_up == 'def':
                player.fighter.base_defense += 1

            game_state = previous_game_state

        # Show character screen
        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        # Targeting something with a spell
        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        # Exit current context
        if exit:

            # If it was in a menu, go back to the previous state
            if game_state in (
                GameStates.SHOW_INVENTORY, 
                GameStates.DROP_INVENTORY, 
                GameStates.CHARACTER_SCREEN):

                game_state = previous_game_state

                redraw_terrain = True
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                # Go back to main menu
                save_game(player, game_map, message_log, game_state)

                return True
        
        # Toggle fullscreen
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # Handle results from player actions
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            equip = player_turn_result.get('equip')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            xp = player_turn_result.get('xp')

            # Add a message to the game log
            if message:
                message_log.add_message(message)

            # Somebody has died
            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                redraw_entities = True
                message_log.add_message(message)

            # An item has been picked up
            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            # An item has been consumed
            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            # An item has been dropped
            if item_dropped:
                entities.append(item_dropped)

                game_state = GameStates.ENEMY_TURN

            # An item has been [d]equipped
            if equip:
                equip_results = player.equipment.toggle_equip(
                    equip)

                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equipped:
                        message_log.add_message(
                            Message(
                                'You equipped the {0}'.format(
                                    equipped.name)))

                    if dequipped:
                        message_log.add_message(
                            Message(
                                'You dequipped the {0}'.format(
                                    dequipped.name)))

                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(
                    targeting_item.item.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(
                    Message('Targeting cancelled'))

            # Add XP and possibly level up as a consequence
            if xp:
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(
                    Message(
                        'You gain {0} experience points.'.format(
                            xp)))

                if leveled_up:
                    message_log.add_message(Message(
                        'Your battle skills grow stronger! You reached level {0}'.format(
                            player.level.current_level) + '!', libtcod.yellow))
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP

        if game_state == GameStates.ENEMY_TURN:
            for entity in game_map.entities:
                if entity.ai:
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
                                redraw_entities = True
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        redraw_entities = True
                        break
            else:
                game_state = GameStates.PLAYERS_TURN
                redraw_entities = True

        """
        ### COMMENT TO HERE ###

def main():

    args = parse_args()

    if args.seed is None:
        args.seed = random.randrange(sys.maxsize)

    # Initialize random number generator
    print("Seed was:", args.seed)
    random.seed(args.seed)


    constants = get_constants()

    # libtcod.console_set_custom_font(
        # 'data/fonts/arial12x12.png', 
        # libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_set_custom_font(
        # 'data/fonts/Yayo-c64-640x200.png', 
        # 'data/fonts/Yayo-c64-1280x400-83b157.png', 
        # 'data/fonts/Alloy-curses-12x12.png', 
        # 'data/fonts/terminal16x16_gs_ro.png', 
        'data/fonts/16x16-sb-ascii.png', # good!
        # 'data/fonts/16x16-RogueYun-AgmEdit.png', # good!
        libtcod.FONT_LAYOUT_ASCII_INROW)

    libtcod.console_init_root(
        constants['screen_width'], constants['screen_height'], 
        constants['window_title'], False)

    terrain_layer = libtcod.console_new(
        constants['screen_width'], 
        constants['screen_height'])
    
    panel = libtcod.console_new(
        constants['screen_width'], 
        constants['panel_height'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False

    main_menu_background_image = libtcod.image_load('menu_background1.png')

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if show_main_menu:
            main_menu(terrain_layer, main_menu_background_image, constants['screen_width'],
                      constants['screen_height'])

            if show_load_error_message:
                message_box(terrain_layer, 'No save game to load', 50, constants['screen_width'], constants['screen_height'])

            libtcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, game_map, message_log, game_state = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN

                game_map.export_txt('maps_txt/lastmap.txt')

                show_main_menu = False
            elif load_saved_game:
                try:
                    player, game_map, message_log, game_state = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break

        else:
            libtcod.console_clear(terrain_layer)
            play_game(
                player, game_map, message_log, game_state,
                terrain_layer, panel, constants)

            show_main_menu = True


if __name__ == '__main__':
    main()
