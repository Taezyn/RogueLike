import pygame
import random

'''
Ici sont recenses les chemins des differents sons du jeu dans init_son 
qui sera recupere dans chaque module utilisant un ou plusieurs sons.
'''


def init_son():
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


'''
Choisit un son aleatoire parmi une liste donnee
'''
def choose_sound(L):
    s = Son(random.choice(L))
    return s


'''
Coupe tous les sons en cours de lecture
'''
def close_sound():
    pygame.mixer.quit()


'''
Permet de creer un son a mixer
'''
class Son:
    def __init__(self, title):
        self.title = title
        self.read = False
        self.son = pygame.mixer.Sound(self.title)

    '''
    Permet de lire un son non joue ou d'arreter de lire un son joue.
    '''
    def playpause(self):
        if not self.read:
            self.son.play()
            self.read = True
        else:
            self.son.stop()
            self.read = False

if __name__ == '__main__':
    pygame.mixer.init()
    s = pygame.mixer.Sound('clean_stage.wav')
    s.play(loops=-1)
