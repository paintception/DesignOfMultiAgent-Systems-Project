from __future__ import print_function, division
from datetime import datetime as dt
from World import World
from TimeLord import TimeLord


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

        # TODO: actually use these in the code
        self.junction_capacity = 4
        self.street_capacity = 6
        junction_throughput = 1  # TODO: replace GridNode.MAX_ROAD_PUSHES with this
        street_throughput = 4  # TODO: replace GridNode.MAX_MOVES with this

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

        n_route_endpoints = 10
        # TODO: set agent routes (first create n start points with no more than junction_capacity repetitions)
        p = self._parameters
        # agents live in random locations, but never more than junction_capacity in one place
        sp_list = self._get_random_points(p.grid_width, p.grid_height, p.n_agents, -1, p.junction_capacity)
        # agents travel to their workplace, of which only n_route_endpoints exist...lower for higher jam probability?
        ep_list = self._get_random_points(p.grid_width, p.grid_height, p.n_agents, n_route_endpoints, -1)

        cars = self._world.get_agents()
        assert len(cars) == p.n_agents, "number of agents not equal to simulation parameter value"
        for i in xrange(p.n_agents):
            # cars[i].set_route(sp_list[i], ep_list[i])
            spn = self._world.get_grid().get_item_at(sp_list[i])
            epn = self._world.get_grid().get_item_at(ep_list[i])
            cars[i].set_route(spn, epn)

    def _get_random_points(self, w, h, n, c=-1, r=-1):
        """
        Return n points between (0,0)-(w-1,h-1), sampled from at most c
        different locations with at most r repetitons of each location.
        For c and r, specify -1 to disable the corresponding limit.

        TODO: At least, that's the idea...currently returned number are selected randomly within given grid range.
        """
        from random import randint
        from utils import Point

        assert c < 0 or r < 0 or n <= c * r, "requested number of points larger than maximum possible"

        result = []
        for i in xrange(n):
            result.append(Point(randint(0, w - 1), randint(0, h - 1)))

        return result

    def do_step(self):
        w, g = self._world, self._world.get_grid()
        cars = w.get_agents()
        t= TimeLord()
        w.update_grid()

        start = dt.now()
        if t.get_day_time() == 0:
            duration = dt.now() - start
            print("===== Day: %i (%.2f secs) =====" %
                  (t.get_day(), duration.seconds + (duration.microseconds / 1000000)))
            #self.print_grid(self._world.print_grid())

            ct, cnt = 0, 0
            for car in cars:
                if not car.is_travelling():
                    car.restart_route()  # or car.reverse_route() to have them travel home
                    ct += 1
                else:
                    cnt += 1
            print("** Restarted %i cars, %i still travelling" % (ct, cnt))

            start = dt.now()

        t.next_time_step()

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
