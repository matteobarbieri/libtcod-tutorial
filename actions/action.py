from game_states import GameStates

class Action():
    
    def __init__(self):
        self.game_map = None
        self.player = None

    def set_context(self, game_map, player, message_log):
        # self.context['game_map'] = game_map
        # self.context['player'] = player

        self.game_map = game_map
        self.player = player
        self.message_log = message_log

    def execute(self):
        pass

class NoopAction(Action):
    pass

class WaitAction(Action):
    """
    Wait one turn without doing anything
    """

    def execute(self):
        # Return outcome
        outcome = {
            "next_state": GameStates.ENEMY_TURN,
        }

        return outcome

