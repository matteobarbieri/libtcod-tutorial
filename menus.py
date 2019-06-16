# import libtcodpy as libtcod
import tcod as libtcod

from equipment_slots import SLOT_NAMES

def menu(con, header, options, width, screen_width, screen_height,
         x=None, y=None, header_fg=libtcod.white):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap)
    # and one line per option
    header_height = libtcod.console_get_height_rect(
        con, 0, 0, width, screen_height, header)

    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(
        window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all the options
    opt_y = header_height

    # Add letters if not already present
    if type(options[0]) != tuple:
        options = [(chr(i+ord('a')), o_txt)
            for i, o_txt in enumerate(options)]

    for option_letter, option_text in options:
        text = "({}) {}".format(option_letter, option_text)
        libtcod.console_print_ex(
            window, 0, opt_y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        opt_y += 1

    # blit the contents of "window" to the root console
    if x is None:
        x = int(screen_width / 2 - width / 2)
    if y is None:
        y = int(screen_height / 2 - height / 2)

    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.4)


def item_submenu(con, header, player, item, screen_width, screen_height):

    item_position = player.inventory.get_item_position_in_list(item) + 20

    # TODO limit the height of the submenu
    item_position = min(item_position, 20000)

    # TODO
    # Get the right list of options for specific item
    # item_options = [
        # ('d', 'Drop'),
        # ('e', 'Equip'),
        # ('u', 'Use'),
    # ]

    item_options = item.item.get_inventory_options()

    width = 15

    # TODO
    # X position should depend on frame's width
    menu(con, header, item_options, width, screen_width, screen_height,
         x=31, y=item_position)

def inventory_menu(con, header, player, inventory_frame,
                   screen_width, screen_height):

    # Extract width and height
    w = inventory_frame.width
    h = inventory_frame.height

    # Draw frame
    inventory_frame.draw_frame(
        1, 1,
        w-2, h-2,
        'Inventory')

    # List the items in the inventory
    # Starting
    item_y = 5

    if player.inventory.items:
        for e in player.inventory.items:
            if not e.equipped:
                inventory_frame.print(
                    3, item_y, '({}) {}'.format(e.item_letter, e.name),
                    fg=e.color)

                item_y += 1

    # List equipped items
    if player.equipment.slots:

        inventory_frame.print(
                3, 28, 'Equipped items:',
            fg=libtcod.white)

        item_y = 30
        for slot, e in player.equipment.slots.items():
            inventory_frame.print(
                3, item_y, '({}) {} ({})'.format(
                    e.item_letter, e.name, SLOT_NAMES[slot]),
                fg=e.color)

            item_y += 1

    else:
        inventory_frame.print(
                3, 28, 'No items equipped!',
            fg=libtcod.white)

    # Blit panel console on root console
    libtcod.console_blit(
        inventory_frame,
        0, 0, w, h,
        con,
        0, 0)


def main_menu(con, background_image, screen_width, screen_height):
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2)
                             - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             'Rogue 20177')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2),
                             libtcod.BKGND_NONE, libtcod.CENTER,
                             'By heXe')

    menu(con, '',
         ['Play a new game', 'Continue last game', 'Quit'], 24,
         screen_width, screen_height)


def character_screen(player,
                     character_screen_width, character_screen_height,
                     screen_width, screen_height):

    # Create new console for showing character info
    window = libtcod.console_new(
        character_screen_width, character_screen_height)

    # Foreground color: white
    libtcod.console_set_default_foreground(
        window, libtcod.white)

    # Header of the character info section
    libtcod.console_print_rect_ex(
        window, 0, 1, character_screen_width, character_screen_height,
        libtcod.BKGND_NONE, libtcod.LEFT, 'Character Information')

    # Character level
    libtcod.console_print_rect_ex(
        window, 0, 2, character_screen_width, character_screen_height,
        libtcod.BKGND_NONE, libtcod.LEFT,
        'Level: {0}'.format(player.level.current_level))

    # Character experience
    libtcod.console_print_rect_ex(
        window, 0, 3, character_screen_width, character_screen_height,
        libtcod.BKGND_NONE, libtcod.LEFT,
        'Experience: {0}'.format(player.level.current_xp))

    # Experience to next level
    libtcod.console_print_rect_ex(
        window, 0, 4, character_screen_width, character_screen_height,
        libtcod.BKGND_NONE, libtcod.LEFT,
        'Experience to Level: {0}'.format(
            player.level.experience_to_next_level))

    # Maximum HP
    libtcod.console_print_rect_ex(
        window, 0, 6, character_screen_width, character_screen_height,
        libtcod.BKGND_NONE, libtcod.LEFT,
        'Maximum HP: {0}'.format(player.fighter.max_hp))

    # Attack value
    libtcod.console_print_rect_ex(
        window, 0, 7, character_screen_width, character_screen_height,
        libtcod.BKGND_NONE, libtcod.LEFT,
        'Attack: {0}'.format(player.fighter.power))

    # Defense value
    libtcod.console_print_rect_ex(
        window, 0, 8, character_screen_width, character_screen_height,
        libtcod.BKGND_NONE, libtcod.LEFT,
        'Defense: {0}'.format(player.fighter.defense))

    # Calculate character screen position w.r.t. the main screen
    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2

    # Blit character console on root console
    libtcod.console_blit(
        window, 0, 0, character_screen_width, character_screen_height,
        0, x, y, 1.0, 0.7)


def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)
