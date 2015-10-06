from utils import Point


class GridNode(Point):
    """
    MAX_ROAD_PUSHES defines the number car transfers to other nodes per timestep.
    MAX_MOVES defines the number of moves from the main stack to street stacks per timestep.
    """

    MAX_ROAD_PUSHES = 1
    MAX_MOVES = 4

    def __init__(self, x, y, grid):
        Point.__init__(self, x, y)
        self._grid = grid
        self._car_stack = []
        self._neighbours = None
        self._streets = None

        self.model_params = {'cars_in_node': 3, 'street_length': 5}
        self._max_car_stack = self.model_params['cars_in_node']
        self._max_cars_on_street = self.model_params['street_length']

    def set_neighbours(self):
        grid = self._grid
        self._neighbours, self._streets = {}, {}
        for drx in xrange(4):
            nb = grid.get_neighbour(self, drx)
            self._neighbours[drx] = nb

            # make sure all directions have a key but mark non-existent ones with a None
            if nb: self._streets[drx] = []
            else: self._streets[drx] = None

    def get_neighbour(self, direction):
        return self._neighbours[direction]

    def get_cars(self):
        temp = [len(self._car_stack)]
        for k in self._streets:
            temp.append(self._streets[k])

        return temp

    def has_room(self):
        return len(self._car_stack) < self._max_car_stack

    def update(self):
        """
        First move cars on streets to their new nodes (max MAX_ROAD_PUSHES per
        street), send event to cars to inform them about (not) being moved -
        JUNCTION_ARRIVED | JUNCTION_REJECTED.
        Then move cars from junction to streets (max MAX_MOVES), send events
        here as well - STREET_ARRIVED | STREET_REJECTED.
        """
        stuck_count = 0  # in case we want to check for deadlocks
        for k in self._streets:
            for i in xrange(self.MAX_ROAD_PUSHES):
                if not self._transfer_car(k):
                    stuck_count += 1

        ci, cars_to_move = 0, self.MAX_MOVES
        while cars_to_move > 0:
            if ci >= len(self._car_stack):
                break
            if self._move_car_to_street():
                cars_to_move -= 1
                ci -= 1  # compensate for car popped from _car_stack
            ci += 1

    def add_car(self, car, call_update=True):
        """
        Inserts car into the main stack of a node.
        Agents adding themselves to their initial position should call with call_update=False
        """
        if len(self._car_stack) < self._max_car_stack:
            self._car_stack.append(car)
            car.set_position(self)
            # if call_update: car.update()  # done in Agent's event handler now
            print('test_add_car')
            return True
        else:
            return False

    def _move_car_to_street(self):
        """
        Moves the next car from the main stack to the street stack it wants to go to next.
        """
        from Grid import MovementEvent, GRID_EVENT as GE
        from World import World

        if len(self._car_stack) > 0:
            car = self._car_stack[0]
            next_dir, next_stop = car.get_next_dir(), car.get_next_stop()

            print("car %s" % car)
            print("next stop: %s (%i), route: %s" % (next_stop, next_dir, car._path))

            if next_stop is None:
                print("Route done.")
                return False

            street_stack = self._streets[next_dir]
            if len(street_stack) < self._max_cars_on_street:
                street_stack.append(car)
                self._car_stack.pop(0)
                print('moving')
                car.handle_movement_event(MovementEvent(GE.STREET_ARRIVED, 0, self))
                return True
            else:
                car.handle_movement_event(MovementEvent(GE.STREET_REJECTED, 0, self))
                return False
        else:
            return True

    def _transfer_car(self, direction):
        """
        Moves the next car from the street stack to the mainstack of node in the given direction.
        """
        from Grid import MovementEvent, GRID_EVENT as GE

        street_stack = self._streets[direction]
        if street_stack and len(street_stack) > 0:
            car = street_stack[0]
            if self._neighbours[direction].add_car(car):
                street_stack.pop(0)
                car.handle_movement_event(MovementEvent(GE.JUNCTION_ARRIVED, 0, self))
                print('car_transfered')
                return True
            else:
                car.handle_movement_event(MovementEvent(GE.JUNCTION_REJECTED, 0, self))
                return False

        return True

    def get_grid_repr(self):
        """
        Returns a concise, fixed with representation for display in the grid.
        Idea: maybe colorize them?
        """
        return "%02i/%01i" % (0, 0)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'GN(%i, %i)' % (self.x, self.y)
