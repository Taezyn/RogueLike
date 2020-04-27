import tcod as libtcod
import math
from render_functions import RenderOrder

'''
Tous les objets python intervenant dans le jeu sont definis comme des entites, sauf le sol
'''

class Entity:
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None,
                 item=None, inventory=None, stairs=None, level=None, visible=True):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        self.visible = visible

        # Les if suivants permettent de faire le lien entre un objet (ai, fighter, etc...)
        # et la classe entite a laquelle l'objet repond egalement

        if self.fighter:
            self.fighter.owner = self
        if self.ai:
            self.ai.owner = self
        if self.item:
            self.item.owner = self
        if self.inventory:
            self.inventory.owner = self
        if self.stairs:
            self.stairs.owner = self
        if self.level:
            self.level.owner = self

    '''
    Fait bouger une entite mobile
    '''
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    '''
    Fait avancer une entite mobile vers une cible si elle
    n'est pas bloquee par le decor ou une autre entite
    '''
    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    '''
    Renvoie la distance entre deux entites
    '''
    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    '''
    Renvoie la distance entre une entite et une coordonnee
    '''
    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    '''
    Utilise l'algorithme de recherche de chemin A* pour
    le deplacement d'un monstre vers le joueur
    Est appelé dans ai.BasicMonster
    '''
    def move_astar(self, target, entities, game_map):
        fov = libtcod.map_new(game_map.width, game_map.height)
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)
        my_path = libtcod.path_new_using_map(fov, 1.41)
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                self.x = x
                self.y = y
        else:
            self.move_towards(target.x, target.y, game_map, entities)
        libtcod.path_delete(my_path)


'''
Teste si toutes les entites dotees d'une ai (donc les monstres)
d'une liste d'entites donnee sont mortes
'''
def all_dead(entities):
    for dead_entity in entities:
        if dead_entity.ai:
            if dead_entity.fighter.hp > 0:
                return False
    return True


'''
Teste si la destination souhaitee d'un fighter est disponible ou non
'''
def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None
