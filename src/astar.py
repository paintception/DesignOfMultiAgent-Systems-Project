"""
An A* path finder implementation.
About faster alternatives:
- orthogonal jump point search? http://qiao.github.io/PathFinding.js/visual/
- overview: http://aigamedev.com/open/tutorial/symmetry-in-pathfinding/
- jump point search: http://gamedevelopment.tutsplus.com/tutorials/how-to-speed-up-a-pathfinding-with-the-jump-point-search-algorithm--gamedev-5818
"""

from heapq import heappush, heappop  # for priority queue


NUM_DIRECTIONS = 4  # number of possible directions to move on the map

if NUM_DIRECTIONS == 4:
    # N E S W
    _DIRS_X = [0, 1, 0, -1]
    _DIRS_Y = [-1, 0, 1, 0]
elif NUM_DIRECTIONS == 8:
    # N NE E SE S SW W NW
    _DIRS_X = [0, 1, 1, 1, 0, -1, -1, -1]
    _DIRS_Y = [-1, -1, 0, 1, 1, 1, 0, -1]


def get_directions_array():
    return (_DIRS_X, _DIRS_Y)


# from: http://stackoverflow.com/a/1601774
def unshared_copy(inList):
    if isinstance(inList, list):
        return list( map(unshared_copy, inList) )
    return inList


class AStar():
    def __init__(self, width, height, junction_step):
        self.w = 0
        self.h = 0
        self.js = 0
        self._create_maps(width, height, junction_step)


    def path_find(self, map, width, height, start_pos, end_pos):
        """
        Find a path from start_pos to end_pos on map which has given width and height.
        """
        self._create_maps(width, height, self.junction_step)
        return self._path_find(map, width, height, NUM_DIRECTIONS, _DIRS_X, _DIRS_Y,
                start_pos[0], start_pos[1], end_pos[0], end_pos[1])


    def _create_maps(self, width, height, junction_step):
        if self.w != width or self.h != height or self.junction_step != junction_step:
            self.w = width
            self.h = height
            self.junction_step = junction_step
            self._closed_nodes_map = []  # map of closed (tried-out) nodes
            self._open_nodes_map = []  # map of open (not-yet-tried) nodes
            self._dir_map = []  # map of dirs

            row = [0] * width
            for i in range(height):  # create 2d arrays
                self._closed_nodes_map.append(list(row))
                self._open_nodes_map.append(list(row))
                self._dir_map.append(list(row))

            for y in xrange(height):
                for x in xrange(width):
                    if y % junction_step != 0 and x % junction_step != 0:
                        self._closed_nodes_map[y][x] = 1

    # A-star algorithm.
    # The path returned will be a string of digits of directions.
    def _path_find(self, the_map, n, m, dirs, dx, dy, xA, yA, xB, yB):
        # import math

        closed_nodes_map = unshared_copy(self._closed_nodes_map)
        open_nodes_map = unshared_copy(self._open_nodes_map)
        dir_map = unshared_copy(self._dir_map)

        pq = [[], []]  # priority queues of open (not-yet-tried) nodes
        pqi = 0  # priority queue index
        # create the start node and push into list of open nodes
        n0 = _node(xA, yA, 0, 0)
        n0.updatePriority(xB, yB)
        heappush(pq[pqi], n0)
        open_nodes_map[yA][xA] = n0.priority  # mark it on the open nodes map

        # A* search
        while len(pq[pqi]) > 0:
            # get the current node w/ the highest priority
            # from the list of open nodes
            n1 = pq[pqi][0]  # top node
            n0 = _node(n1.xPos, n1.yPos, n1.distance, n1.priority)
            x = n0.xPos
            y = n0.yPos
            heappop(pq[pqi])  # remove the node from the open list
            open_nodes_map[y][x] = 0
            closed_nodes_map[y][x] = 1  # mark it on the closed nodes map

            # quit searching when the goal is reached
            # if n0.estimate(xB, yB) == 0:
            if x == xB and y == yB:
                # generate the path from finish to start
                # by following the dirs
                path = ''
                while not (x == xA and y == yA):
                    j = dir_map[y][x]
                    c = str((j + dirs / 2) % dirs)
                    path = c + path
                    x += dx[j]
                    y += dy[j]
                return path

            # generate moves (child nodes) in all possible dirs
            for i in range(dirs):
                xdx = x + dx[i]
                ydy = y + dy[i]
                if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1
                        or the_map[ydy][xdx] == 1 or closed_nodes_map[ydy][xdx] == 1):
                    # generate a child node
                    m0 = _node(xdx, ydy, n0.distance, n0.priority)
                    m0.nextMove(dirs, i)
                    m0.updatePriority(xB, yB)
                    # if it is not in the open list then add into that
                    if open_nodes_map[ydy][xdx] == 0:
                        open_nodes_map[ydy][xdx] = m0.priority
                        heappush(pq[pqi], m0)
                        # mark its parent node direction
                        dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                    elif open_nodes_map[ydy][xdx] > m0.priority:
                        # update the priority
                        open_nodes_map[ydy][xdx] = m0.priority
                        # update the parent direction
                        dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                        # replace the node
                        # by emptying one pq to the other one
                        # except the node to be replaced will be ignored
                        # and the new node will be pushed in instead
                        while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy):
                            heappush(pq[1 - pqi], pq[pqi][0])
                            heappop(pq[pqi])
                        heappop(pq[pqi])  # remove the target node
                        # empty the larger size priority queue to the smaller one
                        if len(pq[pqi]) > len(pq[1 - pqi]):
                            pqi = 1 - pqi
                        while len(pq[pqi]) > 0:
                            heappush(pq[1-pqi], pq[pqi][0])
                            heappop(pq[pqi])
                        pqi = 1 - pqi
                        heappush(pq[pqi], m0)  # add the better node instead
        return ''  # if no route found


class _node:
    xPos = 0  # x position
    yPos = 0  # y position
    distance = 0  # total distance already travelled to reach the node
    priority = 0  # priority = distance + remaining distance estimate

    def __init__(self, xPos, yPos, distance, priority):
        self.xPos = xPos
        self.yPos = yPos
        self.distance = distance
        self.priority = priority

    def __lt__(self, other):  # comparison method for priority queue
        return self.priority < other.priority

    def updatePriority(self, xDest, yDest):
        self.priority = self.distance + self.estimate(xDest, yDest) * 10  # A*

    # give higher priority to going straight instead of diagonally
    def nextMove(self, dirs, d):  # d: direction to move
        if dirs == 8 and d % 2 != 0:
            self.distance += 14
        else:
            self.distance += 10

    # Estimation function for the remaining distance to the goal.
    def estimate(self, xDest, yDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        # Euclidian Distance
        # d = math.sqrt(xd * xd + yd * yd)
        # Manhattan distance
        d = abs(xd) + abs(yd)
        # Chebyshev distance
        # d = max(abs(xd), abs(yd))
        return(d)
