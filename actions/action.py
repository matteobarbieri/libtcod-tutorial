from game_state import GamePhase


class Action():

    def __init__(self):
        self.game_map = None
        self.player = None

    def set_context(self, game_map, player, message_log, fov_map,
                    entity_targeted):
        # self.context['game_map'] = game_map
        # self.context['player'] = player

        self.game_map = game_map
        self.player = player
        self.message_log = message_log
        self.fov_map = fov_map
        self.entity_targeted = entity_targeted

    def _execute(self):
        """
        The actual code that must be reimplemented by children classes.

        Returns the outcome
        """
        return {}

    def execute(self):
        """
        Wrapper function. The actual outcome is computed by the _execute
        method, saved (in order to allow replay) and returned.
        """

        self.outcome = self._execute()
        return self.outcome


class NoopAction(Action):
    pass


class WaitAction(Action):
    """
    Wait one turn without doing anything
    """

    def _execute(self):
        # Return outcome
        outcome = {
            "next_state": GamePhase.ENEMY_TURN,
            "redraw_terrain": True,
        }

        return outcome
