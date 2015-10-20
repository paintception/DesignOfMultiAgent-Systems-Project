#!/usr/bin/env python

from os import path

RESULTS_BASE_DIR = 'results'
RESULTS_FILE_NAME = path.join(RESULTS_BASE_DIR, 'results.json')
PARAMS_OUT_FILE_NAME = path.join(RESULTS_BASE_DIR, 'parameters.json')


def signal_handler(signal, frame):
    import sys
    print('** Byebye.')
    sys.exit(1)  # exit with non-0 so script runner can recognize C-c


def store_results(key, data):
    from os import path
    import json

    prev_data = {}
    if path.isfile(RESULTS_FILE_NAME):
        with open(RESULTS_FILE_NAME, 'r') as f:
            prev_data = json.loads(f.read())

    prev_data[key] = data
    with open(RESULTS_FILE_NAME, 'w') as f:
        json.dump(prev_data, f, indent=2)


def main(args):
    import signal
    import sys
    from time import sleep
    from Simulation import Simulation, SimulationParameters

    signal.signal(signal.SIGINT, signal_handler)

    if args.parameter_file:
        print("** Loading parameters from '%s'" % args.parameter_file)
        sim_params = SimulationParameters.load(args.parameter_file)
    else:
        print("** Creating parameters with random routes")
        sim_params = SimulationParameters()
        sim_params.grid_width = args.grid_size
        sim_params.grid_height = args.grid_size
        sim_params.n_agents = args.n_agents
        sim_params.steps_per_day = args.steps_per_day
        sim_params.max_days = args.max_days

    sim_params.memory_enabled = args.with_memory  # never load this value from file

    simulation = Simulation(sim_params)

    print("** Storing parameters in '%s'" % PARAMS_OUT_FILE_NAME)
    simulation.get_parameters().save(PARAMS_OUT_FILE_NAME)

    # run simulation - would be nice if we could optionally wait for space between steps
    step_delay = 1.0 / args.fps
    while True:
        simulation_running = simulation.do_step()
        if not simulation_running:
            print("** Simulation finished")

            results_key = "sim_%i%s" % (args.sim_id, "T" if sim_params.memory_enabled else "F")
            store_results(results_key, simulation.get_jam_progression())
            sys.exit(0)

        if args.fps > 0:
            sleep(step_delay)


def get_args():
    import argparse

    parser = argparse.ArgumentParser(description='Run traffic simulation', add_help=True, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-g', '--grid-size', type=int, help="Grid size determines the number of junctions in each dimension", default=45)
    parser.add_argument('-a', '--n-agents', type=int, help="Number of agents", default=100)
    parser.add_argument('-s', '--steps-per-day', type=int, help="Number of time steps per day (default one for each minute)", default=24*60)
    parser.add_argument('-m', '--max-days', type=int, help="Maximum number of days to let pass in the simulation (-1 to disable)", default=-1)
    parser.add_argument('-f', '--fps', type=int, help="Maximum time steps per second (-1 to disable)", default=-1)
    parser.add_argument('-p', '--parameter-file', type=str, help="JSON file to load parameters from", default=None)
    parser.add_argument('-w', '--with-memory', action='store_true', help="Enable memory", default=False)
    parser.add_argument('-i', '--sim-id',type=int, help="Simulation ID", default=None)

    args = parser.parse_args()

    return(args)

if __name__ == '__main__':
    args = get_args()
    main(args)
