from game_messages import Message

import tcod as libtcod


class UnableToEquipException(Exception):
    """
    Exception raised whenever it is impossible to equip a piece of equipment
    for whatever reason.
    """
    pass


class Equipment:
    """
    This class describes the equipment currently 'active' (i.e., worn/wielded,
    whatever) on the player.
    """

    def __init__(self, available_slots=[]):

        # Initialize the list of slots
        self.available_slots = available_slots

        # Initialize the `slots` property, which contains the list of all
        # equipped items
        self.slots = dict()

    def stat_bonus(self, stat_name):
        """
        Returns the total equipment stat bonus for a specific stat
        """

        # TODO can be optimized (cached) in order to not recompute each bonus
        # every time a stat is checked

        total_bonus = 0

        # Search for all possible equipment slots
        for _, item in self.slots.items():

            if item:
                total_bonus += item.equippable.stat_bonus(stat_name)

        return total_bonus

    @property
    def max_hp_bonus(self):
        # TODO to rework
        return 0

        # bonus = 0

        # if self.main_hand and self.main_hand.c['equippable']:
            # bonus += self.main_hand.c['equippable'].max_hp_bonus

        # if self.off_hand and self.off_hand.c['equippable']:
            # bonus += self.off_hand.c['equippable'].max_hp_bonus

        # return bonus

    @property
    def power_bonus(self):
        # TODO to rework
        return 0

        # bonus = 0

        # if self.main_hand and self.main_hand.c['equippable']:
            # bonus += self.main_hand.c['equippable'].power_bonus

        # if self.off_hand and self.off_hand.c['equippable']:
            # bonus += self.off_hand.c['equippable'].power_bonus

        # return bonus

    @property
    def defense_bonus(self):
        # TODO to rework
        return 0

        # bonus = 0

        # if self.main_hand and self.main_hand.c['equippable']:
            # bonus += self.main_hand.c['equippable'].defense_bonus

        # if self.off_hand and self.off_hand.c['equippable']:
            # bonus += self.off_hand.c['equippable'].defense_bonus

        # return bonus

    def unequip(self, equippable_entity):
        """
        Unequip a currently equipped item.
        """

        messages = list()

        # Search for the item among equipped items
        for slot, item in self.slots.items():
            if item == equippable_entity:
                item.equipped = False
                self.slots[slot] = None

                # Add item to the owner's inventory
                self.owner.inventory.items.append(item)

                messages.append(Message(
                    "{} unequipped".format(equippable_entity),
                    libtcod.white))
                return messages
            pass
        else:
            # TODO should not really happen actually...
            pass

    def equip(self, equippable_entity, slot=None):
        """
        Parameters
        ----------

        equippable_entity : Entity
            The entity that is being equipped.
        """

        messages = list()

        if slot is not None:
            # TODO implement this
            pass

        # Try to equip the entity in an available slot
        for slot in equippable_entity.c['equippable'].valid_slots:

            # First check if slot is present and free
            if (slot not in self.available_slots or
                self.slots.get(slot) is not None):  # noqa

                # Slot unavailable, move on
                continue
            else:

                # Slot available, equip the item!

                # Set the `equippable` property as true
                equippable_entity.equipped = True

                # Add the entity to slots
                self.slots[slot] = equippable_entity

                messages.append(Message(
                    "Equipped {} in {}".format(equippable_entity, slot),
                    libtcod.white))

                return messages
                # break

        else:
            # Unable to equip the entity
            raise UnableToEquipException(
                "No equipment slots available for {}!".format(
                    equippable_entity))


    @property
    def melee_weapons(self):
        """
        Return the list of melee weapons currently equipped
        """
        weapons = list()

        for _, equipped_entity in self.slots.items():
            if equipped_entity and equipped_entity.item.is_melee():
                weapons.append(equipped_entity)

        # TODO DEBUG remove
        # print("Melee weapons:")
        # print(weapons)

        return weapons
