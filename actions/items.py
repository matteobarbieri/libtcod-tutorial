from .action import Action

from game_state import GamePhase

from entity import get_blocking_entities_at_location

import libtcodpy as libtcod

from game_messages import Message

import random

from components.inventory import InventoryFullException


class PickupAction(Action):

    def __init__(self, **kwargs):
        pass

    def _execute(self):

        # Save the original coordinates of the player
        x = self.player.x
        y = self.player.y

        messages = list()

        item_on_floor = self.game_map.get_item_at(x, y)

        # If there actually is an item on the floor, add it to the player's
        # inventory. Also now it's the enemies' turn (unless for some reason
        # the item can't be picked up).
        if item_on_floor:
            try:
                # (try to) add the item to the player's inventory
                messages.append(self.player.inventory.pickup(item_on_floor))

                # Remove the item from the game map (makes sense)
                self.game_map.entities.remove(item_on_floor)

                # Change game phase (enemies' turn)
                next_phase = GamePhase.ENEMY_TURN
            except InventoryFullException:
                # TODO improve inventory full message
                messages.append(
                    Message("Your inventory is full!", libtcod.yellow))
                next_phase = GamePhase.PLAYERS_TURN
        # Else just print a warning message
        else:
            messages.append(
                Message("There's nothing here to pick up!",
                        libtcod.yellow))
            next_phase = GamePhase.PLAYERS_TURN
            pass




        # Return outcome
        outcome = {
            "next_state": next_phase,
            'messages': messages,
        }

        # TODO check terrain/enemies!!!

        return outcome
