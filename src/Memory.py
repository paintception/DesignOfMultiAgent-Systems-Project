import numpy


class Memory():
    def __init__(self, width, height):
        self._jams_x = numpy.zeros((height, width - 1))
        self._jams_y = numpy.zeros((height - 1, width))

    def add_jam(self, x1, y1, x2, y2, velocity):
        assert x1 == x2 or y1 == y2
        assert not (x1 == x2 and y1 == y2)

        if x1 < x2:
            self._jams_x[y1][x1] = velocity
        elif x2 < x1:
            self._jams_x[y1][x1] = velocity
        elif y1 < y2:
            self._jams_y[y1][x1] = velocity
        elif y2 < y1:
            self._jams_y[y2][x1] = velocity
        else:
            print "fuck you"

    def get_grid_point(self, x1, y1, x2, y2):
        assert x1 == x2 or y1 == y2
        assert not (x1 == x2 and y1 == y2)

        if x1 < x2:
            return self._jams_x[y1][x1]
        elif x2 < x1:
            return self._jams_x[y1][x1]
        elif y1 < y2:
            return self._jams_y[y1][x1]
        elif y2 < y1:
            return self._jams_y[y2][x1]
