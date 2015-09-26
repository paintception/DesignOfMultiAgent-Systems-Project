from __future__ import print_function, division
from random import random, randint
import numpy as np
from utils import Point
import astar


class Grid():
    """
    A grid class with a list as content of each cell. This list can be used to
    add arbitrary content to the grid.

    FIXME: n_blocked is ignored by _astar_grid, while it should mimic _grid
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # _grid is used to contain refs to agents (aka cars) nearby
        self._grid = self._create_matrix(width, height)

        # _astar_grid is used as a basis in get_path() for the A* path finder
        self._astar_grid = np.zeros((self.width, self.height), dtype=np.int)
        self._astar = astar.AStar(self.width, self.height)

    def get_item_at(self, x, y=None):
        """
        Returns the item at the given position.
        """
        x, y = self._check_coords(x, y)

        return self._grid[y][x]

    def get_random_position(self):
        """
        Returns a random grid position on an accessible cell (i.e. on a road or junction).
        """
        x, y = randint(0, self.width - 1), randint(0, self.height - 1)
        return Point(x, y)

    def get_path(self, src, tgt, avoid=None, show_route=False):
        """
        Find a path from src to tgt, avoiding points specified in avoid.
        """
        temp_grid = np.copy(self._astar_grid)
        if type(avoid) is list:
            for p in avoid:
                temp_grid[p.y][p.x] = 1

        r = self._astar.path_find(temp_grid, self.width, self.height,
                                  (src.x, src.y), (tgt.x, tgt.y))

        if (show_route):
            self._show_route(temp_grid, src, tgt, r)

        if len(r) > 0:
            return [int(d) for d in r]

        return None

    def _create_matrix(self, width, height):
        from GridNode import GridNode

        def pick_edge_point():
            y = randint(0, height - 1)
            if (y == 0) or (y == (height - 1)):
                x = randint(0, width - 1)
            else:
                if random() >= 0.5:
                    x = 0
                else:
                    x = -1
            return (x, y)

        # create a list of lists (2D matrix) with another empty list as content
        matrix = [[GridNode() for i in xrange(width)] for j in xrange(height)]

        return matrix

    def _check_coords(self, x, y=None):
        """
        Transforms given 'real' coordinates to 'junction' coordinates usable
        with self._grid. The x parameter is allowed to be a Point object.
        Coordinates are checked to be within bounds, to lie on the junction grid
        and to lie on a junction.
        If round_to_junction is true, coordinates will be 'snapped' to the
        nearest junction (and the last assert will thus never trigger).
        """
        if isinstance(x, Point):
            x, y = x.x, x.y

        assert x >= 0 and x < self.width and y >= 0 and y < self.height, \
            "grid coordinates out of bounds (%i, %i)" % (x, y)

        return x, y

    def _show_route(self, scribble_map, src, tgt, route):
        if len(route) > 0:
            print("showing route: %s" % route)
        else:
            print("no route to show")
            return

        from matplotlib import pyplot
        dirs = astar.get_directions_array()

        x = src.x
        y = src.y
        scribble_map[y][x] = 2
        for i in range(len(route)):
            j = int(route[i])
            x += dirs[0][j]
            y += dirs[1][j]
            scribble_map[y][x] = 3
        scribble_map[y][x] = 4

        pyplot.pcolor(scribble_map)
        pyplot.show()

    def __str__(self):
        rows = []
        for y in xrange(self.height):
            rows.append(' '.join(map(lambda n: "%s" % n.get_grid_repr(), self._grid[y])))
        return '\n'.join(rows)
