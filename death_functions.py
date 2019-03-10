import libtcodpy as libtcod

from render_functions import RenderOrder

from game_messages import Message

from game_states import GameStates


def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red

    # Create and return message for the log
    return Message('You died!', libtcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):

    # Create message for the log
    death_message = Message(
        '{0} is dead!'.format(
            monster.name.capitalize()),
        libtcod.orange)

    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message
