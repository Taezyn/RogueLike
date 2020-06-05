import tcod as libtcod
from game_messages import Message


class Fighter:
    """
    Definit un composant fighter qui sera assigné au joueur et aux monstres
    """
    def __init__(self, hp, defense, power, xp=0):
        """
        Initialise le composant fighter

        Parametres:
        ----------
        hp : int

        defense : int

        power : int

        xp : int


        Renvoi:
        -------
        Aucun

        """
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp

    @property
    def max_hp(self):
        """
        Permet l'ajout d'HP bonus au fighter si son equipement possède cette caractéristique

        Parametres:
        ----------
        Aucun

        Renvoi:
        -------
        Aucun

        """
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0
        return self.base_max_hp + bonus

    @property
    def power(self):
        """
        Permet l'ajout d'attaque bonus au fighter si son equipement possède cette caractéristique

        Parametres:
        ----------
        Aucun

        Renvoi:
        -------
        Aucun

        """
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0
        return self.base_power + bonus

    @property
    def defense(self):
        """
        Permet l'ajout de défense bonus au fighter si son equipement possède cette caractéristique

        Parametres:
        ----------
        Aucun

        Renvoi:
        -------
        Aucun

        """
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0
        return self.base_defense + bonus

    def take_damage(self, amount):
        """
        Fait subir au au fighter un certain montant de dégâts et le fait mourir si HP <= 0

        Parametres:
        ----------
        amount : int
            Dégâts entrants

        Renvoi:
        -------
        results : list
            Liste des résultats. Utilisée dans engine.

        """
        results = []
        self.hp -= amount
        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})
        return results

    def heal(self, *args):
        """
        Permet le soin d'un fighter

        Parametres:
        ----------
        *args : list
            Contient le montant d'HP à rendre, ou 25% HP par défaut

        Renvoi:
        -------
        Aucun

        """
        if len(args) != 0:
            self.hp += args[0]
        else:
            self.hp += self.max_hp//4
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        """
        Permet au fighter d'en attaquer un autre. Fait appel à l'IA pour les monstres

        Parametres:
        ----------
        target : Entity
            Cible de l'attaque

        Renvoi:
        -------
        results : list
            Liste des résultats. Utilisée dans engine.

        """
        results = []
        damage = self.power - target.fighter.defense
        if damage > 0:
            results.append({'message': Message('{0} attaque {1} pour {2} PV.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attaque {1} mais ne fait pas de degats.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})
        return results

    def boss_aoe(self, turn, boss, target, radius):
        """
        Permet au boss d'attaquer en zone.

        Parametres:
        ----------
        turn : int
            Tour en cours
        boss : Entity
            Boss
        target : Entity
            Cible de l'attaque
        radius : int
            Rayon de la zone de dégâts

        Renvoi:
        -------
        results : list
            Liste des résultats. Utilisée dans engine.

        """
        results = []
        if turn % 10 == 3 and boss.distance_to(target) <= radius:
            results.append({'message': Message('Le boss attaque en AOE le joueur pour 33% de sa vie.')})
            results.extend(target.fighter.take_damage(int(0.33 * target.fighter.max_hp)))
        elif turn % 10 == 3 and boss.distance_to(target) > radius:
            results.append({'message': Message('Le boss rate son AOE.')})
        return results
