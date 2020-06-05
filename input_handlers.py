import tcod as libtcod
from game_states import GameStates

"""
Ce module gere la lecture des touches du clavier et de la souris
"""

def handle_keys(key, game_state):
    """
    Définit le set touche auquel le programme doit réagir en fonction de l'état du jeu

    Parametres:
    ----------
    key : tcod.key
        Touche pressée

    Renvoi:
    -------
    dict

    """
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    elif game_state == GameStates.LEVEL_UP:
        return handle_level_up_menu(key)
    elif game_state == GameStates.CHARACTER_SCREEN:
        return handle_character_screen(key)
    elif game_state == GameStates.MENU_SCREEN:
        return handle_player_turn_keys(key)
    return {}


def handle_targeting_keys(key):
    """
    Permet d'annuler le ciblage en cours

    Parametres:
    ----------
    key : tcod.key

    Renvoi:
    -------
    dict

    """
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}


def handle_player_turn_keys(key):
    """
    Etat courant du jeu

    Parametres:
    ----------
    key : tcod.key

    Renvoi:
    -------
    dict

    """
    key_char = chr(key.c)
    if key.vk == libtcod.KEY_UP or key_char == 'z':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 's':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'q':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'd':
        return {'move': (1, 0)}
    elif key_char == 'a':
        return {'move': (-1, -1)}
    elif key_char == 'e':
        return {'move': (1, -1)}
    elif key_char == 'w':
        return {'move': (-1, 1)}
    elif key_char == 'c':
        return {'move': (1, 1)}
    elif key_char == 'x':
        return {'wait': True}

    if key_char == 'g':
        return {'pickup': True}
    elif key_char == 'b':
        return {'show_inventory': True}
    elif key_char == 'l':
        return {'drop_inventory': True}
    elif key.vk == libtcod.KEY_ENTER and not key.lalt:
        return {'take_stairs': True}
    elif key_char == 'i':
        return {'show_character_screen': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}


def handle_level_up_menu(key):
    """
    Choix de la statistique à augmenter lors d'un level-up

    Parametres:
    ----------
    key : tcod.key

    Renvoi:
    -------
    dict

    """
    if key:
        key_char = chr(key.c)
        if key_char == 'a':
            return {'level_up': 'hp'}
        elif key_char == 'b':
            return {'level_up': 'str'}
        elif key_char == 'c':
            return {'level_up': 'def'}
    return {}


def handle_character_screen(key):
    """
    Sortir de l'écran d'info de personnage

    Parametres:
    ----------
    key : tcod.key

    Renvoi:
    -------
    dict

    """
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}


def handle_mouse(mouse):
    """
    Gère la position du curseur et les clics de la souris

    Parametres:
    ----------
    mouse : tcod.mouse

    Renvoi:
    -------
    dict

    """
    (x, y) = (mouse.cx, mouse.cy)
    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}
    return {}


def handle_player_dead_keys(key):
    """
    Gère l'affichage de l'inventaire et le plein écran

    Parametres:
    ----------
    key : tcod.key

    Renvoi:
    -------
    dict

    """
    key_char = chr(key.c)
    if key_char == 'i':
        return {'show_character_screen': True}
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}


def handle_inventory_keys(key):
    """
    Gère le choix d'un item dans l'inventaire

    Parametres:
    ----------
    key : tcod.key

    Renvoi:
    -------
    dict

    """
    index = key.c - ord('a')
    if index >= 0:
        return {'inventory_index': index}
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}
    return {}


def handle_main_menu(key):
    """
    Gère le choix d'une option du menu principal

    Parametres:
    ----------
    key : tcod.key

    Renvoi:
    -------
    dict

    """
    key_char = chr(key.c)
    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c':
        return {'exit': True}
    elif key_char == 'd':
        return {'sound': True}
    elif key_char == 'e':
        return {'command': True}
    elif key_char == 'f':
        return {'scores': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'back_to_game': True}
    return {}


def handle_commands_menu(key):
    """
    Permet de sortir du menu des commandes

    Parametres:
    ----------
    key : tcod.key

    Renvoi:
    -------
    dict

    """
    if key.vk == libtcod.KEY_ESCAPE:
        return {'back_to_game': True}
    return {}
