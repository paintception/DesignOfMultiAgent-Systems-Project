class Point():
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
