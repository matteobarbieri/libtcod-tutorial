from .action import Action

from game_states import GameStates

class MoveAction(Action):

    def __init__(self, **kwargs):
        
        self.direction = kwargs['direction']

    def execute(self):

        # Determine direction
        dx, dy = self.direction

        # Compute destination coordinates
        destination_x = self.player.x + dx
        destination_y = self.player.y + dy

        # Return outcome
        outcome = {
            "next_state": GameStates.ENEMY_TURN,
            "results": [],
            'fov_recompute': True,
            'redraw_terrain': True,
        }

        # TODO check terrain/enemies!!!
        # Update player's position
        self.player.x = destination_x
        self.player.y = destination_y

        return outcome

