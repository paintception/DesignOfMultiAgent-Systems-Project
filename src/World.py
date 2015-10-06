from Agent import Agent
from Grid import Grid
from Singleton import Singleton


@Singleton
class World():
    # avoid ctor parameters since this is a singleton
    def __init__(self):
        pass

    def setup(self, parameters):
        self._parameters = parameters
        print("** Simulation parameters: %s" % self._parameters)

        self._time_step = 0
        self._day = 0
        self._grid = Grid(parameters.grid_width, parameters.grid_height)
        self._agents = [Agent(i, self) for i in xrange(parameters.n_agents)]

    def get_day_time(self):
        return self._time_step

    def get_day(self):
        return self._day

    def get_timestamp(self):
        return self._day * self._parameters.steps_per_day + self._time_step

    def get_parameters(self):
        return self._parameters

    def get_grid(self):
        return self._grid

    def print_grid(self):
        return self._grid.print_grid()

    def update_grid(self):
        self._grid.update_grid()

    def get_agents(self):
        return self._agents

    def next_time_step(self):
        self._time_step = (self._time_step + 1) % self._parameters.steps_per_day
        if self._time_step == 0:
            self._day += 1
