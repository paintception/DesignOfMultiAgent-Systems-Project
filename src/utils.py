from __future__ import division


def enum(**enums):
    return type('Enum', (), enums)

# These numbers match the indices in Astar.py.
DIR = enum(N=0, E=1, S=2, W=3)

DIR_DELTA = enum(N=(0, -1), E=(1, 0), S=(0, 1), W=(-1, 0))


def number_rounder(to_number):
    return lambda v: int(round(v / to_number) * to_number)


class Point():
    """
    A simple 2D point.
    """
    def __init__(self, x=-1, y=-1):
        self.x = x
        self.y = y

    def get_rounded(self):
        return Point(round(self.x), round(self.y))

    def is_set(self):
        return self.x >= 0 and self.y >= 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "(%.2f, %.2f)" % (self.x, self.y)

    def __repr__(self):
        return "Point(%f, %f)" % (self.x, self.y)
