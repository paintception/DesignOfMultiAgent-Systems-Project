from __future__ import print_function, division
from utils import Point


class Agent:
    def __init__(self, name, world):
        self._name = str(name)
        self._position = None
        self._start = None
        self._end = None
        self._path = None
        self._world = world

        self._travel_start_time = -1
        self._total_path_distance = -1
        self._travel_velocity_ratio = 0
        self._waiting_times = {}
        self._stuck_time = 0

    def is_travelling(self):
        return self._position is not None and (self._position != self._end)

    def get_name(self):
        return self._name

    def set_route(self, sp, ep):

        from TimeLord import TimeLord
        t = TimeLord()

        """
        If sp has room for a new car, set given nodes as start and end points
        and teleport to start.
        """
        assert sp is not None and ep is not None, "route start and/or end point not set"

        if sp.has_room():
            self._start = sp
            self._end = ep

           # print("  Agent %s: teleporting to start point %s (from %s)" % (self._name, sp, self._position))
            if self._position:
                self._position.remove_car(self)
            self._position = self._start
            self._start.add_car(self, False)
            self._determine_path()
            self._travel_start_time = t.get_timestamp()
            self._waiting_times[self._travel_start_time] = []

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

    def get_route(self):
        return (Point(self._start.x, self._start.y), Point(self._end.x, self._end.y))

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

    def handle_movement_event(self, ev):
        """
        Called when a movement occurs (or could not occur).
        ev contains: type, timestamp, new_pos.
        """
        from Grid import GRID_EVENT as GE
        print("agent %s event: %s" % (self._name, ev))

        if ev.ev_type == GE.JUNCTION_ARRIVED:
            if self._position != ev.old_pos:  # check if we have actually moved
                self._path.pop(0)

                # record waiting time
                entry = (ev.old_pos.x, ev.old_pos.y, self._stuck_time)
                self._waiting_times[self._travel_start_time].append(entry)
                print("wt list:", self._waiting_times)
                print("ratio:", self.get_velocity_ratio())

            self._stuck_time = 0

        elif ev.ev_type == GE.JUNCTION_REJECTED:
            self._stuck_time += 1
        elif ev.ev_type == GE.STREET_ARRIVED:
            self._stuck_time = 0
        elif ev.ev_type == GE.STREET_REJECTED:
            self._stuck_time += 1

    def _determine_path(self):
        self._path = self._world.get_grid().get_path(self._position, self._end)
        # self._path = self._world.get_grid().get_path(self._position, self._end, None, True)

        if self._path is not None:
            self._total_path_distance = len(self._path)
        else:
            self._total_path_distance = -1
            raise Exception("could not find route for agent %s from %s to %s" % (self._name, self._position, self._end))

    def get_route(self):
        return(self._start, self._end)

    def get_waiting_times(self):
        return self._waiting_times

    # TODO: take self._stuck_time into account, otherwise this will only be accurate if cars can actually move
    def get_velocity_ratio(self):
        distance_to_travel = len(self._path)
        distance_travelled = self._total_path_distance - distance_to_travel

        # compute travel_time from wait list: using current timestamp will be incorrect once the agent has reached its destination
        wt_list = self._waiting_times[self._travel_start_time]
        travel_time = len(wt_list) + sum(map(lambda e: e[2], wt_list))  # number of visited junctions + waiting time at each of them
        # assert(distance_travelled == len(wt_list))

        return travel_time / distance_travelled

    def __str__(self):
        return "<Agent %s @ %s; %s -> %s -- %s>" % \
            (self._name, self._position, self._start, self._end, self._path)
