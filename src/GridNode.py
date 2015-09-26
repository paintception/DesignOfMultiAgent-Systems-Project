class GridNode():
    def __init__(self):
        pass

    def get_grid_repr(self):
    	"""
    	Returns a concise, fixed with representation for display in the grid.
    	Idea: maybe colorize them?
    	"""
    	return "%02i[%02i]" % (0, 0)

    def __str__(self):
    	return "Node..."
