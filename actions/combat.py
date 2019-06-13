from .action import Action

from game_state import GamePhase

import tcod as libtcod

from game_messages import Message

from components.fighter import NoRangedWeaponsEquippedException

class ShootAction(Action):

    def _execute(self):

        messages = list()

        if self.game_state.entity_targeted:
            # TODO implement shooting
            try:
                messages.extend(
                    self.player.fighter.shoot(self.game_state.entity_targeted))
                next_state = GamePhase.ENEMY_TURN
            except NoRangedWeaponsEquippedException:
                messages.append(
                    Message("You don't have any ranged weapons equipped!",
                            libtcod.red))
                next_state = GamePhase.PLAYERS_TURN
                pass
            pass
        else:
            messages.append(
                Message("Target something first!", libtcod.red))

            next_state = GamePhase.PLAYERS_TURN

        # Return outcome
        outcome = {
            # 'fov_recompute': position_changed,  # TODO this might change
            'redraw_terrain': True,
            'messages': messages,
            "next_state": next_state,
            # 'entity_targeted': new_target,
        }

        return outcome


class CycleTargetAction(Action):

    def __init__(self, cycle_dir, **kwargs):
        """
        cycle_dir : int
            Either 1 or -1, determines the direction of the cycle
        """

        self.cycle_dir = cycle_dir

    def _execute(self):

        messages = list()

        # The list of enemies in sight
        enemies_in_sight = list()

        i_targeted = i = 0
        for entity in self.game_map.entities:

            # TODO also check if hostile
            if (
                entity.ai and
                libtcod.map_is_in_fov(self.fov_map, entity.x, entity.y)):

                # Only enemies in sight
                enemies_in_sight.append(entity)

                if self.game_state.entity_targeted == entity:
                    # print("Found old target!")
                    # Remember the entity currently being targeted
                    i_targeted = i

                i += 1

        if len(enemies_in_sight) > 0:
            # Select the next one
            i_targeted = (i_targeted + self.cycle_dir) % len(enemies_in_sight)

            # print("{} enemies in sight, targeting # {}".format(
                # len(enemies_in_sight), i_targeted+1))
            new_target = enemies_in_sight[i_targeted]
        else:
            new_target = None
            messages.append(
                Message("No valid targets in sight.", libtcod.red))

        # Return outcome
        outcome = {
            # 'fov_recompute': position_changed,  # TODO this might change
            'redraw_terrain': True,
            'messages': messages,
            'entity_targeted': new_target,
        }

        return outcome
