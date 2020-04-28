import tcod as libtcod
from game_messages import Message

'''
Definit la classe inventaire comme une liste d'une longueur inferieure a un montant donne
'''

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    '''
    Ajoute un item à la fin de l'inventaire s'il reste de la place
    '''
    def add_item(self, item):
        results = []
        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('Inventaire plein', libtcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('{0} ramasse'.format(item.name), libtcod.blue)
            })
            self.items.append(item)
        return results

    '''
    Utilise un item de l'inventaire
    '''
    def use(self, item_entity, **kwargs):
        results = []
        item_component = item_entity.item
        if item_component.use_function is None:
            equippable_component = item_entity.equippable
            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append({'message': Message('{0} ne peut pas etre utilise'.format(item_entity.name), libtcod.yellow)})
        else:
            if item_component.targeting and not(kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.function_kwargs, **kwargs}
                item_use_results = item_component.use_function(self.owner, **kwargs)
                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)
                results.extend(item_use_results)
        return results

    '''
    Supprime un item utilise
    '''
    def remove_item(self, item):
        self.items.remove(item)

    '''
    Pose un item au sol sans l'utiliser
    '''
    def drop_item(self, item):
        results = []
        if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item:
            self.owner.equipment.toggle_equip(item)
        item.x = self.owner.x
        item.y = self.owner.y
        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message('Vous avez lache {0}'.format(item.name),
                                                                 libtcod.yellow)})
        return results
