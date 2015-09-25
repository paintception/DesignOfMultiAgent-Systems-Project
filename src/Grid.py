from __future__ import print_function, division
import numpy as np
from utils import Point
import astar


class Grid():
    """
    A grid class with a list as content of each cell. This list can be used to
    add arbitrary content to the grid.

    FIXME: n_blocked is ignored by _astar_grid, while it should mimic _grid
    """
    def __init__(self, width, height, junction_step=1, n_blocked=0):
        self.width = width
        self.height = height
        self.junction_step = junction_step

        # These are calculated such that we have exactly the requested number of junctions
        self._real_width = (width - 1) * junction_step + 1
        self._real_height = (height - 1) * junction_step + 1

        # _grid is used to contain refs to agents (aka cars) nearby
        self._grid = self._create_matrix(width, height, n_blocked)

        # _astar_grid is used as a basis in get_path() for the A* path finder
        self._astar_grid = np.zeros((self._real_height, self._real_width), dtype=np.int)
        for y in xrange(self._real_height):
            for x in xrange(self._real_width):
                if y % junction_step != 0 and x % junction_step != 0:
                    self._astar_grid[y][x] = 1

        self._astar = astar.AStar(self._real_width, self._real_height, self.junction_step)

    def get_items_at(self, x, y=None):
        """
        Returns the list of items at the given position, it can be manipulated.
        """
        x, y = self._transform_coords(True, x, y)

        return self._grid[int(y)][int(x)]

    def clear_items_at(self, x, y=None):
        del self.get_items_at(x, y)[:]

    def remove_item_at(self, v, x, y=None):
        self.get_items_at(x, y).remove(v)

    def append_item_at(self, v, x, y=None):
        self.get_items_at(x, y).append(v)

    def get_random_position(self):
        """
        Returns a random grid position on an accessible cell (i.e. on a road or junction).
        """
        from random import randint

        x = randint(0, self._real_width - 1)
        if x % self.junction_step == 0:
            y = randint(0, self._real_height - 1)
        else:
            y = randint(0, self.height - 1) * self.junction_step

        return Point(x, y)

    def round_to_junction(self, x, y=None):
        """
        Rounds given coordinates to a multiple of self.junction_step.
        """
        from utils import number_rounder
        rounder = number_rounder(self.junction_step)
        point_given = isinstance(x, Point)

        if point_given:
            x, y = x.x, x.y

        x, y = rounder(x), rounder(y)

        if point_given:
            return Point(x, y)
        else:
            return x, y

    def get_path(self, src, tgt, avoid=None, show_route=False):
        """
        Find a path from src to tgt, avoiding points specified in avoid.
        """
        temp_grid = np.copy(self._astar_grid)
        if type(avoid) is list:
            for p in avoid:
                temp_grid[p.y][p.x] = 1

        r = self._astar.path_find(temp_grid, self._real_width, self._real_height,
                                  (src.x, src.y), (tgt.x, tgt.y))

        if (show_route):
            self._show_route(temp_grid, src, tgt, r)

        if len(r) > 0:
            return [int(d) for d in r]

        return None

    def _create_matrix(self, width, height, n_blocked=0, n_enter=0, n_exits=0):
        from random import random, randint

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
        matrix = [[[] for i in xrange(width)] for j in xrange(height)]

        for i in xrange(n_blocked):
            x_to_block = randint(0, width - 1)
            y_to_block = randint(0, height - 1)

            # 1 means that there is an obstacle, and you can't pass
            matrix[y_to_block][x_to_block] = 1

        for i in xrange(n_enter):
            x, y = pick_edge_point()
            matrix[y][x] = 2  # 2 means it's a starting point

        for i in xrange(n_exits):
            x, y = pick_edge_point()
            matrix[y][x] = 3  # 3 means it's an ending point

        return matrix

    def _transform_coords(self, round_to_junction, x, y=None):
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

        assert x >= 0 and x < self._real_width and y >= 0 and y < self._real_height, \
            "grid coordinates out of bounds (%i, %i)" % (x, y)

        x_on_jgrid = x % self.junction_step == 0
        y_on_jgrid = y % self.junction_step == 0

        assert x_on_jgrid or y_on_jgrid, \
            "grid coordinates not on road (%i, %i)" % (x, y)

        if round_to_junction:
            x, y = self.round_to_junction(x, y)
        else:
            assert x_on_jgrid and y_on_jgrid, \
                "grid coordinates not on junction (%i, %i)" % (x, y)

        return x / self.junction_step, y / self.junction_step

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
            rows.append(' '.join(map(lambda c: "%02i" % len(c), self._grid[y])))
        return '\n'.join(rows)
