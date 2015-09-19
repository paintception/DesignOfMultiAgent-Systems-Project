#!/usr/bin/env python

from World import World


def main(args):
    world = World(args.grid_size, args.num_agents)


def get_args():
    import argparse

    parser = argparse.ArgumentParser(description='Run traffic simulation', add_help=True)

    parser.add_argument('-g', '--grid-size', type=int, help="Grid size", default=18)
    parser.add_argument('-a', '--num-agents', type=int, help="Number of agents", default=100)

    args = parser.parse_args()

    return(args)

if __name__ == '__main__':
    args = get_args()
    main(args)
