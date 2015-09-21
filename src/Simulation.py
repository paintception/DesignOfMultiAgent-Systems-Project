from __future__ import print_function

class Simulation():
    def __init__(self, world):
        self._world = world

    def run(self):
        w = self._world
        day_count = -1

        while True:
            if self._world.get_time() == 0:
                day_count += 1
                print("===== Day: %i =====" % day_count)
                print(self._world.get_grid())
             
            cars = w.get_agents()

            gw, gh = w.get_grid().width, w.get_grid().height
            for car in cars:
                if not car.is_travelling():
                    # TEMP: randomly route cars
                    from utils import Point
                    from random import randint
                    # TODO: check if no car is at (sx,sy) yet (and if so: wait? or pick another point?)
                    sx, sy = randint(0, gw - 1), randint(0, gh - 1)
                    ex, ey = randint(0, gw - 1), randint(0, gh - 1)

                    car.set_start_point(Point(sx, sy))
                    car.set_end_point(Point(ex, ey))
                    car.reset_pos()

            for car in cars:
                car.update()

            w.next_time_step()
