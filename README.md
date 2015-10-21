# Multi-agent traffic simulation.

The simulation can be run in three different ways:
- A single simulation can be run with `main.py`. Run it with `-h` for a list of options.
- A web interface becomes available after running `webserver.py`. It is accessible at port 8001, usually: <http://localhost:8001>.
  This shows a visualization of the grid as well as a sortable table of the agents while travelling.
- The following two steps will render a plot of repeated simulations:
  - First data must be collected by running `collect-results.sh` (no Windows variant provided yet, the script is very simple though).
    This calls `main.py` with incrementing simulation IDs which are then used to save jam progression into a file 'results.json'.
    The shell script also defines how many simulation repetitions are performed.
  - Then run `draw-plots.py` to average over the result data and draw a plot.

Some of the model parameters cannot be set externally and can only be changed in the `SimulationParameters` class in `Simulation.py`.
