#!/usr/bin/env python

# The program creates a grid where our agents will drive through, the grid is created by the function create_matrix 
# and is represented by a list of lists. The function receives as input the width (matrix_width) and the height (matrix_height) of the maze,
# n_blocks which is the number of cells of the matrix that will correspond to the obstancles the agents will encounter when driving, these are made # randomly and represented inside the grid by 1's. The same logic has been used for the creation of some starting points (n_enter) and destinations # (n_exits) but this time they may only "appear" on the borders of the maze.

# YELLOW = STARTING POINTS
# BROWN = DESTINATION POINTS
# LIGHT_BLUE = OBSTACLES

import numpy
import random
from matplotlib import pyplot


def create_matrix(matrix_height, matrix_width,
                  n_blocks, n_enter, n_exits):
    def pick_edge_point():
        y = random.randint(0, matrix_height - 1)
        if (y == 0) or (y == (matrix_height - 1)):
            x = random.randint(0, matrix_width - 1)
        else:
            if random.random() >= 0.5:
                x = 0
            else:
                x = -1
        return (x, y)

    Matrix = [[0 for i in xrange(matrix_width)] for j in xrange(matrix_height)]

    # Definition of 0s matrix this corresponds to the Maze where the vehicles will drive, 
    # Lista di Liste
    # Lista = [[1,2,3] for i in xrange(10)]

    for i in xrange(n_blocks):
        x_to_block = random.randint(0, matrix_width - 1)
        y_to_block = random.randint(0, matrix_height - 1)

        Matrix [y_to_block] [x_to_block] = 1    # 1 means that there is an obstacle, and you can't pass

    for i in xrange(n_enter):
        x, y = pick_edge_point()
        Matrix[y][x] = 2  # 2 means it's a starting point

    for i in xrange(n_exits):
        x, y = pick_edge_point()
        Matrix[y][x] = 3  # 3 means it's an ending point

    return Matrix


if __name__ == '__main__':
    Matrix = create_matrix(100, 100, 200, 25, 12)
    Matrix_2 = numpy.asarray(Matrix)
    pyplot.pcolor(Matrix_2)
    pyplot.show()

    #print(Matrix)
