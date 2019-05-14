from .action import Action

from game_states import GameStates

from entity import get_blocking_entities_at_location

import tcod as libtcod

from game_messages import Message

import random


class CycleTargetAction(Action):

    def __init__(self, **kwargs):

        pass

    def _execute(self):

        messages = list()

        # The list of enemies in sight
        enemies_in_sight = list()

        for entity in self.game_map.entities:

            # TODO also check if hostile
            if (
                entity.ai and
                libtcod.map_is_in_fov(self.fov_map, entity.x, entity.y)):

                # Only enemies in sight
                enemies_in_sight.append(entity)

        # TODO must cycle through enemies
        new_target = enemies_in_sight[0]

        # Return outcome
        outcome = {
            # 'fov_recompute': position_changed,  # TODO this might change
            'redraw_terrain': True,
            'messages': messages,
            'entity_targeted': new_target,
        }

        return outcome
