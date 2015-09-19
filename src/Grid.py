from __future__ import print_function

# The program creates a grid where our agents will drive through, the grid is created by the function create_matrix 
# and is represented by a list of lists. The function receives as input the width (matrix_width) and the height (matrix_height) of the maze,
# n_blocked which is the number of cells of the matrix that will correspond to the obstancles the agents will encounter when driving, these are made # randomly and represented inside the grid by 1's. The same logic has been used for the creation of some starting points (n_enter) and destinations # (n_exits) but this time they may only "appear" on the borders of the maze.

# YELLOW = STARTING POINTS
# BROWN = DESTINATION POINTS
# LIGHT_BLUE = OBSTACLES


class Grid():
    def __init__(self, width, height, n_blocked=0):
        self._grid = self._create_matrix(width, height, n_blocked)

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

        matrix = [[0 for i in xrange(width)] for j in xrange(height)]

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


if __name__ == '__main__':
    import numpy
    from matplotlib import pyplot
    import astar

    grid_size = 100
    dirs = astar.getDirectionsArray()
    grid = Grid(grid_size, grid_size, 4000)
    start, end = (0, 0), (50, 50)
    route = astar.path_find(grid._grid, grid_size, grid_size, start, end)

    print("route: %s" % route)

    if len(route) > 0:
        x = start[0]
        y = start[1]
        grid._grid[y][x] = 2
        for i in range(len(route)):
            j = int(route[i])
            x += dirs[0][j]
            y += dirs[1][j]
            grid._grid[y][x] = 3
        grid._grid[y][x] = 4

    np_matrix = numpy.asarray(grid._grid)
    pyplot.pcolor(np_matrix)
    pyplot.show()


    # matrix = grid._create_matrix(100, 100, 200, 25, 12)
    # np_matrix = numpy.asarray(matrix)
    # pyplot.pcolor(np_matrix)
    # pyplot.show()
    # print(Matrix)
