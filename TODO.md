# current
- add simple event system
- change max cars per junction+street and MAX_ROAD_PUSHES and MAX_MOVES to use simulation parameters
- if n_route_endpoints makes sense, move it to sim parameters (currently in Simulation._setup())
- implement Simulation._get_random_points() properly (or decide
# implementation

- test avoid list in Grid.get_path()
- replace direction map in astar.py with the one from Utils.py?


# larger picture

- combine junctions with Krauss model as described in paper
  maybe: <http://eprints.whiterose.ac.uk/2149/1/ITS159_WP431_uploadable.pdf>
- with 60*24=1440 timesteps per day and 1 agent, each day takes ~.6s to compute (update: with the larger grid that's 18s)
  so, either make A* simpler (less routing choices) or lower number of timesteps or find a different algorithm
  NOTE 1: using a direct ref to self._astar_grid takes >3 times as long
  NOTE 2: creating local ref but not copying is twice as fast
