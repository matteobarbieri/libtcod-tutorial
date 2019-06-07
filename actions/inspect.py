from .action import Action

from game_state import GamePhase

from entity import get_blocking_entities_at_location

import tcod as libtcod

from game_messages import Message

import random


class InspectAction(Action):

    def __init__(self, x, y):

        self.coords = (x, y)

    def _execute(self):

        # Determine direction
        x, y = self.coords

        target_x = self.game_map.top_x + x
        target_y = self.game_map.top_y + y

        messages = list()

        target = get_blocking_entities_at_location(
            self.game_map.entities, target_x, target_y)

        if target:
            next_state = GamePhase.ENTITY_INFO
            # TODO tmp to remove
            messages.append(
                Message("There's a {} here...".format(
                    target.name), libtcod.yellow))
        else:
            messages.append(
                Message("There's nothing here...", libtcod.yellow))
            next_state = GamePhase.PLAYERS_TURN

        # Return outcome
        outcome = {
            "next_state": next_state,
            "messages": messages,
            "entity_focused": target,
        }

        return outcome
