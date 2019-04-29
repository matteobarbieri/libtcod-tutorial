class DijkstraMap:

    def __init__(self, d_map):
        self.d_map = d_map

    def downhill_from(self, xx, yy):
        """
        Returns two sets of coordinates: the first one containing the list of
        positions which lead towards a minimum, the other one a set of
        coordinates that keeps the actor at a constant value.
        This is done in order to avoid stalemates.
        """

        current_value = self.d_map[xx][yy]

        to_min = list()
        stay_put = list()

        # TODO check for boundaries (<0, >MAX)
        for x in range(xx-1, xx+2):
            for y in range(yy-1, yy+2):
                if self.d_map[x][y] < current_value:
                    to_min.append((x, y))
                elif self.d_map[x][y] == current_value:
                    stay_put.append((x, y))

        return to_min, stay_put

    def dump_txt(self, path):

        h = len(self.d_map[0])
        w = len(self.d_map)

        with open(path, 'w') as tf:
            for y in range(h):
                for x in range(w):
                    if self.d_map[x][y] > 20:
                        tf.write("#")
                    elif self.d_map[x][y] > 9:
                        tf.write(chr(65 - 10 + self.d_map[x][y]))
                    else:
                        tf.write("{}".format(self.d_map[x][y]))
                tf.write("\n")
