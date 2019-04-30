import libtcodpy as libtcod

from game_messages import Message

from render_functions import RenderOrder

class Fighter:
    def __init__(self, hp, defense, power, xp=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus


    def die(self):

        # Create message for the log
        death_message = Message(
            '{0} is dead!'.format(
                self.owner.name.capitalize()),
            libtcod.orange)

        self.owner.char = '%'
        self.owner.color = libtcod.dark_red
        self.owner.blocks = False
        self.owner.fighter = None
        self.owner.ai = None
        self.owner.name = 'remains of ' + self.owner.name
        self.owner.render_order = RenderOrder.CORPSE

        return death_message

    def take_damage(self, amount):
        messages = []

        self.hp -= amount

        if self.hp <= 0:
            # messages.append(
                # {'dead': self.owner, 'xp': self.xp})
            messages.append(self.die())

        return messages

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):

        # TODO Completely rewrite this
        messages = []

        damage = self.power - target.fighter.defense

        if damage > 0:

            messages.append(
                Message('{0} attacks {1} for {2} hit points.'.format(
                    self.owner.name.capitalize(), target.name,
                    str(damage)), libtcod.white))

            # In case there are other effects, add extra messages
            messages.extend(target.fighter.take_damage(damage))
        else:

            # Append the no damage dealt messages
            messages.append(
                Message('{0} attacks {1} but does no damage.'.format(
                    self.owner.name.capitalize(), target.name), libtcod.white))

        return messages
