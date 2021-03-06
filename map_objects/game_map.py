import tcod as libtcod
from random import randint
from components.ai import BasicMonster, Boss, ConfusedMonster
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs
from entity import Entity
from item_functions import heal, cast_lightning, cast_fireball, cast_confuse
from game_messages import Message
from map_objects.rectangle import Rect
from map_objects.tile import Tile
from render_functions import RenderOrder
from random_utilis import monsters_per_room, items_per_room


class GameMap:
    """
    Plateau de jeu sur lequel le joueur se meut, créée de façon procédurale
    """

    def __init__(self, width, height, dungeon_level=1):
        """
        Crée un plateau de jeu rempli de Tiles bloquantes et inexplorées

        Parametres:
        ----------
        width : int

        height : int

        dungeon_level : int


        Renvoi:
        -------
        Aucun

        """
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        """
        Rempli entièremement le plateau de Tiles bloquantes

        Parametres:
        ----------
        Aucun

        Renvoi:
        -------
        tiles : list
            Liste de listes décrivant le terrain dans son ensemble

        """
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, graphics):
        """
        Cree un nombre de salles inferieur a un nombre fixe (s'arrete lorsque la generation aleatoire cree
        deux pieces qui s'intersectent. Place le joueur dans la premiere d'entre elles, puis connecte la nouvelle
        salle avec la precedente et enfin ajoute les escaliers a la liste des entites du jeu

        Parametres:
        ----------
        max_rooms : int

        room_min_size : int

        room_max_size : int

        map_width : int

        map_height : int

        player : Entity

        entities : list

        graphics : dict


        Renvoi:
        -------
        entities : list
            retourne la liste des entités avec les monstres et les objets placés

        """
        rooms = []
        num_rooms = 0
        center_of_last_room_x = None
        center_of_last_room_y = None
        for r in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)
            new_room = Rect(x, y, w, h)
            # Coupe la boucle si la pièce créée intersecte d'autres déjà créées
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            # Si la pièce créée est valide, la relie à la précédente et place les entités
            else:
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()
                center_of_last_room_x = new_x
                center_of_last_room_y = new_y
                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                entities = self.place_entities(new_room, entities, graphics)
                rooms.append(new_room)
                num_rooms += 1
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, graphics.get('stairs'), libtcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)
        return entities

    def create_room(self, room):
        """
        Crée une salle en rendant les Tile intérieures passantes.

        Parametres:
        ----------
        room : Rect
            La pièce avec ses dimensions

        Renvoi:
        -------
        Aucun

        """
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        """
        Créer un couloir horizontal

        Parametres:
        ----------
        x1 : int

        x2 : int

        y : int


        Renvoi:
        -------
        Aucun

        """
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        """
        Créer un couloir vertical

        Parametres:
        ----------
        y1 : int

        y2 : int

        x : int


        Renvoi:
        -------
        Aucun

        """
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, graphics):
        """
        Place les monstres et les objets dans la room en cours de construction, en veillant
        à ne pas superposer des entités, puis ajoute le tout à la liste des entités.
        Le nombre de monstres et d'ojbets dépend de l'étage du donjon

        Parametres:
        ----------
        room : Rect

        entities : list

        graphics : dict


        Renvoi:
        -------
        entities : list

        """

        # monster_chances et item_chances définissent les entités à faire apparaître
        # avec leurs chances d'apparition et leurs poids respectifs
        monster_chances = [
            ('orc', 80, 1),
            ('troll', 20, 3)
        ]
        monsters_to_pop = monsters_per_room(self.dungeon_level, monster_chances, room)
        item_chances = [
            ('healing_potion', 45, 1),
            ('confusion_scroll', 20, 2),
            ('lightning_scroll', 18, 4),
            ('fireball_scroll', 7, 5),
            ('sword', 5, 1),
            ('shield', 5, 1)
        ]
        items_to_pop = items_per_room(self.dungeon_level, item_chances)

        for monster_choice in monsters_to_pop:
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if monster_choice == 'orc':
                    fighter_component = Fighter(hp=20, defense=0, power=4, xp=35)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, graphics.get(monster_choice), libtcod.desaturated_green, 'Orc', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                elif monster_choice == 'troll':
                    fighter_component = Fighter(hp=30, defense=1, power=8, xp=100)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, graphics.get(monster_choice), libtcod.darker_green, 'Troll', blocks=True, fighter=fighter_component,
                                     render_order=RenderOrder.ACTOR, ai=ai_component)
                entities.append(monster)

        for item_choice in items_to_pop:
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal)
                    item = Entity(x, y, graphics.get(item_choice), libtcod.white, 'Potion de soin', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'sword':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
                    item = Entity(x, y, graphics.get(item_choice), libtcod.sky, 'Epee', equippable=equippable_component)
                elif item_choice == 'shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
                    item = Entity(x, y, graphics.get(item_choice), libtcod.darker_orange, 'Bouclier', equippable=equippable_component)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True,
                                          targeting_message=Message('Clic gauche sur une case pour '
                                          'y envoyer une fireball', libtcod.light_cyan),
                                          damage=25, radius=3)
                    item = Entity(x, y, graphics.get('fireball_scroll'), libtcod.dark_orange, 'Parchemin de boule de feu', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True,
                                          targeting_message=Message('Clic gauche pour rendre un enemi '
                                          'confus', libtcod.light_cyan))
                    item = Entity(x, y, graphics.get('confusion_scroll'), libtcod.lighter_pink, 'Parchemin de confusion',
                                  render_order=RenderOrder.ITEM, item=item_component)
                elif item_choice == 'lightning_scroll':
                    item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
                    item = Entity(x, y, graphics.get('lightning_scroll'), libtcod.yellow, 'Parchemin de foudre', render_order=RenderOrder.ITEM,
                                  item=item_component)
                entities.append(item)
        return entities

    def is_blocked(self, x, y):
        """
        Lit si la coordonnée x,y est bloquée ou non

        Parametres:
        ----------
        x : int

        y : int


        Renvoi:
        -------
        bool

        """
        if self.tiles[x][y].blocked:
            return True
        return False

    def next_floor(self, player, message_log, constants, graphics):
        """
        Fait passer à l'étage suivant et crée une map (boss ou standart) en fonction de l'étage

        Parametres:
        ----------
        player : Entity

        message_log : MessageLog

        constants : dict

        graphics : dict


        Renvoi:
        -------
        entities : list

        play_boss_music : bool

        play_stage_music : bool

        """
        self.dungeon_level += 1
        entities = [player]
        message_log.add_message(Message('Vous recuperez la moitie de votre vie.', libtcod.light_violet))
        if self.dungeon_level % 5 == 0:
            self.tiles = self.initialize_tiles()
            entities = self.make_boss_map(entities, player)
            message_log.add_message(Message("C'est l'heure du du-du-du---DUEL !", libtcod.light_red))
            play_boss_music = True
            play_stage_music = False
        else:
            self.tiles = self.initialize_tiles()
            entities = self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                          constants['map_width'], constants['map_height'], player, entities, graphics)
            play_boss_music = False
            if self.dungeon_level % 5 == 1:
                play_stage_music = True
            else:
                play_stage_music = False
        player.fighter.heal(player.fighter.max_hp // 2)
        return entities, play_boss_music, play_stage_music

    def make_boss_map(self, entities, player):
        """
        Crée une pièce spécifique pour le combat de boss

        Parametres:
        ----------
        entities : list

        player : Entity


        Renvoi:
        -------
        entities : list

        """
        w = 50
        h = 30
        x = 15
        y = 10
        boss_rect = Rect(x, y, w, h)
        self.create_room(boss_rect)
        player.x = 40
        player.y = 35
        fighter_component = Fighter(hp=20*player.fighter.power, defense=0, power=player.fighter.max_hp//10,
                                    xp=player.level.experience_to_next_level)
        ai_component = Boss()
        boss = Entity(40, 25, 270, libtcod.darker_green, 'Boss', blocks=True,
                      fighter=fighter_component, render_order=RenderOrder.ACTOR, ai=ai_component)
        entities.append(boss)
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(40, 25, 264, libtcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component, visible=False)
        entities.append(down_stairs)
        return entities
