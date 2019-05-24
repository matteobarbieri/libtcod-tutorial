from equipment_slots import EquipmentSlots


class Equipment:
    """
    This class describes the equipment currently 'active' (i.e., worn/wielded,
    whatever) on the player.
    """

    def __init__(self, main_hand=None, off_hand=None, available_slots=None):

        # TODO must update/replace this stuff
        self.main_hand = main_hand
        self.off_hand = off_hand

        # Initialize the list of slots
        self.available_slots = available_slots

        # Initialize the list of equipped items
        self.equipped_items = dict()

    def stat_bonus(self, stat_name):
        """
        Returns the total equipment stat bonus for a specific stat
        """

        # TODO can be optimized (cached) in order to not recompute each bonus
        # every time a stat is checked

        total_bonus = 0

        # Search for all possible equipment slots
        for s in self.available_slots:

            # Get item equipped at slot s (or None)
            item = self.equipped_items.get(s)

            if item:
                total_bonus += item.equippable.stat_bonus(stat_name)

        return total_bonus

    @property
    def max_hp_bonus(self):
        # TODO to rework
        return 0
        bonus = 0

        if self.main_hand and self.main_hand.c['equippable']:
            bonus += self.main_hand.c['equippable'].max_hp_bonus

        if self.off_hand and self.off_hand.c['equippable']:
            bonus += self.off_hand.c['equippable'].max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        # TODO to rework
        return 0
        bonus = 0

        if self.main_hand and self.main_hand.c['equippable']:
            bonus += self.main_hand.c['equippable'].power_bonus

        if self.off_hand and self.off_hand.c['equippable']:
            bonus += self.off_hand.c['equippable'].power_bonus

        return bonus

    @property
    def defense_bonus(self):
        # TODO to rework
        return 0
        bonus = 0

        if self.main_hand and self.main_hand.c['equippable']:
            bonus += self.main_hand.c['equippable'].defense_bonus

        if self.off_hand and self.off_hand.c['equippable']:
            bonus += self.off_hand.c['equippable'].defense_bonus

        return bonus

    def toggle_equip(self, equippable_entity):

        # TODO to rework
        results = []

        slot = equippable_entity.c['equippable'].valid_slots[0]

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})

                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        return results

    @property
    def melee_weapons(self):
        """
        Return the list of melee weapons currently equipped
        """
        weapons = list()

        if self.main_hand and self.main_hand.item.is_melee():
            weapons.append(self.main_hand)

        if self.off_hand and self.off_hand.item.is_melee():
            weapons.append(self.off_hand)

        # TODO DEBUG remove
        print("Melee weapons:")
        print(weapons)

        return weapons
