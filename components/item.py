class Item:
    """
    Class describing an item
    """

    def __init__(
            self, use_function=None, targeting=False,
            targeting_message=None, **kwargs):

        # The function called when the item is used
        self.use_function = use_function

        # Other things that might be used by the use_function
        self.function_kwargs = kwargs

        # TODO these things must be probably reworked
        self.targeting = targeting
        self.targeting_message = targeting_message

    def stat_bonus(self, stat_name):
        """
        The total bonus provided by an item to a specific stat (if equipped).
        """

        # TODO stub, must be implemented
        return 0
