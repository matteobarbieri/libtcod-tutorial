# import libtcodpy as libtcod
import tcod as libtcod

from enum import Enum, auto

from game_states import GameStates

from menus import character_screen, inventory_menu


class RenderOrder(Enum):
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def check_if_still_in_sight(fov_map, entity):
    """
    Checks if an entity is in sight and return it if it is true, else return
    None.
    """

    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        return entity
    else:
        return None

def get_entity_under_mouse(mouse, entities, fov_map, top_x, top_y):
    (x, y) = (mouse.cx, mouse.cy)

    entities_list = [
        entity for entity in entities if
            entity.x == (top_x + x) and
            entity.y == (top_y + y) and
            libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]

    if entities_list:
        sorted(entities_list, key=lambda e: e.render_order.value)
        return entities_list[-1]  # The last one
    else:
        return None


def get_names_under_mouse(mouse, entities, fov_map, top_x, top_y):
    (x, y) = (mouse.cx, mouse.cy)

    names = [
        entity.name for entity in entities if
            entity.x == (top_x + x) and
            entity.y == (top_y + y) and
            libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def render_entity_label(terrain_layer, entity, top_x, top_y):

    # Print the name of the entity on the top left tile
    libtcod.console_put_char(
        terrain_layer, entity.x-top_x-1, entity.y-top_y-1, '\\', libtcod.BKGND_DEFAULT)

    libtcod.console_print_ex(
        terrain_layer,
        # 0,
        # top_x - entity.x - 1, top_y - entity.y - 1,
        entity.x - top_x - 1,  entity.y - top_y - 2,
        libtcod.BKGND_NONE,
        libtcod.LEFT,
        '{}'.format(entity.name))


def render_entity_frame(entity_frame, entity):

    # Draw a rectangle of the background color for the full
    # length of the bar
    # libtcod.console_set_default_background(entity_frame, libtcod.red)
    # libtcod.console_rect(entity_frame, 3, 3, 7, 2,
                         # False, libtcod.BKGND_SCREEN)

    # Extract width and height
    w = entity_frame.width
    h = entity_frame.height

    # Draw frame
    entity_frame.draw_frame(
        1, 1,
        w-2, h-2,
        'Info')

    # Print the entiy's name
    entity_frame.print(
        3, 3, '{}'.format(entity.name))

    # Draw entity graphics
    # TODO
    # Mockup for entity detail
    entity_frame.draw_rect(
        3, 5, 10, 10, 0, bg=libtcod.red)


def render_bar(panel, x, y, total_width,
               name, value, maximum,
               bar_color, back_color):

    # Compute bar width, based on current value and maximum
    bar_width = int(float(value) / maximum * total_width)

    # Draw a rectangle of the background color for the full
    # length of the bar
    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1,
                         False, libtcod.BKGND_SCREEN)

    # Now draw the 'active' part of the bar
    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1,
                             False, libtcod.BKGND_SCREEN)

    # Draw the event log
    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(
        panel, int(x + total_width / 2), y,
        libtcod.BKGND_NONE,
        libtcod.CENTER,
        '{0}: {1}/{2}'.format(name, value, maximum))


# def clear_entity(con, entity, game_map, fov_map, top_x=0, top_y=0):
    # # erase the character that represents this object
    # # libtcod.console_put_char(
        # # con, entity.x-top_x, entity.y-top_y, ' ', libtcod.BKGND_NONE)

    # # Simply redraw the corresponding map tile above it
    # visible = libtcod.map_is_in_fov(fov_map, entity.x, entity.y)

    # if visible or game_map.tiles[entity.x][entity.y].explored:
        # # If visible or explored, redraw map tile
        # game_map.tiles[entity.x][entity.y].render_at(
            # con, entity.x-top_x, entity.y-top_y, visible)
    # else:
        # # Else, just draw a black space at that position
        # libtcod.console_put_char(
   #          con, entity.x-top_x, entity.y-top_y, ' ', libtcod.BKGND_DEFAULT)


# def clear_all(con, entities, game_map, fov_map, top_x, top_y):
    # for entity in entities:
        # clear_entity(con, entity, game_map, fov_map, top_x, top_y)


def draw_entity(terrain_layer, entity,
                fov_map, game_map, top_x=0, top_y=0):

    # Only draw entities that are in player's fov
    if (libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or
        (entity.stairs and game_map.tiles[entity.x][entity.y].explored)):
        # (entity.c['stairs'] and game_map.tiles[entity.x][entity.y].explored):
        # TODO include case for doors

        # print("Bgcolor: {}".format(bg_color))

        libtcod.console_put_char(
            terrain_layer,
            entity.x-top_x,
            entity.y-top_y,
            entity.char,
            libtcod.BKGND_NONE)

        libtcod.console_set_char_foreground(
            terrain_layer, entity.x-top_x, entity.y-top_y, entity.color)

