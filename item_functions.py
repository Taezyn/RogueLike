from game_messages import *
from components.ai import ConfusedMonster
import sound_manager.sound_manager as sm

sound = sm.init_son()
confuse_sounds = sound.get('confuse')
fire_sounds = sound.get('fire')
thunder_sounds = sound.get('thunder')
potion_drinking_sounds = sound.get('potion_drinking')[0]

'''
Definit les comportements des items lorsqu'ils sont utilises
'''


'''
Potion de soin : restaure un quart de la vie
'''
def heal(*args, **kwargs):
    entity = args[0]
    results = []
    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('Deja full life', libtcod.yellow)})
    else:
        entity.fighter.heal()
        potion_drinking_sound = sm.Son(potion_drinking_sounds)
        potion_drinking_sound.playpause()
        results.append({'consumed': True, 'message': Message('25% PV rendus', libtcod.green)})
    return results


'''
Parchemin de foudre : inflige des degats a la cible la plus proche
'''
def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')
    results = []
    target = None
    closest_distance = maximum_range + 1
    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)
            if distance < closest_distance:
                target = entity
                closest_distance = distance
    if target:
        results.append({'consumed': True, 'target': target, 'message': Message(
                    'Un éclair inflige {0} a {1} !'.format(damage, target.name))})
        thunder_sound = sm.choose_sound(thunder_sounds)
        thunder_sound.playpause()
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message("Pas d'enemis a portee")})
    return results


'''
Parchemin de feu : tire une boule de feu qui explose d'un rayon donne a
l'endroit choisi avec la souris. Touche aussi le joueur
'''
def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    results = []
    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('Hors de portee', libtcod.yellow)})
        return results
    results.append({'consumed': True, 'messsage': Message('Tu allumes le feu sur un rayon de {0}'.format(radius), libtcod.orange)})
    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message('{0} subit {1} degats de feu'.format(entity.name, damage), libtcod.orange)})
            fire_sound = sm.choose_sound(fire_sounds)
            fire_sound.playpause()
            results.extend(entity.fighter.take_damage(damage))
    return results


'''
Parchemin de confusion
'''
def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    results = []
    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('Hors de portee', libtcod.yellow)})
        return results
    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)
            confused_ai.owner = entity
            entity.ai = confused_ai
            results.append({'consumed': True, 'message': Message('{0} devient debile'.format(entity.name), libtcod.light_green)})
            confuse_sound = sm.choose_sound(confuse_sounds)
            confuse_sound.playpause()
            break
    else:
        results.append({'consumed': False, 'message': Message('Pas de cible', libtcod.yellow)})
    return results
