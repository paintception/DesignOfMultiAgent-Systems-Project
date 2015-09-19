class Point():
    def __init__(self, x=-1, y=-1):
        self.x = x
        self.y = y

    def is_set(self):
        return self.x > -1 and self.y > -1

    def __str__(self):
        return "(%.2f, %.2f)" % (self.x, self.y)