def render_all(terrain_layer, panel, entity_frame, main_window,
               player,
               game_map, fov_map, fov_recompute,
               redraw_terrain, redraw_entities, message_log,
               constants, mouse,
               game_state, entity_focused, entity_targeted,
               current_turn):

    ### Extract variables from contants dict
    screen_width = constants['screen_width']
    screen_height = constants['screen_height']
    panel_height = constants['panel_height']
    bar_width = constants['bar_width']
    panel_y = constants['panel_y']
    terrain_layer_width = constants['terrain_layer_width']
    terrain_layer_height = constants['terrain_layer_height']
    frame_width = constants['frame_width']
    frame_height = constants['frame_height']

    #########################################
    ######### Render terrain first ##########
    #########################################

    # First compute the part of visible map, based on the player's position
    # Compute top left corner coordinates
    top_x = int(player.x - screen_width/2)
    top_x = max(0, top_x)
    top_x = min(game_map.width - screen_width, top_x)

    top_y = int(player.y - screen_height/2)
    top_y = max(0, top_y)
    top_y = min(game_map.height - screen_height + panel_height, top_y)

    # Only redraw terrain if needed
    if redraw_terrain:

        # Clear the console before drawing on it
        libtcod.console_clear(terrain_layer)

        for y in range(top_y, top_y + screen_height - panel_height):
            for x in range(top_x, top_x + screen_width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)

                if visible:
                    # Render it as visible
                    # game_map.tiles[x][y].render_at(terrain_layer, x, y, visible)
                    game_map.tiles[x][y].render_at(
                        terrain_layer, x-top_x, y-top_y, visible)
                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    # Render as currently out of sight
                    game_map.tiles[x][y].render_at(
                        terrain_layer, x-top_x, y-top_y, visible)

        if entity_targeted:
            visible = libtcod.map_is_in_fov(fov_map,
                entity_targeted.x, entity_targeted.y)

            if visible:
                # print("Targeted {} at ({}, {})".format(
                    # entity_targeted.name, entity_targeted.x, entity_targeted.y))

                libtcod.console_set_char_background(
                    terrain_layer,
                    entity_targeted.x-top_x, entity_targeted.y-top_y,
                    libtcod.red, libtcod.BKGND_SET)

    #########################################
    ########### Render entities  ############
    #########################################

    # if redraw_terrain or redraw_entities:
    if redraw_terrain:
        # libtcod.console_clear(entities_layer)
        # Sort entities by their associated render order
        entities_in_render_order = sorted(
            game_map.entities, key=lambda x: x.render_order.value)

        # Draw all entities in the list in the correct order
        for entity in entities_in_render_order:
            draw_entity(terrain_layer, entity,
                        fov_map, game_map, top_x, top_y)

        # # Blit terrain layer on root console
        # libtcod.console_blit(
            # terrain_layer,
            # 0, 0, screen_width, screen_height,
            # 0,
            # 0, 0)

    #########################################
    ############ Render panel  ##############
    #########################################

    # Now render the health bar
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(
            panel,
            message_log.x,
            y,
            libtcod.BKGND_NONE,
            libtcod.LEFT,
            message.text)
        y += 1

    # Render the HP bar
    render_bar(
        panel, 1, 1, bar_width,
        'HP', player.c['fighter'].hp, player.c['fighter'].max_hp,
        libtcod.light_red, libtcod.darker_red)

    # Show current dungeon level
    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Dungeon level: {0}'.format(game_map.dungeon_level))

    # Show current dungeon level
    libtcod.console_print_ex(panel, 1, 5, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Time: {0}'.format(current_turn))

    # Show info about entities under mouse cursor
    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(
        panel,
        1,
        0,
        libtcod.BKGND_NONE,
        libtcod.LEFT,
        get_names_under_mouse(
            mouse, game_map.entities, fov_map, top_x, top_y))

    # Blit panel console on root console
    libtcod.console_blit(
        panel, 0, 0,
        screen_width, panel_height,
        0,
        0, panel_y)

    #########################################
    ### Blit terrain layer on root console ##
    #########################################

    libtcod.console_blit(
        terrain_layer,
        0, 0, terrain_layer_width, terrain_layer_height,
        main_window,
        0, 0)

    #########################################
    ######### Render entity frame  ##########
    #########################################

    entity_under_mouse = get_entity_under_mouse(
            mouse, game_map.entities, fov_map, top_x, top_y)

    if entity_under_mouse:

        render_entity_label(
            main_window, entity_under_mouse,
            top_x, top_y)

    if game_state == GameStates.ENTITY_INFO:
        # TODO to move somewhere else!
        render_entity_frame(entity_frame, entity_focused)

        # Blit panel console on root console
        libtcod.console_blit(
            entity_frame,
            0, 0, frame_width, frame_height,
            main_window,
            screen_width - frame_width, 0)

    libtcod.console_blit(
        main_window,
        0, 0, terrain_layer_width, terrain_layer_height,
        0,
        0, 0)

    # Show inventory menu
    if game_state in (GameStates.INVENTORY_MENU, ):
        if game_state == GameStates.INVENTORY_MENU:
            inventory_title = 'Press the key next to an item to use it, '
            'or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, '
            'or Esc to cancel.\n'

        inventory_menu(
            terrain_layer, inventory_title, player,
            50, screen_width, screen_height)

    # Show character screen
    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)

    # TODO possibly no longer needed because of rendering overhaul
    # clear_all(terrain_layer, game_map.entities, game_map,
              # fov_map, top_x, top_y)

    return top_x, top_y
