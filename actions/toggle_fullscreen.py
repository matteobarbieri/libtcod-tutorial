from .action import Action

import libtcodpy as libtcod

class ToggleFullscreenAction(Action):

    # def __init__(self, **kwargs):
        # pass

    def execute(self):

        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

