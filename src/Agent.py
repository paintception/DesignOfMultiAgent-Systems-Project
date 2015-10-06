from __future__ import print_function


class Agent:
    def __init__(self, name, world):
        self._name = str(name)
        self._position = None
        self._start = None
        self._end = None
        self._path = None
        self._world = world

    def is_travelling(self):
        return self._position is not None and (self._position != self._end)

    def set_route(self, sp, ep):
        """
        If sp has room for a new car, set given nodes as start and end points
        and teleport to start.
        """
        assert sp is not None and ep is not None, "route start and/or end point not set"

        if sp.has_room():
            self._start = sp
            self._end = ep

            print("  Agent %s: teleporting to start point %s (from %s)" % (self._name, sp, self._position))
            self._position = self._start
            self._start.add_car(self, False)
            self._determine_path()

            return True

        return False

    def restart_route(self):
        """
        Call set_route() with current start and end points.
        """
        return self.set_route(self._start, self._end)

    def reverse_route(self):
        """
        Call set_route() with current start and end points reversed.
        """
        return self.set_route(self._end, self._start)

    def get_pos_node(self):
        return self._position

    def set_position(self, new_pos):
        self._position = new_pos

    def get_next_dir(self):
        if self._path:
            return self._path[0]
        else:
            return -1

    def get_next_stop(self):
        if self._path:
            return self._position.get_neighbour(self._path[0])
        else:
            return None

    def update(self):
        self._path.pop(0)  # update path to destination

    def _determine_path(self):
        self._path = self._world.get_grid().get_path(self._position, self._end)
        # self._path = self._world.get_grid().get_path(self._position, self._end, None, True)

        if self._path is None:
            raise Exception("could not find route for agent %s from %s to %s" % (self._name, self._position, self._end))

    def __str__(self):
        return "<Agent %s @ %s; %s -> %s -- %s>" % \
            (self._name, self._position, self._start, self._end, self._path)
