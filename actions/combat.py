from .action import Action

from game_states import GameStates

from entity import get_blocking_entities_at_location

import tcod as libtcod

from game_messages import Message

import random


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

                if self.entity_targeted == entity:
                    # print("Found old target!")
                    # Remember the entity currently being targeted
                    i_targeted = i

                i += 1

        if len(enemies_in_sight) > 0:
            # Select the next one
            i_targeted = (i_targeted + self.cycle_dir) % len(enemies_in_sight)

            # print("{} enemies in sight, targeting # {}".format(len(enemies_in_sight), i_targeted+1))
            new_target = enemies_in_sight[i_targeted]
        else:
            new_target = self.entity_targeted

        # Return outcome
        outcome = {
            # 'fov_recompute': position_changed,  # TODO this might change
            'redraw_terrain': True,
            'messages': messages,
            'entity_targeted': new_target,
        }

        return outcome
