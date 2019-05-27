from enum import Enum, auto


class GameStates(Enum):
    PLAYERS_TURN = auto()
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()
    INVENTORY_MENU = auto()
    INVENTORY_ITEM_MENU = auto()
    TARGETING = auto()
    LEVEL_UP = auto()
    CHARACTER_SCREEN = auto()
    ENTITY_INFO = auto()
