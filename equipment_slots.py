from enum import Enum, auto


class EquipmentSlots(Enum):
    MAIN_HAND = auto()
    OFF_HAND = auto()
    HEAD = auto()
    CHEST = auto()
    HANDS = auto()
    LEGS = auto()
    FEET = auto()

SLOT_NAMES = {
    EquipmentSlots.MAIN_HAND: "Main hand",
    EquipmentSlots.OFF_HAND: "Off hand",
    EquipmentSlots.HEAD: "Head",
    EquipmentSlots.CHEST: "Chest",
    EquipmentSlots.HANDS: "Hands",
    EquipmentSlots.LEGS: "Legs",
    EquipmentSlots.FEET: "Feet",
}
