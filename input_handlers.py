import tcod as libtcod

from game_state import GamePhase

from actions import *

def handle_input(key, mouse, game_state):
    """
    Handle inputs differently depending on game state
    """

    # TODO refactor as dispatch tables
    #########################################
    ############ PLAYER'S TURN ##############
    #########################################
    if game_state == GamePhase.PLAYERS_TURN:
        return handle_player_turn_keys(key, mouse)
    #########################################
    ############ INVENTORY MENU #############
    #########################################
    elif game_state in (GamePhase.INVENTORY_MENU, ):
        return handle_inventory_keys(key, mouse)
    #########################################
    ########## INVENTORY ITEM MENU ##########
    #########################################
    elif game_state == GamePhase.INVENTORY_ITEM_MENU:
        return handle_inventory_item_keys(key, mouse)
    #########################################
    ########### CHARACTER SCREEN ############
    #########################################
    elif game_state == GamePhase.CHARACTER_SCREEN:
        return handle_character_screen(key, mouse)
    #########################################
    ############## ENTITY INFO ##############
    #########################################
    elif game_state == GamePhase.ENTITY_INFO:
        return handle_entity_info(key, mouse)

    # Return empty outcome dict
    return {}


def handle_entity_info(key, mouse):

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return ToggleFullscreenAction()
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu, go back to main game
        return BackToGameAction()

    # No key was pressed
    return NoopAction()

def handle_inventory_item_keys(key, mouse):

    # Code to prevent double input
    key_char = chr(key.c) if key.vk == libtcod.KEY_CHAR else ""

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return ToggleFullscreenAction()

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu, go back to main game
        return BackToInventoryMenuAction()

    if key_char == "d":
        return DropItemAction()
    elif key_char == "e":
        return EquipItemAction()
    elif key_char == "u":
        return UnequipItemAction()

    # No key was pressed
    return NoopAction()

def handle_inventory_keys(key, mouse):

    # letter_index = key.c - ord('a') if key.vk == libtcod.KEY_CHAR else -1
    letter_index = key.c if key.vk == libtcod.KEY_CHAR else -1

    # TODO To enable again
    if letter_index >= 0:
        return SelectInventoryItemAction(chr(letter_index))

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return ToggleFullscreenAction()
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu, go back to main game
        return BackToGameAction()

    # No key was pressed
    return NoopAction()


def handle_main_menu(key):
    key_char = chr(key.c)

    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c' or  key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}


def handle_level_up_menu(key):
    pass
    """
    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            return {'level_up': 'hp'}
        elif key_char == 'b':
            return {'level_up': 'str'}
        elif key_char == 'c':
            return {'level_up': 'def'}

    return {}
    """


def handle_character_screen(key, mouse):

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return ToggleFullscreenAction()
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu, go back to main game
        return BackToGameAction()

    # No key was pressed
    return NoopAction()

def handle_player_turn_keys(key, mouse):


    # Code to prevent double input
    key_char = chr(key.c) if key.vk == libtcod.KEY_CHAR else ""

    #########################################
    ############## MOVEMENT #################
    #########################################

    if key.vk == libtcod.KEY_UP or key_char == 'k':
        return MoveAction(direction=(0, -1))
    elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
        return MoveAction(direction=(0, 1))
    elif key.vk == libtcod.KEY_LEFT or key_char == 'h':
        return MoveAction(direction=(-1, 0))
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
        return MoveAction(direction=(1, 0))
    elif key_char == 'y':
        return MoveAction(direction=(-1, -1))
    elif key_char == 'u':
        return MoveAction(direction=(1, -1))
    elif key_char == 'b':
        return MoveAction(direction=(-1, 1))
    elif key_char == 'n':
        return MoveAction(direction=(1, 1))
    elif key_char == 'z':
        return WaitAction()

    #########################################
    ################ COMBAT #################
    #########################################

    # Targeting
    if key.vk == libtcod.KEY_TAB:

        if key.shift:
            # Select the previous one
            return CycleTargetAction(-1)
        else:
            # Select the next one
            return CycleTargetAction(1)

    elif key_char == 'f':
        return ShootAction()

    #########################################
    ########### GO TO MAIN MENU #############
    #########################################

    # Show main menu
    elif key.vk == libtcod.KEY_ESCAPE:
        return ShowMenuAction()

    #########################################
    ########## TOGGLE FULLSCREEN ############
    #########################################

    elif key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return ToggleFullscreenAction()

    #########################################
    ################# MISC ##################
    #########################################

    elif key_char == 'i':
        return ShowInventoryAction()

    elif key_char == 'c':
        return ShowCharacterScreenAction()

    elif key_char == 'g':
        return PickupAction()

    #########################################
    ############ MOUSE ACTIONS ##############
    #########################################

    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return InspectAction(x, y)
    # elif mouse.rbutton_pressed:
        # return {'right_click': (x, y)}

    #########################################
    ############ SELECT ENTITY ##############
    #########################################


    """
    elif key_char == 'g':
        return {'pickup': True}
    elif key_char == 'd':
        return {'drop_inventory': True}
    elif key.vk == libtcod.KEY_ENTER:
        return {'take_stairs': True}

    # Updated
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}
    """

    # No key was pressed
    return NoopAction()

def handle_targeting_keys(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_player_dead_keys(key):
    """
    The set of keys for a dead player.

    Can only see the inventory and toggle fullscreen.
    """

    key_char = chr(key.c) if key.vk == libtcod.KEY_CHAR else ""

    if key_char == 'i':
        return {'show_inventory': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}

def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}
