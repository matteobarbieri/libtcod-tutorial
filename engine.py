import libtcodpy as libtcod

from entity import get_blocking_entities_at_location
from input_handlers import handle_keys, handle_mouse
from loader_functions.initialize_new_game import get_constants, get_game_variables
from fov_functions import initialize_fov, recompute_fov
from render_functions import clear_all, render_all
from game_states import GameStates
from death_functions import kill_monster, kill_player

from game_messages import Message


def main():

    constants = get_constants()


    entities = [player]

    # Set font
    libtcod.console_set_custom_font(
        'data/fonts/arial10x10.png',
        libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
    )

    # Initialize main window
    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)

    # The main game screen
    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])

    # The UI screen
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])

    # When the game starts the fov must be computed for the first time
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    # Handles for keyboard and mouse inputs
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    previous_game_state = game_state

    # Required for targeting system
    targeting_item = None

    # Main loop
    while not libtcod.console_is_window_closed():

        # Wait for an event (keyboard or mouse)
        libtcod.sys_check_for_event(
            libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        # If the fov needs to be recomputed (for instance, because the player
        # moved, do it
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'],
                          constants['fov_algorithm'])

        # Render all entities on the map
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants['screen_width'], constants['screen_height'], constants['bar_width'],
                   constants['panel_height'], constants['panel_y'], mouse, constants['colors'], game_state)

        # Reset fov_recompute to False
        fov_recompute = False

        # ACtually print stuff on screen
        libtcod.console_flush()

        clear_all(con, entities)

        # Detect player's action
        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        move = action.get('move')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        # Click and right click actions
        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        player_turn_results = []

        # If it is player's turn and it is a move action, do it
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(
                    entities, destination_x, destination_y)

                # There is a blocking entity in destination tile
                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)

                # Destination tile is empty, can move
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        # Pickup an item on the ground
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

        # Show the inventory
        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        # Drop an item from the inventory
        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        # Choose a specific item in the inventory
        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(
                    player.inventory.use(
                        item, entities=entities, fov_map=fov_map))

            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        # Exit game
        if exit:
            if game_state in (
                    GameStates.SHOW_INVENTORY,
                    GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            # Cancel targeting if in TARGETING state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                return True
        
        # If in targeting, fire item
        if game_state == GameStates.TARGETING:
            # Fire whatever it is on left click
            if left_click:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(
                    targeting_item, entities=entities, fov_map=fov_map,
                    target_x=target_x, target_y=target_y)

                player_turn_results.extend(item_use_results)
            # Cancel action with right click
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})


        # Toggle full screen
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # Loop through all results
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('item_consumed')
            item_dropped = player_turn_result.get('item_dropped')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')

            if message:
                message_log.add_message(message)

            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('Targeting cancelled'))

            # Handle death of entities
            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)


            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN

        # Enemies' turn
        if game_state == GameStates.ENEMY_TURN:

            # Loop through all entities
            for entity in entities:

                # Only do something for those having an AI component,
                # For very obvious reasons
                if entity.ai:

                    # Get the results of an enemy's action
                    enemy_turn_results = entity.ai.take_turn(
                        player, fov_map, game_map, entities)

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

            # for-else loop end: switch back to player's turn after all
            # entities have performed their action
            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
