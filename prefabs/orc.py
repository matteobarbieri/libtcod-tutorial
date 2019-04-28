import libtcodpy as libtcod

from render_functions import RenderOrder

from entity import Entity

from components.ai import BasicMonster
from components.fighter import Fighter


def make_orc(x, y):

    fighter_component = Fighter(
        hp=20, defense=0, power=4, xp=35)
    ai_component = BasicMonster()

    mob = Entity(
        x, y,
        'o', libtcod.desaturated_green,
        'Orc',
        blocks=True,
        render_order=RenderOrder.ACTOR,
        components=dict(
            fighter=fighter_component,
            ai=ai_component)
    )

    return mob

