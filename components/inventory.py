import tcod as libtcod

from game_messages import Message


class InventoryFullException(Exception):
    pass


class Inventory:

    def __init__(self, capacity):
        self.capacity = capacity

        # Keep track separately of items and their associated letters
        self.items = list()
        self.item_letters = list()

        # The list of all letters available for an item
        # TODO limit to the maximum number of items a player can have on him,
        # between equipped and in inventory
        self.available_letters = [
            chr(i) for i in range(ord('a'), ord('z') + 1)]

    def unequip(self, item):

        raise Exception("Not implemented!")
        messages = self.owner.equipment.equip(item)

        # Remove the item from the inventory
        self.items.remove(item)
        self.item_letters.remove(item.item_letter)

        # Return a feedback message
        return messages

    def equip(self, item):

        messages = self.owner.equipment.equip(item)

        # Remove the item from the inventory
        # self.items.remove(item)
        # self.item_letters.remove(item.item_letter)

        # Return a feedback message
        return messages

    def drop(self, item, level):

        # TODO
        # For the time being, just drop it on the floor exactly where the
        # player is.
        item.x = self.owner.x
        item.y = self.owner.y

        # Remove the item from the inventory
        self.items.remove(item)
        self.item_letters.remove(item.item_letter)

        # Re-add the used letter to the list of available ones
        self.available_letters.append(item.item_letter)
        self.available_letters.sort()
        item.item_letter = None

        # Add it back to the map's entities
        level.entities.append(item)

        # Return a feedback message
        return Message("You drop a {} on the floor.".format(item),
                libtcod.white)

    def pickup(self, item, level):

        # Should just be equal, but just in case...
        if len(self.items) >= self.capacity:
            raise InventoryFullException()

        # Remove item coordinates (they do not make sense once they're in the
        # player's inventory
        item.x = None
        item.y = None

        # Actually add the item to the inventory, Associating it with the
        # first available letter
        item_letter = self.available_letters.pop(0)
        item.item_letter = item_letter
        self.items.append(item)
        self.item_letters.append(item_letter)
        print("Item letter: {}".format(item_letter))

        # And remove it from the map
        level.entities.remove(item)

        # Return a feedback message
        return Message("You pick up a {}".format(item),
                libtcod.white)

    def get_item_position_in_list(self, item):
        """
        """

        return self.items.index(item)

    """

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
        """
