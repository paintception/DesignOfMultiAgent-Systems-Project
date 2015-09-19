class Agent:
    def __init__(self, world):
        self._world = world
        self._position = (0, 0)
        self._start = (-1, -1)
        self._end = (-1, -1)
        self._velocity = 0
        self._nowaypoints = []  # initially empty, add points for A* to avoid
