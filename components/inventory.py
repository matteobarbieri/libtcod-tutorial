import tcod as libtcod

from game_messages import Message


class InventoryFullException(Exception):
    pass


class Inventory:

    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def pickup(self, item):

        # Should just be equal, but just in case...
        if len(self.items) >= self.capacity:
            raise InventoryFullException()

        # Remove item coordinates (they do not make sense once they're in the
        # player's inventory
        item.x = None
        item.y = None

        # Actually add the item to the inventory
        self.items.append(item)

        # Return a feedback message
        return Message("You pick up a {}".format(item),
                libtcod.white)

    def drop(self, item):
        pass

    def get_item_position_in_list(self, item):
        """
        """

        return self.items.index(item)
    
    """
    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full', libtcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0}!'.format(item.name), libtcod.blue)
            })

            self.items.append(item)

        return results

    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            equippable_component = item_entity.equippable

            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append(
                    {
                        'message': Message(
                            'The {0} cannot be used'.format(
                                item_entity.name),
                            libtcod.yellow)
                    }
                )

        else:
            if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.function_kwargs, **kwargs}
                item_use_results = item_component.use_function(self.owner, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)

                results.extend(item_use_results)

        return results

    def remove_item(self, item):
        self.items.remove(item)

    def drop_item(self, item):
        results = []

        # When an item is dropped, it is also unequiped
        if \
                self.owner.equipment.main_hand == item \
                or self.owner.equipment.off_hand == item:
            self.owner.equipment.toggle_equip(item)

        # Set here the coordinates of the item, which will appear again in the
        # map
        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message('You dropped the {0}'.format(item.name),
                                                                 libtcod.yellow)})

        return results
    """
