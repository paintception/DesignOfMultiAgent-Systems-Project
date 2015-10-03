from utils import DIR


class Agent:
    def __init__(self, name, world):
        self._name = str(name)
        self._position = None
        self._start = None
        self._end = None
        self._velocity = 0
        self._direction = DIR.N
        self._route = None
        self._world = world

    def is_travelling(self):
        return (self._end == self._position) and not self._position is None

    def set_start_point(self, p):
        self._start = p

    def set_end_point(self, p):
        self._end = p

    def reset_pos(self):
        self._position = self._start
        # self._update_map_position()

    def get_pos(self):
        return self._position

    def set_position(self, new_pos):
        self._position = new_pos

    def get_next_stop(self):
        if self._route:
            return self._position.get_neighbour(self._route[0])
        else:
            return None

    def update(self):
        #from World import World
        #_world = World.getInstance()
        # TODO: do movement and memory updates
        # create list of (Point, weight) tuples to pass to get_path(), which
        # only gets called if we modify the weight list

        if not self._route:
            #No route is plotted
            self._route = self._world.get_grid().get_path(self._position, self._end)

            #Here if you like some fancy interface
            # self._route = self._world.get_grid().get_path(self._position, self._end, None, True)

            if self._route == []:
                raise Exception("could not find route for agent %s from %s to %s" % (self._name, self._start, self._end))

        #self._update_map_position()
        self._route.pop()

    def _update_map_position(self):
        self._position = self._position.get_neighbour(self._route.pop())

    def __str__(self):
        return "<<agent %s @ %s; %s -> %s; v: %.2f, d: %s>>" % \
            (self._name, self._position, self._start, self._end,
                self._velocity, self._direction)
