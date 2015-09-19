from Agent import Agent
from Grid import Grid


class World():
    def __init__(self, grid_size, num_agents):
        self._grid = Grid(grid_size, grid_size)
        self._time = 0
        self._agents = [Agent() for i in xrange(num_agents)]
        # self.model_params = {}
