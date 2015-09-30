             

class GridNode():
    """
    ROADPUSHES gives the number of pusches to the road per timestep.
    MAX_MOVES gives the number of pushes from the roades per timestep.
    """
    ROADPUSHES = 1 
    MAX_MOVES = 4

    def __init__(self, x, y, grid):


        self._x = x
        self._y = y
        self._grid = grid
        self._car_stack = []
        self._neighbours = None
        self._streets = None
        self.model_params = {'cars_in_node' : 3 , 'street_length' : 5 }
        self._max_car_stack = self.model_params['cars_in_node']
        self._max_car_on_street = self.model_params['street_length']

    def set_neighbours(self):
        grid = self._grid
        nbs = {
            0 : grid.get_neighbour(self, 0), 
            1 : grid.get_neighbour(self, 1),
            2 : grid.get_neighbour(self, 2),
            3 : grid.get_neighbour(self, 3)}
        self._neighbours = nbs
        self._streets = {}
        if nbs[0]: self._streets[nbs[0]] = []
        if nbs[1]: self._streets[nbs[1]] = []
        if nbs[2]: self._streets[nbs[2]] = []
        if nbs[3]: self._streets[nbs[3]] = []

    def get_new_car(self, car): 
        """
        incerts car into the main stack of a node
        """
        if len(self._car_stack) < self._max_car_stack:
            self._car_stack.append(car)
            car.update()
            return 1
        else:
            return 0
    
    def move_car(self): 
        """
        moves the next car from the main stack to the streetstack it wants to go to next
        """
        if len(_car_stack) > 0:    
            _car = _car_stack.pop(0)
            if len(_streets[_car.get_next_stop(self)]) < _max_car_on_street:
                _streets[_car.get_next_stop(self)].append() 
                return 1
            else:
                _car_stack.append(car)
                return 0
        else:
            return 1

    def push_car(self, direction):
        """
        moves the next car from the street stack to the mainstack of the corresponding node
        """
        street_stack = self._streets[direction]
        if len(street_stack)> 0:
            car = street_stack[0]
            #FIXME: probably should pop the car and reinsert *or* only pop if get_new_car() succeeded
            if direction.get_new_car(car) == 1:
                return 1
            else:
                street_stack.insert(0,car)
                return 0
        return 1
        
    def get_grid_repr(self):
        """
        Returns a concise, fixed with representation for display in the grid.
        Idea: maybe colorize them?
        """
        return "%02i/%01i" % (0, 0)

    def update_node(self):
        deadstack=0
        """
        in case we want to check for deadlocks
        """
        for i in xrange(self.ROADPUSHES):
            for k in self._streets:
                if not self.push_car(k):
                    deadstack += 1
        ci = 0
        cars_to_move = self.MAX_MOVES
        while cars_to_move > 0:
            if ci >= len(self._car_stack):
                break
            self.move_car()
            cars_to_move -= 1
            ci += 1

    def get_neighbour(self, direction):
        return self._neighbours[direction]

    def get_pos(self):
        return self._x, self._y

    def __str__(self):
        return "Node..."
