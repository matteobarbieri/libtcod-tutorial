from .action import Action
from .exceptions import ShowMenuException

from game_state import GamePhase

from loader_functions.data_loaders import save_game


class ShowMenuAction(Action):

    def _execute(self):

        # Go back to main menu
        # TODO When going back to main game it's always player's turn, maybe
        # consider removing it from the required arguments of `save_game`?
        save_game(self.player, self.game_map, self.message_log,
                  GamePhase.PLAYERS_TURN)

        # Raise an exception which will cause the game to exit the main loop
        raise ShowMenuException()


class ShowCharacterScreenAction(Action):

    def _execute(self):

        # Return outcome
        outcome = {
            'next_state': GamePhase.CHARACTER_SCREEN,
        }

        return outcome


class SelectInventoryItemAction(Action):

    def __init__(self, item_letter):
        self.item_letter = item_letter
        print("Item letter from action: {}".format(item_letter))

    def _execute(self):

        try:
            item_index = self.player.inventory.item_letters.index(
                self.item_letter)
            item = self.player.inventory.items[item_index]
            # print("Selected {}!".format(item))
            next_phase = GamePhase.INVENTORY_ITEM_MENU
        except ValueError as e:
            # print("Value error!")
            item = None
            next_phase = GamePhase.INVENTORY_MENU

        except IndexError as e:
            # print("Index error!")
            item = None
            next_phase = GamePhase.INVENTORY_MENU

        except Exception as e:
            print("Uncaught Exception!")
            raise e

        # Return outcome
        outcome = {
            'selected_inventory_item': item,
            'next_state': next_phase
        }

        return outcome


class ShowInventoryAction(Action):

    def _execute(self):

        # Return outcome
        outcome = {
            'selected_inventory_item': None,
            'next_state': GamePhase.INVENTORY_MENU,
        }

        return outcome


class BackToInventoryMenuAction(Action):

    def _execute(self):
        """
        Simply reset the state to show inventory menu
        """

        # Return outcome
        outcome = {
            'next_state': GamePhase.INVENTORY_MENU,
            'redraw_terrain': True,
        }

        return outcome


class BackToGameAction(Action):

    def _execute(self):
        """
        Simply reset the state to player's turn
        """

        # Return outcome
        outcome = {
            'next_state': GamePhase.PLAYERS_TURN,
            'redraw_terrain': True,
        }

        return outcome
