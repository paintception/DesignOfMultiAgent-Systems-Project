from Singleton import Singleton


@Singleton
class TimeLord():
    # avoid ctor parameters since this is a singleton
    def __init__(self):
        self._time_step = 0
        self._day = 0
        self._timesteps_per_day = 0

    def setup(self, timesteps_per_day):
        self._timesteps_per_day = timesteps_per_day

    def next_time_step(self):
        self._time_step = (self._time_step + 1) % self._timesteps_per_day
        print ("** Timestep: %s" % self._time_step)
        if self._time_step == 0:
            self._day += 1

    def get_day_time(self):
        return self._time_step

    def get_day(self):
        return self._day

    def get_timestamp(self):
        return self._day * self._timesteps_per_day + self._time_step
