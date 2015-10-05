from __future__ import print_function, division
from datetime import datetime as dt


class Simulation():
    def __init__(self, world):
        self._world = world
        self._day_count = 0

    def do_step(self):
        w, g = self._world, self._world.get_grid()
        cars = w.get_agents()
        start = dt.now()

        for car in cars:
            if not car.is_travelling():
                check = False
                while not check:
                    car.set_start_point(g.get_random_position())
                    car.set_end_point(g.get_random_position())
                    car.reset_pos()
                    check = self.add_car(car)
                    if check: print("new route set for: %s" % car)

        w.update_grid()

        if self._world.get_time() == 0:
            duration = dt.now() - start
            print("===== Day: %i (%.2f secs) =====" %
                  (self._day_count, duration.seconds + (duration.microseconds / 1000000)))
            #printing grid
            #self.print_grid(self._world.print_grid())
            start = dt.now()
            self._day_count += 1

        w.next_time_step()

    def run(self):
        while True:
            self.do_step()

    def add_car(self, car):
        return self._world.get_grid().add_car(car)

    def print_grid(self, printing_grid):
        self._printing_grid = printing_grid
        #print (self._printing_grid)

    def Json_data(self, data_we_want_to_plot): 
        
        from django.utils import simplejson                                         

        json_data_we_want_to_plot = json.dumps(data_we_want_to_plot)
        render_template("_our_HTML_", {"_our_data", our_js_data})

        "Here we create JSON data. Into the js script file we need to add: type=""text/javascript"">"
        "data_from_django = {{ :_our_data }};"
        "widget.init(data_from_django);"

