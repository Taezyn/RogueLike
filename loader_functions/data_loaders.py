import shelve
import os


def save_game(player, entities, game_map, message_log, game_state):
    data_file = shelve.open('savegame', 'n')
    data_file['player_index'] = entities.index(player)
    data_file['entities'] = entities
    data_file['game_map'] = game_map
    data_file['message_log'] = message_log
    data_file['game_state'] = game_state
    data_file.close()


def load_game():
    if not('savegame.dat' in os.listdir()):
        raise FileNotFoundError
    else:
        data_file = shelve.open('savegame', 'r')
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']
        player = entities[player_index]
        data_file.close()
    return player, entities, game_map, message_log, game_state
