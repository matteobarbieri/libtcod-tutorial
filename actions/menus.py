from .action import Action
from .exceptions import ShowMenuException

from game_states import GameStates

from loader_functions.data_loaders import save_game


class ShowMenuAction(Action):

    def _execute(self):

        # Go back to main menu
        # TODO When going back to main game it's always player's turn, maybe
        # consider removing it from the required arguments of `save_game`?
        save_game(self.player, self.game_map, self.message_log,
                  GameStates.PLAYERS_TURN)

        # Raise an exception which will cause the game to exit the main loop
        raise ShowMenuException()


class ShowCharacterScreenAction(Action):

    def _execute(self):

        # Return outcome
        outcome = {
            'next_state': GameStates.CHARACTER_SCREEN,
        }

        return outcome


class SelectInventoryItemAction(Action):

    def __init__(self, inventory_item_index):
        self.inventory_item_index = inventory_item_index

    def _execute(self):

        try:
            self.item = self.player.inventory.items[self.inventory_item_index]
            print("Selected {}!".format(self.item))
        except Exception as e:
            print("Uncaught Exception!")
            raise e

        # Return outcome
        outcome = {
            'selected_inventory_item': self.item,
            'next_state': GameStates.INVENTORY_ITEM_MENU,
        }

        return outcome


class ShowInventoryAction(Action):

    def _execute(self):

        # Return outcome
        outcome = {
            'selected_inventory_item': None,
            'next_state': GameStates.INVENTORY_MENU,
        }

        return outcome


class BackToGameAction(Action):

    def _execute(self):
        """
        Simply reset the state to player's turn
        """

        # Return outcome
        outcome = {
            'next_state': GameStates.PLAYERS_TURN,
            'redraw_terrain': True,
        }

        return outcome
