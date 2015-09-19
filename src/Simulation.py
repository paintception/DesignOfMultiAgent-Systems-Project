from __future__ import print_function


class Simulation():
    def __init__(self, world):
        self._world = world

    def run(self):
        w = self._world

        while True:
            print("Time: %s" % self._world.get_time())

            cars = w.get_agents()

            gw, gh = w.get_grid().width, w.get_grid().height
            for car in cars:
                if not car.is_travelling():
                    # TEMP: randomly route cars
                    from Utils import Point
                    from random import randint
                    # TODO: check if no car is at (sx,sy) yet
                    sx, sy = randint(0, gw), randint(0, gh)
                    ex, ey = randint(0, gw), randint(0, gh)
                    
                    car.set_start_point(Point(sx, sy))
                    car.set_end_point(Point(ex, ey))
                    car.reset_pos()

            for car in cars:
                print(car)
                car.update()
                #TODO: update grid with new car position

            w.next_time_step()
