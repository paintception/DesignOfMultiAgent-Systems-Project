#!/usr/bin/env python


def signal_handler(signal, frame):
    import sys
    print('** Byebye.')
    sys.exit(0)


def main(args):
    import signal
    import sys
    from time import sleep
    from Simulation import Simulation, SimulationParameters

    signal.signal(signal.SIGINT, signal_handler)

    sim_params = SimulationParameters()
    sim_params.grid_width = args.grid_size
    sim_params.grid_height = args.grid_size
    sim_params.n_agents = args.n_agents
    sim_params.steps_per_day = args.steps_per_day
    sim_params.max_days = args.max_days

    simulation = Simulation(sim_params)

    # run simulation - would be nice if we could optionally wait for space between steps
    step_delay = 1.0 / args.fps
    while True:
        simulation_running = simulation.do_step()
        if not simulation_running:
            print("** Simulation finished")
            sys.exit()

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

    args = parser.parse_args()

    return(args)

if __name__ == '__main__':
    args = get_args()
    main(args)
