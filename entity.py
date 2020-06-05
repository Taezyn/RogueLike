import tcod as libtcod
import math
from render_functions import RenderOrder
from components.item import Item


class Entity:
    """
    Tous les objets python intervenant dans le jeu sont définis comme des entités, sauf le sol
    """
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None,
                 item=None, inventory=None, stairs=None, level=None, visible=True, equipment=None, equippable=None):
        """
        Crée une entité avec différents attributs, selon son type

        Parametres:
        ----------
        x : int
            Abscisse de l'entité
        y : int
            Ordonnée de l'entité
        char : int
            Aspect graphique (correspondant à une zone de l'image textures.png)
        color : tcod.color
            Couleur de l'entité
        blocks : bool
            L'entité est-elle bloquante ?
        render_order : int
            Priorité de rendu graphique
        fighter : Fighter ou None
            Composant Fighter de l'entité
        ai : BasicMonster ou Boss ou Non
            IA de l'entité
        item : Item ou None
            Si l'entité est un item
        inventory : Inventory ou Non
            Si l'entité est un inventaire
        stairs : Stairs ou None
            Si l'entité est un escalier
        level : Level ou None
            Si l'entité possède une barre d'XP
        visible : bool
            Si l'entité est visible
        equipment : Equipment ou None
            Si l'entité peut s'équiper d'item
        equippable : Equippable ou None
            Si l'entité peut être équipée

        Renvoi:
        -------
        Aucun
        """
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
        self.equipment = equipment
        self.equippable = equippable

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
        if self.equipment:
            self.equipment.owner = self
        if self.equippable:
            self.equippable.owner = self
            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

    def move(self, dx, dy):
        """
        Déplace une entité

        Parametres:
        ----------
        dx : int

        dy : int

        Renvoi:
        -------
        Aucun

        """
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        """
        Fait avancer une entité vers une cible, si le chemin n'est pas bloqué

        Parametres:
        ----------
        target_x : int

        target_y : int

        game_map : GameMap

        entities : list


        Renvoi:
        -------
        Aucun

        """
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)


    def distance_to(self, other):
        """
        Renvoie la distance entre deux entités

        Parametres:
        ----------
        other : Entity

        Renvoi:
        -------
        float

        """
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)


    def distance(self, x, y):
        """
        Renvoie la distance entre une entité et une coordonnée

        Parametres:
        ----------
        x : int

        y : int


        Renvoi:
        -------
        float

        """
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move_astar(self, target, entities, game_map):
        """
        Utilise l'algorithme de recherche de chemin A* pour le déplacement d'un monstre
        en direction du joueur. Est appelé dans ai.BasicMonster

        Parametres:
        ----------
        target : Entity

        entities : list

        game_map : GameMap


        Renvoi:
        -------
        Aucun

        """
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


def all_dead(entities):
    """
    Teste si toutes les entités dotés d'IA sont mortes

    Parametres:
    ----------
    entities : list

    Renvoi:
    -------
    bool

    """
    for dead_entity in entities:
        if dead_entity.ai:
            if dead_entity.fighter.hp > 0:
                return False
    return True


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    """
    Teste si la destination souhaitée est disponible ou non

    Parametres:
    ----------
    entities : list

    destination_x : int

    destination_y : int


    Renvoi:
    -------
    Entity ou None :
        Renvoie l'entité qui bloque le chemin s'il y en a une.

    """
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None
