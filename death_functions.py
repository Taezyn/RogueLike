import tcod as libtcod
from game_messages import Message
from game_states import GameStates
from render_functions import RenderOrder
import sound_manager.sound_manager as sm

sound = sm.init_son()
death_sounds = sound.get('death')[0]


def kill_player(player):
    """
    Gère la mort du joueur

    Parametres:
    ----------
    player : Entity

    Renvoi:
    -------
    Message

    """
    player.char = 268
    player.color = libtcod.dark_red
    death_sound = sm.Son(death_sounds)
    death_sound.playpause()
    return Message('Rekt', libtcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    """
    Gère la mort d'un monstre

    Parametres:
    ----------
    monster : Entity

    Renvoi:
    -------
    death_message : Message

    """
    death_message = Message('{0} est mort'.format(monster.name.capitalize()), libtcod.orange)
    monster.char = 268
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'Restes de ' + monster.name
    monster.render_order = RenderOrder.CORPSE
    return death_message
