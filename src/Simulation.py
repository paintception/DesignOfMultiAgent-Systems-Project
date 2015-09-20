from __future__ import print_function, division


class Simulation():
    def __init__(self, world):
        self._world = world

    def run(self):
        from datetime import datetime as dt

        w = self._world
        day_count = 0

        start = dt.now()
        while True:
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

            if self._world.get_time() == 0:
                duration = dt.now() - start
                print("===== Day: %i (%.2f msecs) =====" %
                    (day_count, duration.seconds + (duration.microseconds / 1000000)))
                print(self._world.get_grid())
                start = dt.now()
                day_count += 1

            w.next_time_step()
