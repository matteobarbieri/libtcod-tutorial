from enum import Enum, auto


class ItemType(Enum):
    WEAPON = auto()
    CONSUMABLE = auto()


class ItemSubtype(Enum):
    RANGED = auto()
    MELEE = auto()


class Item:
    """
    Class describing an item
    """

    def __init__(
            self, item_types=[], item_subtypes=[],
            use_function=None, targeting=False, targeting_message=None,
            **kwargs):

        # The function called when the item is used
        self.use_function = use_function

        # Other things that might be used by the use_function
        self.function_kwargs = kwargs

        # Set item type[s] and subtype[s]
        self.item_types = item_types
        self.item_subtypes = item_subtypes

        # TODO these things must be probably reworked
        self.targeting = targeting
        self.targeting_message = targeting_message
