class Item:
    """
    Class describing an item
    """

    def __init__(
            self, use_function=None, targeting=False,
            targeting_message=None, **kwargs):

        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs

    def stat_bonus(self, stat_name):
        """
        The total bonus provided by an item to a specific stat (if equipped).
        """

        # TODO stub, must be implemented
        return 0
