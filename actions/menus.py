from .action import Action
from .exceptions import ShowMenuException

from game_states import GameStates

from loader_functions.data_loaders import save_game

class ShowMenuAction(Action):

    def execute(self):

        # Go back to main menu
        # TODO When going back to main game it's always player's turn, maybe
        # consider removing it from the required arguments of `save_game`?
        save_game(self.player, self.game_map, self.message_log,
                  GameStates.PLAYERS_TURN)

        # Raise an exception which will cause the game to exit the main loop
        raise ShowMenuException()
        
class ShowInventoryAction(Action):

    def execute(self):

        # Return outcome
        outcome = {
            'next_state': GameStates.SHOW_INVENTORY,
        }

        return outcome


class BackToGameAction(Action):

    def execute(self):
        """
        Simply reset the state to player's turn
        """

        # Return outcome
        outcome = {
            'next_state': GameStates.PLAYERS_TURN,
            'redraw_terrain': True,
        }

        return outcome
