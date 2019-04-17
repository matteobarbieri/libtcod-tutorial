import libtcodpy as libtcod

from map_objects.tile import Wall

from enum import Enum, auto

from game_states import GameStates

from menus import character_screen, inventory_menu, level_up_menu

class RenderOrder(Enum):
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def get_names_under_mouse(mouse, entities, fov_map, top_x, top_y):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities if entity.x == (top_x + x) and entity.y ==
             (top_y + y) and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


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
    libtcod.console_print_ex(panel,
                             int(x + total_width / 2),
                             y,
                             libtcod.BKGND_NONE,
                             libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name,
                                                   value,
                                                   maximum))

def clear_entity(con, entity, game_map, fov_map, top_x=0, top_y=0):
    # erase the character that represents this object
    # libtcod.console_put_char(
        # con, entity.x-top_x, entity.y-top_y, ' ', libtcod.BKGND_NONE)

    # Simply redraw the corresponding map tile above it
    visible = libtcod.map_is_in_fov(fov_map, entity.x, entity.y)

    if visible or game_map.tiles[entity.x][entity.y].explored:
        # If visible or explored, redraw map tile
        game_map.tiles[entity.x][entity.y].render_at(
            con, entity.x-top_x, entity.y-top_y, visible)
    else:
        # Else, just draw a black space at that position
        libtcod.console_put_char(
            con, entity.x-top_x, entity.y-top_y, ' ', libtcod.BKGND_DEFAULT)

def clear_all(con, entities, game_map, fov_map, top_x, top_y):
    for entity in entities:
        clear_entity(con, entity, game_map, fov_map, top_x, top_y)

def draw_entity(terrain_layer, entity, 
                fov_map, game_map, top_x=0, top_y=0):

    # Only draw entities that are in player's fov
    if  libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or \
        (entity.c['stairs'] and game_map.tiles[entity.x][entity.y].explored):
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
            
def render_all(terrain_layer, panel, player, 
               game_map, fov_map, fov_recompute, 
               redraw_terrain, redraw_entities, message_log,
               constants, mouse,
               game_state):

    ### Extract variables from contants dict
    screen_width = constants['screen_width']
    screen_height = constants['screen_height']
    panel_height = constants['panel_height']
    bar_width = constants['bar_width']
    panel_y = constants['panel_y']

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

        libtcod.console_clear(terrain_layer)

        for y in range(top_y, top_y + screen_height - panel_height):
            for x in range(top_x, top_x + screen_width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)

                if visible:
                    # Render it as visible
                    # game_map.tiles[x][y].render_at(terrain_layer, x, y, visible)
                    game_map.tiles[x][y].render_at(terrain_layer, x-top_x, y-top_y, visible)
                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    # Render as currently out of sight
                    game_map.tiles[x][y].render_at(terrain_layer, x-top_x, y-top_y, visible)

    #########################################
    ######### Render entities  #########
    #########################################
    if redraw_terrain or redraw_entities:
        # libtcod.console_clear(entities_layer)
        # Sort entities by their associated render order
        entities_in_render_order = sorted(
            game_map.entities, key=lambda x: x.render_order.value)

        # Draw all entities in the list in the correct order
        for entity in entities_in_render_order:
            # draw_entity(terrain_layer, entity, fov_map, game_map, top_x, top_y)
            draw_entity(terrain_layer, entity, fov_map, game_map, top_x, top_y)

        libtcod.console_blit(terrain_layer, 0, 0, screen_width, screen_height, 0, 0, 0)

        # Delete them from the layer right after drawing them
        # Draw all entities in the list in the correct order
        for entity in entities_in_render_order:
            # draw_entity(terrain_layer, entity, fov_map, game_map, top_x, top_y)
            draw_entity(terrain_layer, entity, fov_map, game_map, top_x, top_y)

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

    libtcod.console_blit(
        panel,
        0,
        0,
        screen_width,
        panel_height,
        0,
        0,
        panel_y)

    # Show inventory menu
    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'

        inventory_menu(
            terrain_layer, inventory_title, player, 
            50, screen_width, screen_height)

    # Show level up menu
    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(
                terrain_layer, 'Level up! Choose a stat to raise:', 
                player, 40, screen_width, screen_height)

    # Show character screen
    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)

    clear_all(terrain_layer, game_map.entities, game_map, fov_map, top_x, top_y)

    return top_x, top_y


