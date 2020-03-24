import tcod as libtcod
from game_messages import Message
from game_states import GameStates
from render_functions import RenderOrder
import sound_manager.sound_manager as sm

sound = sm.init_son()
death_sounds = sound.get('death')[0]


# Gere la mort du joueur
def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red
    death_sound = sm.Son(death_sounds)
    death_sound.playpause()
    return Message('Rekt', libtcod.red), GameStates.PLAYER_DEAD


# Gere la mort d'un monstre
def kill_monster(monster):
    death_message = Message('{0} est mort'.format(monster.name.capitalize()), libtcod.orange)
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'Restes de ' + monster.name
    monster.render_order = RenderOrder.CORPSE
    return death_message
