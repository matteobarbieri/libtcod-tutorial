# import libtcodpy as libtcod

import tcod as libtcod

import argparse

import random

import sys

from input_handlers import handle_input, handle_main_menu
from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box
from fov_functions import initialize_fov, recompute_fov

from render_functions import render_all, check_if_still_in_sight

from game_state import GamePhase, GameState
from death_functions import kill_monster, kill_player

from actions import ShowMenuException


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--seed', type=int)

    return parser.parse_args()


def update_game_state(
    outcome,
    game_state: GameState, fov_recompute, redraw_terrain,
    message_log):  # noqa

    # Update game state
    if outcome.get('next_state') is not None:
        game_state.game_phase = outcome.get('next_state')

    # Update focused entity
    if outcome.get('entity_focused') is not None:
        game_state.entity_focused = outcome.get('entity_focused')

    # Update targeted entity
    if outcome.get('entity_targeted') is not None:
        game_state.entity_targeted = outcome.get('entity_targeted')

    # Update selected inventory item
    if outcome.get('selected_inventory_item') is not None:
        game_state.selected_inventory_item = outcome.get(
            'selected_inventory_item')

    # Determine whether to recompute fov...
    if outcome.get('fov_recompute') is not None:
        fov_recompute = outcome.get('fov_recompute')
    else:
        fov_recompute = fov_recompute

    # Or redraw terrain
    if outcome.get('redraw_terrain') is not None:
        redraw_terrain = outcome.get('redraw_terrain')
    else:
        redraw_terrain = redraw_terrain

    # Add messages to the log
    if outcome.get('messages') is not None:
        for m in outcome.get('messages'):
            message_log.add_message(m)

    return fov_recompute, redraw_terrain


def play_game(player, game_map, game_state,
              message_log,
              terrain_layer, panel, entity_frame, inventory_frame,
              main_window, constants):

    # At the beginning of the game, recompute fov
    fov_recompute = True
    redraw_terrain = True
    redraw_entities = True

    # Entity being inspected
    game_state.entity_focused = None

    # Entity being targeted
    game_state.entity_targeted = None

    # Inventory item being selected
    game_state.selected_inventory_item = None

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # TODO temporarily disabled
    # previous_game_state = game_state

    # TODO temporarily disabled
    # targeting_item = None

    current_turn = 1
    # entities = game_map.entities

    ############################################
    ############### MAIN LOOP ##################
    ############################################

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(
            libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        ############################################
        ########### RENDER GAME WINDOW #############
        ############################################
        if fov_recompute:

            fov_map.compute_fov(
                player.x, player.y,
                constants['fov_radius'], constants['fov_light_walls'],
                constants['fov_algorithm'])

        # If the player move, check if targeted entity is still in sight
        if game_state.entity_targeted and redraw_terrain:
            game_state.entity_targeted = check_if_still_in_sight(
                fov_map, game_state.entity_targeted)
            # Check if by any chance target is dead
            # TODO more generally, if it is no longer targetable for any
            # reason
            if (
                game_state.entity_targeted and
                not game_state.entity_targeted.fighter):  # noqa

                game_state.entity_targeted = None

            # TODO same for focused entity?

        top_x, top_y = render_all(
            terrain_layer, panel, entity_frame, inventory_frame, main_window,
            player, game_map, fov_map, fov_recompute,
            redraw_terrain, redraw_entities, message_log,
            constants, mouse, game_state,
            current_turn)

        # TODO find a better place
        game_map.top_x = top_x
        game_map.top_y = top_y

        fov_recompute = False
        redraw_terrain = False
        redraw_entities = False

        libtcod.console_flush()

        ############################################
        ############## PLAYER'S TURN ###############
        ############################################
        if game_state.is_players_turn():

            ############################################
            ############# EXECUTE ACTIONS ##############
            ############################################
            action = handle_input(key, mouse, game_state.game_phase)

            # Add all objects required to perform any action
            # TODO check, should the message log be passed here?
            action.set_context(
                game_map, player, message_log, fov_map,
                game_state)

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

                fov_recompute, redraw_terrain = update_game_state(
                    outcome, game_state, fov_recompute, redraw_terrain,
                    message_log)

        ############################################
        ############## ENEMIES' TURN ###############
        ############################################
        elif game_state.is_enemies_turn():

            # Each entity takes a turn
            for entity in game_map.entities:
                if entity.ai:
                    # enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map)

                    # Pick an action for each entity
                    entity_action = entity.ai.pick_action(player, game_map)

                    # XXX no need to set context, asit was needed previously to
                    # choose the action

                    # Execute the action
                    outcome = entity_action.execute()

            # Go back to player's turn state
            game_state.game_phase = GamePhase.PLAYERS_TURN
            # redraw_entities = True
            redraw_terrain = True

            current_turn += 1

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
        'data/fonts/16x16-sb-ascii.png',  # good!
        # 'data/fonts/16x16-RogueYun-AgmEdit.png', # good!
        libtcod.FONT_LAYOUT_ASCII_INROW)

    # libtcod.console_init_root(
    #     constants['screen_width'], constants['screen_height'],
    #     constants['window_title'], False)

    libtcod.console_init_root(
        constants['screen_width'], constants['screen_height'],
        constants['window_title'], False, renderer=libtcod.RENDERER_SDL2)

    terrain_layer = libtcod.console_new(
        constants['terrain_layer_width'],
        constants['terrain_layer_height'])

    main_window = libtcod.console_new(
        constants['terrain_layer_width'],
        constants['terrain_layer_height'])

    panel = libtcod.console_new(
        constants['screen_width'],
        constants['panel_height'])

    entity_frame = libtcod.console_new(
        constants['frame_width'],
        constants['frame_height'])

    inventory_frame = libtcod.console_new(
        constants['frame_width'],
        constants['frame_height'])

    player = None
    game_map = None
    message_log = None

    show_main_menu = True
    show_load_error_message = False

    # main_menu_background_image = libtcod.image_load('menu_background1.png')
    main_menu_background_image = libtcod.image_load('menu_background2.png')

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(
            libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if show_main_menu:
            main_menu(terrain_layer, main_menu_background_image,
                      constants['screen_width'], constants['screen_height'])

            if show_load_error_message:
                message_box(
                    terrain_layer, 'No save game to load', 50,
                    constants['screen_width'], constants['screen_height'])

            libtcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if (show_load_error_message and
                (new_game or load_saved_game or exit_game)):
                # TODO wut?
                show_load_error_message = False
            elif new_game:
                # Start a new game
                player, game_map, message_log, game_phase = get_game_variables(
                    constants)
                game_phase = GamePhase.PLAYERS_TURN

                game_map.export_txt('maps_txt/lastmap.txt')

                show_main_menu = False
            elif load_saved_game:
                # Load a previously saved game
                try:
                    player, game_map, message_log, game_phase = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break

        else:
            # migrating to tcod
            # libtcod.console_clear(terrain_layer)
            terrain_layer.clear()

            game_state = GameState()
            # game_state.player = player
            game_state.game_phase = game_phase
            # game_state.game_map = game_map

            play_game(player, game_map,
                game_state, message_log,
                terrain_layer, panel, entity_frame, inventory_frame,
                main_window, constants)

            show_main_menu = True


if __name__ == '__main__':
    main()
