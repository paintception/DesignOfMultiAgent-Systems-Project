from Utils import Point


class Agent:
    def __init__(self, world):
        self._world = world
        self._position = Point(0, 0)
        self._start = Point()
        self._end = Point()
        self._velocity = 0

    def is_travelling(self):
        return self._end.is_set()

    def set_start_point(self, p):
        self._start = p

    def set_end_point(self, p):
        self._end = p

    def reset_pos(self):
        self._position = self._start

    def update(self):
        pass

    def __str__(self):
        return "(Agent @ %s - %s -> %s)" % (self._position, self._start, self._end)
