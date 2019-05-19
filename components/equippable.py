class Equippable:
    """
    Class describing an item that can be equipped.
    """

    def __init__(self, valid_slots=[], stats_bonuses={}, skills_bonuses={}):
        """
        Parameters
        ----------

        valid_slots : list
            A list of all possible slots where the item can be equipped.

        stats_bonuses: dict
            A dictionary containing all bonuses that this piece of equipment
            grants its owner.
        """

        self.valid_slots = valid_slots
        self.stats_bonuses = stats_bonuses
        self.skills_bonuses = skills_bonuses

    def stat_bonus(self, stat_name):
        """
        The total bonus provided by an item to a specific stat (if equipped).
        """

        if stat_name in self.stats_bonuses.keys():
            return self.stat_bonuses[stat_name]
        else:
            return 0
