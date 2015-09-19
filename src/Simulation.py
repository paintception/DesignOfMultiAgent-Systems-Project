from __future__ import print_function


class Simulation():
    def __init__(self, world):
        self._world = world

    def run(self):
        while True:
            print("Time: %s" % self._world.get_time())

            cars = self._world.get_agents()

            for car in cars:
                if not car.is_travelling():
                    pass
                    # generate start + end points
                    # set both on car
                    # teleport car to start point, but only if no car is there yet

            for car in cars:
                car.update()

            self._world.next_time_step()
