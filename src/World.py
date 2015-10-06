from Agent import Agent
from Grid import Grid
from Singleton import Singleton
from TimeLord import TimeLord


@Singleton
class World():
    # avoid ctor parameters since this is a singleton
    def __init__(self):
        pass

    def setup(self, parameters):
        self._parameters = parameters
        print("** Simulation parameters: %s" % self._parameters)

        self._grid = Grid(parameters.grid_width, parameters.grid_height)
        self._agents = [Agent(i, self) for i in xrange(parameters.n_agents)]

        self._timelord = TimeLord()
        self._timelord.setup(self._parameters.steps_per_day)

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

