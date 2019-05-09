import random

from .mob_states import MobState
from .actions import AIMoveAction, AIAction

# TODO used in old code
# from game_messages import Message
# import libtcodpy as libtcod


class DestinationReachedException(Exception):
    """
    Used to signal that the destination has been reached
    """
    pass


class BasicMonster:

    def __init__(self, location, state=MobState.LOITERING):

        # Set starting "boredom" (required to changed state)
        self.boredom = -1

        # The MapPart where the mob currently is
        self.location = location

        # The location where the mob desires to go
        self.target_location = None

        # Set mob's initial state
        self.state = state

    def loiter(self, game_map):

        # Unpack room coordinates
        x1, y1, x2, y2 = self.location.xy

        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)

        destination_x = self.owner.x + dx
        destination_y = self.owner.y + dy

        # Remain withing the room
        if destination_x <= x1 or destination_x >= x2:
            destination_x = self.owner.x
            dx = 0

        if destination_y <= y1 or destination_y >= y2:
            destination_y = self.owner.y
            dy = 0

        return AIMoveAction(direction=(dx, dy), game_map=game_map,
                mob=self.owner)

    def transfer(self, game_map):
        """
        Move towards a new location
        """

        destinations_tomin, destinations_tostill = \
            self.target_location.d_map.downhill_from(
                self.owner.x, self.owner.y)

        # TODO use `destinations_tostill`

        if destinations_tomin:
            destination_x, destination_y = random.choice(destinations_tomin)

            # Compute displacement
            dx = destination_x - self.owner.x
            dy = destination_y - self.owner.y
        else:
            # The mob has arrived to destination
            raise DestinationReachedException()


        return AIMoveAction(direction=(dx, dy), game_map=game_map,
                mob=self.owner)


    def pick_action(self, player, game_map):

        ####################################
        ############ LOTERING ##############
        ####################################
        if self.state == MobState.LOITERING:
            # While loitering, accumulate a certain amount of boredom
            # After it reaches a certain level, go do something else
            if random.random() < self.boredom:

                # Reset boredom
                self.boredom = -1
                self.state = MobState.TRANSFERRING

                # Pick random destination
                while self.target_location is None:
                    target_room = random.choice(game_map.rooms)

                    # Do not pick current room
                    if self.location != target_room:
                        self.target_location = target_room
                        self.location = None

                return self.pick_action(player, game_map)
            else:
                self.boredom += 0.1
                return self.loiter(game_map)

        ####################################
        ############ LOTERING ##############
        ####################################
        if self.state == MobState.TRANSFERRING:
            try:
                return self.transfer(game_map)
            except DestinationReachedException:

                # Set the current location as previous target location
                self.location = self.target_location

                # Reset target_location to None
                self.target_location = None

                # And the current state to LOITERING
                self.state = MobState.LOITERING
                return self.pick_action(player, game_map)

        # Fallback Noop action
        return AIAction()

    """
    def take_turn(self, target, fov_map, game_map, entities):

        results = []

        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results
    """

"""
class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + random.randint(0, 2) - 1
            random_y = self.owner.y + random.randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': ('The {0} is no longer confused!'.format(self.owner.name), libtcod.red)})

        return results
"""
