from __future__ import print_function, division
from datetime import datetime as dt
from World import World


class SimulationParameters():
    """
    All valid parameters with defaults pre-set.

    grid_width          - (int)
    grid_height         - (int)
    n_agents            - (int)
    junction_capacity   - (int) maximum number of agents per junction
    street_capacity     - (int) maximum number of agents per street
    junction_throughput - (int) maximum number of moves from junction streets to other junctions (per timestep)
    street_throughput   - (int) maximum number of moves from a junction to connecting streets (per direction, per timestep)
    steps_per_day       - (int)

    Some numbers:
    system_capacity = grid_width * grid_height * (junction_capacity + 4 * street_capacity)
    max_travel_distance = grid_width + grid_height (unweighted)
    """
    def __init__(self):
        self.grid_width = 5
        self.grid_height = 5
        self.n_agents = 75
        # self.junction_capacity = 4
        # self.street_capacity = 6
        # junction_throughput = 1  # TODO: replace GridNode.MAX_ROAD_PUSHES with this
        # street_throughput = 4  # TODO: replace GridNode.MAX_MOVES with this
        self.steps_per_day = 24 * 60

    def __str__(self):
        return ', '.join(map(lambda (k,v): "%s: %s" % (k, v), self.__dict__.items()))

    def __repr__(self):
        return "<SimulationParameters: %s>" % self.__str__()


class Simulation():
    """
    Main class for the traffic simulation. The idea is to instantiate this with
    a parameters dictionary (see class SimulationParameters) and then call
    do_step() repeatedly. This can be done either from a command line main
    function, or from Django.
    """

    def __init__(self, parameters):
        self._world = World()
        self._parameters = parameters
        self._setup()

    def _setup(self):
        self._world.setup(self._parameters)

    def do_step(self):
        w, g = self._world, self._world.get_grid()
        cars = w.get_agents()
        start = dt.now()

        for car in cars:
            if not car.is_travelling():
                new_route_found = False
                while not new_route_found:
                    new_route_found = car.set_route(g.get_random_position(), g.get_random_position())

        w.update_grid()

        if w.get_time() == 0:
            duration = dt.now() - start
            print("===== Day: %i (%.2f secs) =====" %
                  (w.get_day(), duration.seconds + (duration.microseconds / 1000000)))
            #printing grid
            #self.print_grid(self._world.print_grid())
            start = dt.now()

        w.next_time_step()

    def print_grid(self, printing_grid):
        self._printing_grid = printing_grid
        #print (self._printing_grid)

    def Json_data(self, data_we_want_to_plot):
        from django.utils import simplejson as json

        json_data_we_want_to_plot = json.dumps(data_we_want_to_plot)
        render_template("_our_HTML_", {"_our_data", our_js_data})

        "Here we create JSON data. Into the js script file we need to add: type=""text/javascript"">"
        "data_from_django = {{ :_our_data }};"
        "widget.init(data_from_django);"
