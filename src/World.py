from Agent import Agent
from Grid import Grid
from Singelton import Singelton

@Singelton
class World():
    TIME_STEPS_PER_DAY = 24 * 60

    def __init__(self):
        pass

    def setup(self, grid_size, num_agents):
        self._grid = Grid(grid_size, grid_size)
        self._time = 0
        self._agents = [Agent(i, self) for i in xrange(num_agents)]


    def get_time(self):
        return self._time

    def get_model_parameters(self):
	return self.model_parameters

    def get_grid(self):
        return self._grid

    def print_grid(self):
        return self._grid.print_grid()

    def update_grid(self):
        self._grid.update_grid()

    def get_agents(self):
        return self._agents

    def next_time_step(self):
        self._time = (self._time + 1) % self.TIME_STEPS_PER_DAY
