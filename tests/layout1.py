import sys, os

# Append parent folder
sys.path.append(
    os.path.join(os.path.dirname(__file__), '..'))

import libtcodpy as libtcod

from loader_functions.initialize_new_game import get_constants, get_game_variables


def main():
    constants = get_constants()

    # libtcod.console_set_custom_font('data/fonts/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_set_custom_font(
        # 'data/fonts/Alloy-curses-12x12.png', 
        'data/fonts/16x16-sb-ascii.png', # good!
        libtcod.FONT_LAYOUT_ASCII_INROW
        )

    screen_width = 80
    screen_height = 30

    libtcod.console_init_root(
        screen_width, screen_height, 
        constants['window_title'], False)

    ui_left = libtcod.console_new(
        int(screen_width/2), 
        screen_height-10)
    
    ui_right = libtcod.console_new(
        int(screen_width/2), 
        screen_height-10)

    ui_panel = libtcod.console_new(
        int(screen_width), 
        10)

    ui_over = libtcod.console_new(
        int(screen_width/2), 
        screen_height-10)
    
    libtcod.console_set_default_background(ui_left, libtcod.red)
    libtcod.console_rect(ui_left, 0, 0, 40, 20, False, libtcod.BKGND_SET)

    libtcod.console_set_default_background(ui_right, libtcod.blue)
    libtcod.console_rect(ui_right, 0, 0, 40, 20, False, libtcod.BKGND_SET)

    libtcod.console_set_default_background(ui_panel, libtcod.green)
    libtcod.console_rect(ui_panel, 0, 0, 80, 10, False, libtcod.BKGND_SET)

    libtcod.console_set_default_background(ui_over, libtcod.yellow)
    libtcod.console_set_key_color(ui_over, libtcod.black)
    libtcod.console_rect(ui_over, 2, 2, 2, 2, False, libtcod.BKGND_SET)

    # Write @ on left ui part
    libtcod.console_set_default_foreground(ui_left, libtcod.white)
    libtcod.console_put_char(ui_left, 6, 6, '@', libtcod.BKGND_DEFAULT)

    # Write K on over ui part
    libtcod.console_set_default_foreground(ui_over, libtcod.pink)
    libtcod.console_put_char(ui_over, 6, 6, 'K', libtcod.BKGND_DEFAULT)
    libtcod.console_put_char(ui_over, 3, 3, 'K', libtcod.BKGND_DEFAULT)

    bg_color = libtcod.console_get_char_background(ui_right, 6, 6)
    libtcod.console_set_char_background(ui_over, 6, 6, bg_color)

    # Blit left on root
    libtcod.console_blit(
        ui_left, 0, 0, 
        40, 20, 0, 
        0, 0)

    # Blit over on right
    libtcod.console_blit(
        ui_over, 0, 0, 
        40, 20, ui_right, 
        0, 0)

    # Blit right on root
    libtcod.console_blit(
        ui_right, 0, 0, 
        40, 20, 0, 
        40, 0)

    # libtcod.console_blit(
        # ui_over, 0, 0, 
        # 40, 20, 0, 
        # 40, 0)


    # Blit console on root
    libtcod.console_blit(
        ui_panel, 0, 0, 
        80, 10, 0, 
        0, 20)

    libtcod.console_flush()

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Main loop
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(
            libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)


if __name__ == '__main__':
    main()
