import libtcodpy as libtcod

from random import randint

from game_messages import Message

from enum import Enum, auto

from entity import get_blocking_entities_at_location

class MobState(Enum):
    # The mob will walk around the room
    LOITERING = auto()

    # TODO add more

class AIAction():
    """
    An action performed by an entity
    """

    def __init__(self):
        pass

    def execute(self):
        print("AI Action placeholder")
        pass

class AIMoveAction(AIAction):
    
    def __init__(self, **kwargs):
        
        self.direction = kwargs['direction']
        self.game_map = kwargs['game_map']
        self.mob = kwargs['mob']

    def execute(self):

        # Determine direction
        dx, dy = self.direction

        # Compute destination coordinates
        destination_x = self.mob.x + dx
        destination_y = self.mob.y + dy

        self.mob.last_direction = (dx, dy)
        # Check for collision with other possible non-entity blocking objects in
        # the room
        if not self.game_map.is_blocked(destination_x, destination_y):
            target = get_blocking_entities_at_location(
                self.game_map.entities, destination_x, destination_y)

            if target:
                # Do not change last direction
                pass
            else:
                # Actually move
                self.mob.x = destination_x
                self.mob.y = destination_y


class BasicMonster:
    
    def __init__(self, location, state=MobState.LOITERING):

        # The MapPart where the mob currently is
        self.location = location

        # Set mob's initial state
        self.state = state

    def loiter(self, game_map):

        # Unpack room coordinates
        x1, y1, x2, y2 = self.location.xy

        dx = randint(-1, 1)
        dy = randint(-1, 1)

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


    def pick_action(self, player, game_map):

        if self.state == MobState.LOITERING:
            return self.loiter(game_map)

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
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer confused!'.format(self.owner.name), libtcod.red)})

        return results
"""
