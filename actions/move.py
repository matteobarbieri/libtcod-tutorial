from .action import Action

from game_states import GameStates

from entity import get_blocking_entities_at_location


class MoveAction(Action):

    def __init__(self, **kwargs):
        
        self.direction = kwargs['direction']

    def execute(self):

        # Determine direction
        dx, dy = self.direction

        # Save the original coordinates of the player
        source_x = self.player.x
        source_y = self.player.y

        # Compute destination coordinates
        destination_x = self.player.x + dx
        destination_y = self.player.y + dy

        # If it is not blocked, do something, either move to a new location,
        # attack an enemy or interact with an entity
        if not self.game_map.is_blocked(destination_x, destination_y):
            target = get_blocking_entities_at_location(
                self.game_map.entities, destination_x, destination_y)

            if target:
                # TODO replace with something more generic, like 'interact'
                # attack_results = player.fighter.attack(target)
                # player_turn_results.extend(attack_results)
                pass
            else:

                # Update player's position
                self.player.x = destination_x
                self.player.y = destination_y
        else:
            pass

        # Check if the position has changed
        position_changed = (
            source_x != self.player.x or source_y != self.player.y)


        # Return outcome
        outcome = {
            "next_state": GameStates.ENEMY_TURN,
            "results": [],
            'fov_recompute': position_changed, # TODO this might change
            'redraw_terrain': position_changed,
        }

        # TODO check terrain/enemies!!!

        return outcome

