import os

import shelve

def save_game(player, game_map, message_log, game_state):
    # with shelve.open('savegame.dat', 'n') as data_file:
    with shelve.open('savegame', 'n') as data_file:
        data_file['player_index'] = game_map.entities.index(player)
        # data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state

def load_game():
    if not os.path.isfile('savegame.dat'):
        raise FileNotFoundError

    with shelve.open('savegame', 'r') as data_file:
        player_index = data_file['player_index']
        # entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']

    player = game_map.entities[player_index]

    return player, game_map, message_log, game_state
