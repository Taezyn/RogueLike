import pygame
import random

"""
Ici sont recenses les chemins des differents sons du jeu dans init_son 
qui sera recupere dans chaque module utilisant un ou plusieurs sons.
"""


def init_son():
    """
    Permet de récuperer le dictionnaire contenant l'adresse de chacune des bandes sons utilisées

    Parametres:
    ----------
    Aucun

    Renvoi:
    -------
    sons : dict

    """
    sons = {'confuse': ['sound_manager/confuse_sound/confuse_sound_1.wav',
                        'sound_manager/confuse_sound/confuse_sound_2.wav',
                        'sound_manager/confuse_sound/confuse_sound_3.wav'],
            'fire': ['sound_manager/fire_sound/fire_sound_1.wav',
                     'sound_manager/fire_sound/fire_sound_2.wav',
                     'sound_manager/fire_sound/fire_sound_3.wav',
                     'sound_manager/fire_sound/fire_sound_4.wav'],
            'sword': ['sound_manager/sword_sound/sword_sound_1.wav',
                      'sound_manager/sword_sound/sword_sound_2.wav',
                      'sound_manager/sword_sound/sword_sound_3.wav',
                      'sound_manager/sword_sound/sword_sound_4.wav',
                      'sound_manager/sword_sound/sword_sound_5.wav',
                      'sound_manager/sword_sound/sword_sound_6.wav',
                      'sound_manager/sword_sound/sword_sound_7.wav',
                      'sound_manager/sword_sound/sword_sound_8.wav',
                      'sound_manager/sword_sound/sword_sound_9.wav'],
            'thunder': ['sound_manager/thunder_sound/thunder_sound_1.wav',
                        'sound_manager/thunder_sound/thunder_sound_2.wav',
                        'sound_manager/thunder_sound/thunder_sound_3.wav'],
            'background_music': ['sound_manager/background_music/background_music_1.wav',
                                 'sound_manager/background_music/background_music_2.wav',
                                 'sound_manager/background_music/background_music_3.wav',
                                 'sound_manager/background_music/background_music_4.wav'],
            'boss_fight': ['sound_manager/boss_fight/boss_fight_1.wav',
                           'sound_manager/boss_fight/boss_fight_2.wav'],
            'hurt': ['sound_manager/hurt_sound.wav'],
            'level_up': ['sound_manager/level_up_sound.wav'],
            'potion_drinking': ['sound_manager/potion_drinking_sound.wav'],
            'death': ['sound_manager/death_sound.wav'],
            'clean_stage': ['sound_manager/clean_stage.wav']}
    return sons


def choose_sound(L):
    """
    Choisi un son aléatoire parmis une liste donnée

    Parametres:
    ----------
    L : list

    Renvoi:
    -------
    s : Son

    """
    s = Son(random.choice(L))
    return s


def close_sound():
    """
    Coupe tous les sons en cours de lecture

    Parametres:
    ----------
    Aucun

    Renvoi:
    -------
    Aucun

    """
    pygame.mixer.quit()


class Son:
    """
    Crée un son
    """
    def __init__(self, title):
        """
        Initialise un son avec pygame.mixer

        Parametres:
        ----------
        title : str
            chemin d'accès de la bande son

        Renvoi:
        -------
        Aucun

        """
        self.title = title
        self.read = False
        self.son = pygame.mixer.Sound(self.title)

    def playpause(self):
        """
        Lit un son en pause, ou met en pause un son en cours de lecture

        Parametres:
        ----------
        Aucun

        Renvoi:
        -------
        Aucun
        """
        if not self.read:
            self.son.play()
            self.read = True
        else:
            self.son.stop()
            self.read = False
