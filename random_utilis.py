from random import randint
import numpy as np

"""
Ce module gere le taux d'apparation de monstres et d'items
en fonction de l'etage du donjon en assignant un poids au nombre
d'apparition en fonction de l'etage
"""


def monsters_per_room(dungeon_level, monsters_list, room):
    """
    Choisit combien de monstres de chaque type faire appraître, en fonction de l'étage actuel

    Parametres:
    ----------
    dungeon_level : int

    monsters_list : list

    room : Rect

    Renvoi:
    -------
    monsters_to_pop : list

    """
    total_weight = randint(1, int(3 * np.log(dungeon_level) + 1))
    monsters_pop_list = []
    current_weight = 0
    while current_weight < total_weight:
        chance = randint(1, 100)
        current_pick = 0
        monster_pick = False
        sum_chances = monsters_list[current_pick][1]
        while not monster_pick:
            if sum_chances < chance and current_weight + monsters_list[current_pick][2] < total_weight:
                current_pick += 1
                if current_pick >= len(monsters_list):
                    monsters_pop_list.append(monsters_list[current_pick][0])
                    current_weight += monsters_list[current_pick][2]
                    monster_pick = True
                sum_chances += monsters_list[current_pick][1]
            else:
                monsters_pop_list.append(monsters_list[current_pick][0])
                current_weight += monsters_list[current_pick][2]
                monster_pick = True
    monsters_pop_dict = {monster: monsters_pop_list.count(monster) for monster in monsters_pop_list}
    monsters_pop_list = []
    room_surface = (room.x2 - room.x1)*(room.y2 - room.y1)
    for monster in monsters_pop_dict:
        if monsters_pop_dict.get(monster) > room_surface // 4:
            monsters_pop_dict[monster] = room_surface // 4
        for i in range(monsters_pop_dict[monster]):
            monsters_pop_list.append(monster)
    return monsters_pop_list


def items_per_room(dungeon_level, item_list):
    """
    Choisit combien d'items de chaque type faire appraître, en fonction de l'étage actuel

    Parametres:
    ----------
    dungeon_level : int

    item_list : list


    Renvoi:
    -------
    items_to_pop : list

    """
    total_weight = randint(0, int(3 * np.log(dungeon_level) + 1))
    items_pop_list = []
    current_weight = 0
    while current_weight < total_weight:
        chance = randint(1, 100)
        current_pick = 0
        monster_pick = False
        sum_chances = item_list[current_pick][1]
        while not monster_pick:
            if sum_chances < chance and current_weight + item_list[current_pick][2] < total_weight:
                current_pick += 1
                if current_pick >= len(item_list):
                    items_pop_list.append(item_list[current_pick][0])
                    current_weight += item_list[current_pick][2]
                    monster_pick = True
                sum_chances += item_list[current_pick][1]
            else:
                items_pop_list.append(item_list[current_pick][0])
                current_weight += item_list[current_pick][2]
                monster_pick = True
    items_pop_dict = {item: items_pop_list.count(item) for item in items_pop_list}
    items_pop_list = []
    for item in items_pop_dict:
        if items_pop_dict.get(item) > 2:
            items_pop_dict[item] = 2
        for i in range(items_pop_dict[item]):
            items_pop_list.append(item)
    return items_pop_list
