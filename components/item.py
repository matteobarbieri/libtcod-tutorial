"""
The item class represents items and their properties "while they are in the
backpack". Meaning that for instance the info about their properties as items
that can be equipped must be stored in an instance of the  `Equippable` class.
"""

from enum import Enum, auto


class ItemType(Enum):
    """
    The main type of the item.
    """
    WEAPON = auto()
    ARMOR = auto()
    DEVICE = auto()
    CONSUMABLE = auto()


class ItemSubtype(Enum):
    """
    Additional item properties.
    """
    RANGED = auto()
    MELEE = auto()


class Item:
    """
    Class describing an item
    """

    def __init__(
            self, item_types=[], item_subtypes=[],
            ):

        # Set item type[s] and subtype[s]
        self.item_types = item_types
        self.item_subtypes = item_subtypes

    def get_inventory_options(self):
        """
        Return a list of possible actions for the item once it is selected
        from the inventory.
        """
        options = list()

        if self.is_armor() or self.is_weapon() or self.is_device():
            options.append(('e', 'Equip'))

        if self.is_consumable():
            options.append(('u', 'Use'))

        # Any item can be dropped
        options.append(('d', 'Drop'))

        return options

    # def __init__(
            # self, item_types=[], item_subtypes=[],
            # use_function=None, targeting=False, targeting_message=None,
            # **kwargs):

        # # The function called when the item is used
        # self.use_function = use_function

        # # Other things that might be used by the use_function
        # self.function_kwargs = kwargs

        # # Set item type[s] and subtype[s]
        # self.item_types = item_types
        # self.item_subtypes = item_subtypes

        # # TODO these things must be probably reworked
        # self.targeting = targeting
        # self.targeting_message = targeting_message

    def is_armor(self):
        return ItemType.ARMOR in self.item_types

    def is_weapon(self):
        return ItemType.WEAPON in self.item_types

    def is_device(self):
        return ItemType.DEVICE in self.item_types

    def is_consumable(self):
        return ItemType.CONSUMABLE in self.item_types

    def is_melee(self):
        return ItemSubtype.MELEE in self.item_subtypes

    def is_ranged(self):
        return ItemSubtype.RANGED in self.item_subtypes
