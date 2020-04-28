import tcod as libtcod
from game_messages import Message

'''
Definit l'objet fighter qui sera assigné au joueur et aux monstres
'''


class Fighter:
    def __init__(self, hp, defense, power, xp=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0
        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0
        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0
        return self.base_defense + bonus

    '''
    Subit un certain montant de degats et meurt si la vie passe en negatif
    '''
    def take_damage(self, amount):
        results = []
        self.hp -= amount
        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})
        return results

    '''
    Soigne d'un montant indiqué ou par defaut de 25% de la vie max
    '''
    def heal(self, *args):
        if len(args) != 0:
            self.hp += args[0]
        else:
            self.hp += self.max_hp//4
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    '''
    Attaque la cible du fighter.
    Pour un monstre, decide avec ai.BasicMonster,
    Pour le joueur, decide par le deplacement
    '''
    def attack(self, target):
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

    '''
    Pour le boss : attaque en aoe, 3 cases autour de lui
    '''
    def boss_aoe(self, turn, boss, target, radius):
        if turn % 10 == 3 and boss.distance_to(target) <= radius:
            target.fighter.take_damage(int(0.33 * target.fighter.max_hp))
            return [{'message': Message('Le boss attaque en AOE le joueur pour 33% de sa vie.')}]
        elif turn % 10 == 3 and boss.distance_to(target) > radius:
            return [{'message': Message('Le boss rate son AOE.')}]
        return []
