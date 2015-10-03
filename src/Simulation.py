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
                print (car)
                if not car.is_travelling():
                    # TEMP: randomly route cars

                    check = 0
                    while not check:
                        car.set_start_point(g.get_random_position())
                        car.set_end_point(g.get_random_position())
                        car.reset_pos()
                        print (check)
                        check = self.add_car(car)

            w.update_grid()

            if self._world.get_time() == 0:
                duration = dt.now() - start
                print("===== Day: %i (%.2f secs) =====" %
                    (day_count, duration.seconds + (duration.microseconds / 1000000)))
                #printing grid
                #self.print_grid(self._world.print_grid())
                start = dt.now()
                day_count += 1

            w.next_time_step()

    def add_car(self, car):
        if self._world.get_grid().add_car(car):
            return 1
        return 0

    def print_grid(self, printing_grid):
        self._printing_grid=printing_grid
        print (self._printing_grid)