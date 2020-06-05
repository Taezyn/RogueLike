import tcod as libtcod
from random import randint
from game_messages import Message


"""
Module definissant les différents comportements des monstres.
"""


class BasicMonster:
    """
    Comportement d'un monstre stantard : si il voit le joueur il se deplace jusqu'a 2 cases de lui
    S'il est a une case il l'attaque, sinon il ne fait rien
    """

    def __init__(self):
        """
        Initialise une IA basique

        Parametres:
        ----------
        Aucun

        Renvoi:
        -------
        Aucun

        """
        self.ai_name = 'BasicMonster'

    def take_turn(self, target, fov_map, game_map, entities):
        """
        Joue le tour d'une IA basique

        Parametres:
        ----------
        target : Entity
            Cible de l'IA, c'est à dire le joueur
        fov_map : tcod.map
            Champ de vision de l'entité
        game_map : GameMap
            Carte actuellement utilisée
        entities : list
            Liste des entités de la carte

        Renvoi:
        -------
        results : list
            Liste des resultats. Utilisée dans engine
        """
        results = []
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)
            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)
        return results


class ConfusedMonster:
    """
    Comportement d'un monstre confus par un parchemin : mouvement
    aleatoire autour de sa position durant un nombre de tour donne
    """

    def __init__(self, previous_ai, number_of_turns=10):
        """
        Initialise une IA confuse

        Parametres:
        ----------
        previous_ai : BasicMonster ou Boss
            IA précédente à garder en mémoire
        number_of_turns: int
            Nombre de tours de l'effet

        Renvoi:
        -------
        Aucun

        """
        self.ai_name = 'ConfusedMonster'
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns


    def take_turn(self, target, fov_map, game_map, entities):
        """
        Joue le tour d'une IA basique

        Parametres:
        ----------
        target : Entity
            Cible de l'IA, c'est à dire le joueur. Non utilisé ici.
        fov_map : tcod.map
            Champ de vision de l'entité. Non utilisé ici.
        game_map : GameMap
            Carte actuellement utilisée
        entities : list
            Liste des entités de la carte

        Renvoi:
        -------
        results : list
            Liste des resultats. Utilisée dans engine
        """
        results = []
        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1
            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)
            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message("{0} n'est plus confus".format(self.owner.name), libtcod.red)})
        return results


class Boss:
    """
    IA du boss, présent un niveau sur cinq
    """

    def __init__(self):
        """
        Initialise une IA de Boss

        Parametres:
        ----------
        Aucun

        Renvoi:
        -------
        Aucun

        """
        self.ai_name = 'Boss'
        self.turn = 1
        self.aoeing = False
        self.radius = 3

    def take_turn(self, target, fov_map, game_map, entities):
        """
        Joue le tour d'une IA basique

        Parametres:
        ----------
        target : Entity
            Cible de l'IA, c'est à dire le joueur
        fov_map : tcod.map
            Champ de vision de l'entité
        game_map : GameMap
            Carte actuellement utilisée
        entities : list
            Liste des entités de la carte

        Renvoi:
        -------
        results : list
            Liste des resultats. Utilisée dans engine

        """
        results = []
        boss = self.owner
        if self.turn % 10 == 0 or self.aoeing:
            self.aoeing = True
            attack_results = boss.fighter.boss_aoe(self.turn, boss, target, self.radius)
            results.extend(attack_results)
            if attack_results:
                self.aoeing = False
        else:
            if libtcod.map_is_in_fov(fov_map, boss.x, boss.y):
                if boss.distance_to(target) >= 2:
                    boss.move_astar(target, entities, game_map)
                elif target.fighter.hp > 0:
                    attack_results = boss.fighter.attack(target)
                    results.extend(attack_results)
        self.turn += 1
        return results
