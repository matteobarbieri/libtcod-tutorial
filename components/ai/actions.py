from entity import get_blocking_entities_at_location


class AIAction():
    """
    An action performed by an entity
    """

    def __init__(self):
        pass

    def _execute(self):
        print("AI Action placeholder")

    def execute(self):
        self.outcome = self._execute()

        return self.outcome


class AIMoveAction(AIAction):

    def __init__(self, **kwargs):

        self.direction = kwargs['direction']
        self.game_map = kwargs['game_map']
        self.mob = kwargs['mob']

    def _execute(self):

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

        # TODO return outcome
