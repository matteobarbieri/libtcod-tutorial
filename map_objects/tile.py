import random

import libtcodpy as libtcod

GRAY_PALETTE = [
    # libtcod.Color(242, 242, 242),
    libtcod.Color(204, 204, 204),
    libtcod.Color(165, 165, 165),
    libtcod.Color(127, 127, 127),
    libtcod.Color(89, 89, 89),
]


class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block
    sight.
    """

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        self.explored = False

    def render_at(self, con, x, y, visible):
        """
        Render a tile at position x, y
        """
        # Set color for background

        if type(self) == Tile:
            return

        libtcod.console_set_char_background(
            con, x, y, self.bg_color, libtcod.BKGND_SET)

        if self.fg_symbol is not None:
            # Set color for foreground symbol
            libtcod.console_set_default_foreground(
                con, libtcod.black)

            # Draw symbol on foreground
            libtcod.console_put_char(
                con, x, y, self.fg_symbol, libtcod.BKGND_NONE)


class Floor(Tile):
    """
    A block representing traversable terrain
    """

    def __init__(self, bg_color=libtcod.black, fg_symbol=None,
                 fg_color=None):

        # Declare it as non-blocking
        super().__init__(False)

        self.bg_color = bg_color
        self.fg_color = fg_color
        self.fg_symbol = fg_symbol


class Wall(Tile):
    """
    A block of wall
    """

    def __init__(self, bg_color, fg_symbol='#', fg_color=libtcod.black):

        # Declare it as blocked
        super().__init__(True)

        self.bg_color = bg_color
        self.fg_color = fg_color
        self.fg_symbol = fg_symbol

    def create_from_palette(palette=GRAY_PALETTE):
        """
        palette: list
            Each element is a libtcod.Color object
        """

        return Wall(random.choice(palette))

    def create(base_color=libtcod.Color(159, 89, 66), color_variance=20):

        # Extract colors
        b, g, r = base_color.b, base_color.g, base_color.r

        # Slightly alter them
        b += random.randint(-color_variance, color_variance)
        b = max(0, b)
        b = min(255, b)

        g += random.randint(-color_variance, color_variance)
        g = max(0, g)
        g = min(255, g)

        r += random.randint(-color_variance, color_variance)
        r = max(0, r)
        r = min(255, r)

        return Wall(libtcod.Color(b, g, r))
