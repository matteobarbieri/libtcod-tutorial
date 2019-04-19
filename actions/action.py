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
