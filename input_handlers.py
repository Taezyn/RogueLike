import tcod as libtcod
from game_states import GameStates

'''
Ce module gere la lecture des touches du clavier et de la souris
'''

def handle_keys(key, game_state):
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


'''
Permet d'annuler le ciblage d'un monstre avec un parchemin
'''
def handle_targeting_keys(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}


'''
Etat courrant du jeu, permet de se deplacer et d'ouvrir les differents menus
'''
def handle_player_turn_keys(key):
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


'''
Choix de la stat a augmenter lors d'un level-UP
'''
def handle_level_up_menu(key):
    if key:
        key_char = chr(key.c)
        if key_char == 'a':
            return {'level_up': 'hp'}
        elif key_char == 'b':
            return {'level_up': 'str'}
        elif key_char == 'c':
            return {'level_up': 'def'}
    return {}


'''
Lorsque l'on affiche l'ecran du personnage on ne
peut qu'appuyer sur echap pour quitter ce menu
'''
def handle_character_screen(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}

'''
Gere la position du clic de la souris
'''
def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)
    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}
    return {}


'''
Gere en permanance l'affichage de l'inventaire,
le plein ecran et le menu prinipal
'''
def handle_player_dead_keys(key):
    key_char = chr(key.c)
    if key_char == 'i':
        return {'show_character_screen': True}
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}


'''
Permet de gerer la saisie d'un objet dans l'inventaire
'''
def handle_inventory_keys(key):
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


'''
Permet de gerer le choix dans le menu principal
'''
def handle_main_menu(key):
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
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'back_to_game': True}
    return {}


'''
Idem que pour le menu d'info personnage
'''
def handle_commands_menu(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'back_to_game': True}
    return {}
