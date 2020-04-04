from enum import Enum, auto

'''
Ce module recense les etats du jeu et permet de faire connaitre au programme
dans quel etat il se trouve, et donc comment reagir face a tel ou tel input
'''

class GameStates(Enum):
    PLAYERS_TURN = auto()
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()
    SHOW_INVENTORY = auto()
    DROP_INVENTORY = auto()
    TARGETING = auto()
    LEVEL_UP = auto()
    CHARACTER_SCREEN = auto()
    MENU_SCREEN = auto()
