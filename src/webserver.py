#!/usr/bin/env python

"""
- mostly from: https://www.junian.net/2014/07/simple-http-server-and-client-in-python.html
- simple example: https://github.com/mathisonian/simple-testing-server/blob/master/simple-testing-server.py
- threaded example: https://mafayyaz.wordpress.com/2013/02/08/writing-simple-http-server-in-python-with-rest-and-json/
"""
from __future__ import print_function
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import path


class HTTPRequestHandler(BaseHTTPRequestHandler):
    mime_types = {
        'js': 'application/javascript',
        'html': 'text/html',
        'css': 'text/css'
    }

    base_path = 'www'

    def do_GET(self):
        try:
            rq_path = self.path
            if rq_path[0] == '/': rq_path = rq_path[1:]
            filename = path.join(self.base_path, rq_path)

            print("** Attempting to open %s" % filename)
            f = open(filename, 'r')

            extension = path.splitext(self.path)[1][1:]
            # mime_type = mime_types.get(extension, 'application/octet-stream')
            mime_type = self.mime_types.get(extension, 'unknown/unknown')

            self.send_response(200)
            self.send_header("Content-type", mime_type)
            self.end_headers()

            self.wfile.write(f.read())
            f.close()
        except IOError:
            self.send_error(404, 'file not found')

    # def do_POST(self):
    #     pass


def main(args):
    import signal
    # from time import sleep
    # from Simulation import Simulation, SimulationParameters

    signal.signal(signal.SIGINT, signal_handler)

    httpd = HTTPServer(('localhost', args.port), HTTPRequestHandler)
    print('starting http server on port %i...' % args.port)
    httpd.serve_forever()

    # sim_params = SimulationParameters()
    # sim_params.grid_width = args.grid_size
    # sim_params.grid_height = args.grid_size
    # sim_params.n_agents = args.n_agents
    # sim_params.steps_per_day = args.steps_per_day

    # simulation = Simulation(sim_params)

    # # run simulation - would be nice if we could optionally wait for space between steps
    # step_delay = 1.0 / args.fps
    # while True:
    #     simulation.do_step()
    #     if args.fps > 0:
    #         sleep(step_delay)


def signal_handler(signal, frame):
    import sys
    print('** Byebye.')
    sys.exit(0)


def get_args():
    import argparse

    parser = argparse.ArgumentParser(description='Run traffic simulation webserver/', add_help=True, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-p', '--port', type=int, help="Server port to listen on", default=8001)

    args = parser.parse_args()

    return(args)

if __name__ == '__main__':
    args = get_args()
    main(args)
