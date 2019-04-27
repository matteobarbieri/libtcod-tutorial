from .action import Action
from .exceptions import ShowMenuException

from game_states import GameStates

from loader_functions.data_loaders import save_game

class ShowMenuAction(Action):

    # def __init__(self, **kwargs):
        # pass

    def execute(self):

        # Go back to main menu
        # TODO When going back to main game it's always player's turn, maybe
        # consider removing it from the required arguments of `save_game`?
        save_game(self.player, self.game_map, self.message_log,
                  GameStates.PLAYERS_TURN)

        # Raise an exception which will cause the game to exit the main loop
        raise ShowMenuException()
        
