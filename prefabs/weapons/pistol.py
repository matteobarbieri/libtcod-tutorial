from components.item import Item

from entity import Entity

from render_functions import RenderOrder

from components.equippable import Equippable

import tcod as libtcodpy


def make_pistol():

    item_component = Item()

    # TODO
    equippable_component = Equippable()

    pistol = Entity(
        None, None,
        ')', libtcodpy.green, "Pistol", blocks=False,
        block_sight=False, render_order=RenderOrder.ITEM,
        components={
            'equippable': equippable_component,
            'item': item_component,
        })

    return pistol
