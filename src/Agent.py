from utils import DIR, Point


class Agent:
    def __init__(self, world, name):
        self._world = world
        self._name = str(name)
        self._last_position = Point(0, 0)
        self._position = Point(0, 0)
        self._start = Point()
        self._end = Point()
        self._velocity = 0
        self._direction = DIR.N
        self._route = None

        world.get_grid().append_item_at(self, self._position)

    def is_travelling(self):
        return self._end.is_set()

    def set_start_point(self, p):
        self._start = p

    def set_end_point(self, p):
        self._end = p

    def reset_pos(self):
        self._last_position = self._position
        self._position = self._start
        self._update_map_position()

    def get_pos(self):
        return self._position

    def update(self):
        self._last_position = self._position

        # TODO: do movement and memory updates
        # create list of (Point, weight) tuples to pass to get_path(), which
        # only gets called if we modify the weight list

        if not self._route:
            #No route is plotted
            self._route = self._world.get_grid().get_path(self._position, self._end)

            #Here if you like some fancy interface
            # self._route = self._world.get_grid().get_path(self._position, self._end, None, True)
            print "agent %s route: %s" % (self._name, self._route)

            if self._route == []:
                raise Exception("could not find route for agent %s from %s to %s" % (self._name, self._start, self._end))

        self._update_map_position()

    def _update_map_position(self):
        lp = self._last_position.get_rounded()
        np = self._position.get_rounded()

        if lp != np:
            g = self._world.get_grid()
            g.remove_item_at(self, lp)
            g.append_item_at(self, np)

    def __str__(self):
        return "<<agent %s @ %s; %s -> %s; v: %.2f, d: %s>>" % \
            (self._name, self._position, self._start, self._end,
                self._velocity, self._direction)
