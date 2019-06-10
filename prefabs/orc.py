import libtcodpy as libtcod

from render_functions import RenderOrder

from entity import Entity

from components.ai import BasicMonster
from components.fighter import Fighter

import random


def make_orc(room, AiComponentClass=BasicMonster):

    # TODO must change for non square rooms
    # Unpack room coordinates
    x1, y1, x2, y2 = room.xy
    x = random.randint(x1+1, x2-1)
    y = random.randint(y1+1, y2-1)

    fighter_component = Fighter(
        hp=20, defense=0, power=4, xp=35)

    # Create the AI for the monster
    ai_component = AiComponentClass(room)

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
