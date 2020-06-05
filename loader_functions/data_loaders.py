import shelve
import os

def save_game(player, entities, game_map, message_log, game_state, score):
    """
    Sauvegarde la partie courante

    Parametres:
    ----------
    player : Entity

    entities : list

    gamp_map : GameMap

    message_log : MessageLog

    game_state : int

    score : int


    Renvoi:
    -------
    Aucun

    """
    data_file = shelve.open('savegame', 'n')
    data_file['player_index'] = entities.index(player)
    data_file['entities'] = entities
    data_file['game_map'] = game_map
    data_file['message_log'] = message_log
    data_file['game_state'] = game_state
    data_file['score'] = score
    data_file.close()


def save_score(score):
    """
    Sauvegarde le score d'une partie terminée

    Parametres:
    ----------
    socre : int

    Renvoi:
    -------
    Aucun

    """
    f = open('scores.txt', 'a')
    f.write(str(score[0]) + '\n')
    f.write(str(score[1]) + '\n')
    f.close()


def load_game():
    """
    Charge une sauvegarde

    Parametres:
    ----------
    Aucun

    Renvoi:
    -------
    player : Entity

    entities : list

    gamp_map : GameMap

    message_log : MessageLog

    game_state : int

    score : int


    """
    if not('savegame.dat' in os.listdir()):
        raise FileNotFoundError
    else:
        data_file = shelve.open('savegame', 'r')
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']
        score = data_file['score']
        player = entities[player_index]
        data_file.close()
    return player, entities, game_map, message_log, game_state, score


def delete_save():
    """
    Permet de supprimer un fichier de sauvegarde à l'issue d'une partie perdue.

    Parametres:
    ----------
    Aucun

    Renvoi:
    -------
    Aucun

    """
    if 'savegame.dat' in os.listdir() and 'savegame.bak' in os.listdir() and 'savegame.dir' in os.listdir():
        os.remove('savegame.dat')
        os.remove('savegame.dir')
        os.remove('savegame.bak')
