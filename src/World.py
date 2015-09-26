from Agent import Agent
from Grid import Grid


class World():
    TIME_STEPS_PER_DAY = 24 * 60

    def __init__(self, grid_size, num_agents):
        self._grid = Grid(grid_size, grid_size)
        self._time = 0
        self._agents = [Agent(self, i) for i in xrange(num_agents)]
        # self.model_params = {}

    def get_time(self):
        return self._time

    def get_grid(self):
        return self._grid

    def get_agents(self):
        return self._agents

    def next_time_step(self):
        self._time = (self._time + 1) % self.TIME_STEPS_PER_DAY
