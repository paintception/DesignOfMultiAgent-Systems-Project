from __future__ import print_function, division
import Grid as Grid
class Simulation():
    def __init__(self, world):
        self._world = world

    def run(self):
        from datetime import datetime as dt

        w, g = self._world, self._world.get_grid()
        day_count = 0

        start = dt.now()
        while True:
            cars = w.get_agents()

            for car in cars:
                if not car.is_travelling():
                    # TEMP: randomly route cars
                    # TODO: check if no car is at (sx,sy) yet (and if so: wait? or pick another point?)
                    car.set_start_point(g.get_random_position())
                    car.set_end_point(g.get_random_position())
                    car.reset_pos()

            w.update_grid()

            if self._world.get_time() == 0:
                duration = dt.now() - start
                print("===== Day: %i (%.2f secs) =====" %
                    (day_count, duration.seconds + (duration.microseconds / 1000000)))
                print(self._world.get_grid())
                start = dt.now()
                day_count += 1

            w.next_time_step()
