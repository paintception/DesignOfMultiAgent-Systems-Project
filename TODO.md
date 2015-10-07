# current
- also create event somehow to notify cars that street/junction movement capacity is reached (so 6 events in total)
- if n_route_endpoints makes sense, move it to sim parameters (currently in Simulation._setup())
# implementation

- test avoid list in Grid.get_path()
- replace direction map in astar.py with the one from Utils.py?


# larger picture

- with 60*24=1440 timesteps per day and 1 agent, each day takes ~.6s to compute (update: with the larger grid that's 18s)
  so, either make A* simpler (less routing choices) or lower number of timesteps or find a different algorithm
  NOTE 1: using a direct ref to self._astar_grid takes >3 times as long
  NOTE 2: creating local ref but not copying is twice as fast
