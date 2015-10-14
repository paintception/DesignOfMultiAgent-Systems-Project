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
    max_days            - (int) number of days after which to stop the simulation

    Some numbers:
    system_capacity = grid_width * grid_height * (junction_capacity + 4 * street_capacity)
    max_travel_distance = grid_width + grid_height (unweighted)
    """
    def __init__(self):
        self.grid_width = 7
        self.grid_height = 7
        self.n_agents = 50

        self.junction_capacity = 3
        self.street_capacity = 5
        self.junction_throughput = 1
        self.street_throughput = 4

        self.steps_per_day = 30
        self.max_days = 10

        self.routes = None  # used to predefine agent routes

    @staticmethod
    def load(filename):
        import json
        from utils import Point

        with open(filename, 'r') as f:
            p = SimulationParameters()
            o = json.loads(f.read())['sim_parameters']
            print("o:", o)
            for (k,v) in o.items():
                p.__dict__[k] = v
            if p.routes:
                p.routes = [(Point(r[0][0], r[0][1]), Point(r[1][0], r[1][1])) for r in p.routes]
            return p

    def save(self, filename):
        import json
        with open(filename, 'w') as f:
            output = json.dumps({'sim_parameters': self.jsonifiable()})
            f.write(output + '\n')

    def jsonifiable(self):
        result = {k: v for (k, v) in self.__dict__.items()}
        if result['routes']:
            result['routes'] = [((s.x, s.y), (e.x, e.y)) for (s, e) in result['routes']]
        return result

    def __str__(self):
        return ', '.join(map(lambda (k,v): "%s: %s" % (k, v), self.__dict__.items()))

    def __repr__(self):
        return "<SimulationParameters: %s>" % self.__str__()


class Simulation():
    """
    Main class for the traffic simulation. The idea is to instantiate this with
    a parameters dictionary (see class SimulationParameters) and then call
    do_step() repeatedly. This can be done either from a command line main
    function, or from webserver.py.
    If parameters contains a 'routes' key, its value is taken to be a list with
    for each agent a start and end point, so: ((Sx, Sy), (Ex, Ey)); this can be
    used in conjunction with the load/save functions.
    """

    def __init__(self, parameters):
        self._world = World()
        self._parameters = parameters
        self._setup()
        self._jam_progression=[]

    def _setup(self):
        import random
        from utils import Point

        p = self._parameters
        self._world.setup(p)

        assert p.n_agents <= p.grid_width * p.grid_height * p.junction_capacity, \
            "not enough room for agent start points with given grid size and junction capacity"

        def random_point_except(w, h, p):
            r = p
            while r == p: r = (random.randint(0, w - 1), random.randint(0, h - 1))
            return r

        sp_list, ep_list = [], []
        if not self._parameters.routes:
            # create a key for every location, then select positions from it and
            # remove locations which have been assigned the maximum number of times
            choices = { (x, y): p.junction_capacity for x in xrange(p.grid_width) for y in xrange(p.grid_height) }
            while len(sp_list) < p.n_agents:
                rk = random.choice(choices.keys())
                if choices[rk] > 1: choices[rk] -= 1
                else: del choices[rk]

                sp_list.append(Point(rk[0], rk[1]))
                ep = random_point_except(p.grid_width, p.grid_height, rk)
                ep_list.append(Point(ep[0], ep[1]))

        else:
            routes = self._parameters.routes
            assert len(routes) == p.n_agents, "number of given routes not equal to n_agents parameter"
            for i in xrange(p.n_agents):
                r = routes[i]
                sp_list.append(r[0])
                ep_list.append(r[1])

        cars = self._world.get_agents()
        assert len(cars) == p.n_agents, "number of agents not equal to simulation parameter value"
        for i in xrange(p.n_agents):
            spn = self._world.get_grid().get_item_at(sp_list[i])
            epn = self._world.get_grid().get_item_at(ep_list[i])
            cars[i].set_route(spn, epn)

        if not self._parameters.routes:  # store routes in parameters if not already there
            route_points = [a.get_route() for a in self._world.get_agents()]
            self._parameters.routes = [(s, e) for (s, e) in route_points]

    def get_parameters(self):
        return self._parameters

    def do_step(self):
        """
        Runs one simulation step and returns True, unless the simulation is
        finished (params.max_days has been reached).
        """
        w, g = self._world, self._world.get_grid()
        cars = w.get_agents()
        t = TimeLord()
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

        if self._parameters.max_days > -1 and t.get_day() >= self._parameters.max_days:
            return False
        else:
            return True

    def print_grid(self, printing_grid):
        self._printing_grid = printing_grid
        print (self._printing_grid)

    def _print_jams(self):
        self._world.get_grid()._print_jams()

    def _print_jam_progression(self):
        print (self._jam_progression)
