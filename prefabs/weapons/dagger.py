from entity import Entity

from components.item import Item, ItemType, ItemSubtype  # noqa
from components.equippable import Equippable

from equipment_slots import EquipmentSlots

from render_functions import RenderOrder

import tcod as libtcodpy


def make_dagger():

    # Create the base Item instance
    item_component = Item(
        item_types=[ItemType.WEAPON],
        item_subtypes=[ItemSubtype.MELEE]
    )

    # The equippable component of the entity
    equippable_component = Equippable(
        valid_slots=[EquipmentSlots.MAIN_HAND, EquipmentSlots.OFF_HAND],
        damage_range=[3, 4],
    )

    dagger = Entity(
        None, None,
        '-', libtcodpy.sky, "Dagger", blocks=False,
        block_sight=False, render_order=RenderOrder.ITEM,
        components={
            'equippable': equippable_component,
            'item': item_component,
        })

    return dagger
