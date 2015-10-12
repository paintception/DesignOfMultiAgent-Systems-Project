from utils import Point
from TimeLord import TimeLord
from World import World



class GridNode(Point):
    def __init__(self, x, y, grid):
        from World import World
        p = World().get_parameters()

        Point.__init__(self, x, y)
        self._grid = grid
        self._car_stack = []
        self._neighbours = None
        self._streets = None

        # self.model_params = {'cars_in_node': 2, 'street_length': 1}
        # self._max_car_stack = self.model_params['cars_in_node']
        # self._max_cars_on_street = self.model_params['street_length']
        self._max_car_stack = p.junction_capacity
        self._max_cars_on_street = p.street_capacity
        self._junction_throughput = p.junction_throughput  # was MAX_ROAD_PUSHES before
        self._street_throughput = p.street_throughput  # was MAX_MOVES before

    def set_neighbours(self):
        grid = self._grid
        self._neighbours, self._streets = {}, {}
        self._center_jams=[]
        self._street_jams={}

        for drx in xrange(4):
            nb = grid.get_neighbour(self, drx)
            self._neighbours[drx] = nb

            # make sure all directions have a key but mark non-existent ones with a None
            if nb: self._streets[drx] = []
            else: self._streets[drx] = None


            if nb: self._street_jams[drx] = []
            else: self._street_jams[drx] = None

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
        First move cars on streets to their new nodes (max: _junction_throughput per
        street), send event to cars to inform them about (not) being moved -
        JUNCTION_ARRIVED | JUNCTION_REJECTED.
        Then move cars from junction to streets (max: _street_throughput), send events
        here as well - STREET_ARRIVED | STREET_REJECTED.
        """
        stuck_count = 0  # in case we want to check for deadlocks
        for k in self._streets:
            for i in xrange(self._junction_throughput):
                if not self._transfer_car(k):
                    stuck_count += 1

        ci, cars_to_move = 0, self._street_throughput
        while cars_to_move > 0:
            if ci >= len(self._car_stack):
                break
            if self._move_car_to_street():
                cars_to_move -= 1
                ci -= 1  # compensate for car popped from _car_stack
            ci += 1

    def remove_car(self, car):
        """
        Removes car from main stack.
        """
        self._car_stack.remove(car)

    def add_car(self, car, call_update=True):
        """
        Inserts car into the main stack of a node.
        Agents adding themselves to their initial position should call with call_update=False
        """
        if len(self._car_stack) < self._max_car_stack:
            self._car_stack.append(car)
            car.set_position(self)
            # if call_update: car.update()  # done in Agent's event handler now
            # print('test_add_car')
            return True
        else:
            return False

    def _move_car_to_street(self):
        """
        Moves the next car from the main stack to the street stack it wants to go to next.
        """
        from Grid import MovementEvent, GRID_EVENT as GE
        t = TimeLord()
        time= t.get_timestamp()
        if len(self._car_stack) > 0:
            car = self._car_stack[0]
            next_dir, next_stop = car.get_next_dir(), car.get_next_stop()

            #print("car %s" % car)
            #print("next stop: %s (%i), route: %s" % (next_stop, next_dir, car._path))
            
            if next_stop is None:
                #print("Route done.")
                return False

            street_stack = self._streets[next_dir]

            # print("room for car on street? %s" % (len(street_stack) < self._max_cars_on_street))
            if len(street_stack) < self._max_cars_on_street:
                street_stack.append(car)
                self._car_stack.pop(0)
                #print('moving')
                car.handle_movement_event(MovementEvent(GE.STREET_ARRIVED, time, self))
                return True
            else:
                car.handle_movement_event(MovementEvent(GE.STREET_REJECTED, time, self))
                self._add_center_jam(time)
                return False
        else:
            return True

    def _transfer_car(self, direction):
        """
        Moves the next car from the street stack to the mainstack of node in the given direction.
        """
        from Grid import MovementEvent, GRID_EVENT as GE
        t = TimeLord()
        time = t.get_day_time()
        street_stack = self._streets[direction]
        if street_stack and len(street_stack) > 0:
            car = street_stack[0]
            to_node = self._neighbours[direction]
            if to_node.add_car(car):
                street_stack.pop(0)
                car.handle_movement_event(MovementEvent(GE.JUNCTION_ARRIVED, time, self))
                # print('car_transfered')
                return True
            else:
                car.handle_movement_event(MovementEvent(GE.JUNCTION_REJECTED, time, self))
                self._add_street_jam(direction,time)
                return False

        return True

    def get_grid_repr(self):
        """
        Returns a concise, fixed with representation for display in the grid.
        Idea: maybe colorize them?
        """
        return "%02i/%01i" % (0, 0)

    def _add_center_jam(self, time):
        print ("jam at: (%i, %i)" % (self.x, self.y))
        self._center_jams.append(time)
        print("jams:", self._center_jams)

    def _add_street_jam(self, drx, time):
        World().update_counter()
        self._street_jams[drx].append(time)
        print ("jam at street: %i (%i, %i), total: %i" % (drx, self.x, self.y, World().get_counter()))
        print("jams:", self._street_jams[drx])

    def jsonifiable(self):
        result = {
            'main': [c.get_name() for c in self._car_stack],
            'streets': {}
        }
        for k in self._streets:
            s = self._streets[k]
            if s is not None: result['streets'][k] = [c.get_name() for c in s]
            else: result['streets'][k] = None

        return result

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'GN(%i, %i)' % (self.x, self.y)

    def _print_node_jams(self):
        import collections
        if self._center_jams:
            test= [item for item, count in collections.Counter(self._center_jams).items() if count > 1]
            print("Node %s %s had %s jams at crossing," %(self.x, self.y, test))
        for s in self._street_jams:
            if self._street_jams[s]:
                test= [item for item, count in collections.Counter(self._street_jams[s]).items() if count > 1]
                print("Node %s %s had %s jams at street: %s," %(self.x, self.y, test, s))

    def make_weights(self):
        s=0
        for x in self._street_jams:
            s += len(x)
        s=s/len(self._street_jams)
        w= len(self._center_jams)+s
        return w

    def has_Jam(self):
        s=False
        for x in self._street_jams:
            if len(x) > 0:
                s=True

        if len(self._center_jams) > 0 or s:
            return True

        else:
            return False