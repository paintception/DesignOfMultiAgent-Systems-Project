import Grid as Grid
class GridNode():
    def __init__(self, x, y, world):
        self._x = x
	self._y = y
	self._car_stack = []
	self._neighbours = {
		'N' : Grid.get_neighbour(self, 0), 
		'E' : Grid.get_neighbour(self, 1),
		'S' : Grid.get_neighbour(self, 2),
		'W' : Grid.get_neighbour(self, 3)}
	self._streets = {
		Grid.get_neighbour(self, 0) : [None],
		Grid.get_neighbour(self, 1) : [None],
		Grid.get_neighbour(self, 2) : [None],
		Grid.get_neighbour(self, 3) : [None]}
	self._max_car_stack = world.get_model_parameters()['cars_in_node']
	self._max_car_on_street = world.get_model_parameters()['street_length']

    def get_new_car(self, car):
	if len(_car_stack) < _max_car_stack:
		_car_stack.append(car)
		return 1
	else:
		return 0
	
    def move_car(self, target_node):
	_car = _car_stack.pop(0)
	if len(_streets[_car.get_next_stop(self)]) < _max_car_on_street:
		_streets[_car.get_next_stop(self)].append() 
		return 1
	else:
		_car_stack.append(car)
		return 0

   def push_car(self, direction):
	if len(_streets[_neighbour[direction]])> 0: 
		car = _streets[_neighbour[direction]][0]
		if _neighbours[direction].get_new_car(car) = 1:
			return 1
		else:
			 _streets[_neighbour[direction]].insert(0,car)
    
    def get_grid_repr(self):
    	"""
    	Returns a concise, fixed with representation for display in the grid.
    	Idea: maybe colorize them?
    	"""
    	return "%02i/%01i" % (0, 0)

    def __str__(self):
    	return "Node..."
