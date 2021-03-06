#!/usr/bin/env python

"""
- mostly from: https://www.junian.net/2014/07/simple-http-server-and-client-in-python.html
- simple example: https://github.com/mathisonian/simple-testing-server/blob/master/simple-testing-server.py
- threaded example: https://mafayyaz.wordpress.com/2013/02/08/writing-simple-http-server-in-python-with-rest-and-json/
"""
from __future__ import print_function
from os import path
import json
from urlparse import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from Simulation import Simulation, SimulationParameters
from TimeLord import TimeLord
from World import World

simulation, t, w = None, None, None
verbose_mode = False

class HTTPRequestHandler(BaseHTTPRequestHandler):
    global simulation

    mime_types = {
        'js': 'application/javascript',
        'html': 'text/html',
        'css': 'text/css'
    }

    base_path = 'www'
    api_prefix = '/sim'
    index_file = 'index.html'


    def do_GET(self):
        if self.path.startswith(self.api_prefix):
            self._handle_api_request()
        else:
            self._handle_file_request()

    def do_POST(self):
        if self.path.startswith(self.api_prefix):
            self._handle_api_request()
        else:
            self.send_error(404, 'POST requests only supported for API calls')

    def log_message(self, format, *args):
        if verbose_mode: print("msg", format % args)

    def _handle_file_request(self):
        try:
            rq_path = urlparse(self.path).path  # get just the path, not the query/fragment_id etc.
            if rq_path[0] == '/': rq_path = rq_path[1:]
            if len(rq_path) == 0: rq_path = self.index_file
            filename = path.join(self.base_path, rq_path)

            if verbose_mode: print("** Attempting to open %s" % filename)
            f = open(filename, 'r')

            extension = path.splitext(rq_path)[1][1:]
            # mime_type = mime_types.get(extension, 'application/octet-stream')
            mime_type = self.mime_types.get(extension, 'unknown/unknown')

            self._send_ok_headers(mime_type)

            self.wfile.write(f.read())
            f.close()
        except IOError:
            self.send_error(404, 'file not found')

    def _handle_api_request(self):
        rq_path = urlparse(self.path).path  # get just the path, not the query/fragment_id etc.
        rq_path = rq_path[(len(self.api_prefix)+1):]  # strip api prefix + '/'
        if verbose_mode: print("API endpoint requested:", rq_path)

        func_name = '_api_' + rq_path

        if self.command == 'POST':
            func_name += '_POST'

        try:
            func = getattr(self, func_name)
        except AttributeError:
            func = None

        if func:  # and type(func) == 'instancemethod':
            self._send_ok_headers('application/json')

            response_text = func()
            self.wfile.write(response_text)
        else:
            self.send_error(404, 'no such API endpoint')

    def _send_ok_headers(self, mime_type):
        self.send_response(200)
        self.send_header('Content-type', mime_type)
        self.send_header('Content-Language', 'en')
        self.end_headers()


    #################
    # API FUNCTIONS #
    #################
    # functions without any suffix are invoked for GET, others have respective method as suffix (e.g. _api_func_POST)

    def _api_test(self):
        test_data = [{'key1-str': 'xyzzy', 'key2-int': 42}, 'elem3', 4]
        return json.dumps(test_data)

    def _api_step(self):
        running = simulation.do_step()
        return json.dumps({
            'ts': t.get_timestamp(),
            'step': t.get_day_time(),
            'day': t.get_day(),
            'finished': not running
        })

    def _api_grid(self):
        g = w.get_grid()
        gdata = []

        for y in xrange(g.height):
            row = []
            for x in xrange(g.width):
                row.append(g.get_item_at(x, y).jsonifiable())
            gdata.append(row)

        return json.dumps({ 'width': g.width, 'height': g.height, 'grid': gdata })

    def _api_parameters(self):
        return json.dumps(w.get_parameters().jsonifiable());

    def _api_number_of_jams(self):
        from World import World
        return json.dumps(World().get_counter())

    def _api_agents(self):
        from World import World
        data = [a.jsonifiable() for a in World().get_agents()]
        return json.dumps(data)

    # start new simulation with given parameters, if any
    def _api_new_POST(self):
        length = int(self.headers.getheader('Content-Length'))
        data = self.rfile.read(length)

        try:
            p = SimulationParameters.loads(data)
            simulation = Simulation(p)  # creating a new simulation resets everything
            return json.dumps({'status': 'ok'})
        except ValueError, e:
            print("error processing json POST data '%s' (len=%i): %s" % (data, length, e) )
            return json.dumps({'status': 'err', 'msg': 'could not parse input'})

    def _api_restart_POST(self):
        length = int(self.headers.getheader('content-length'))
        data = self.rfile.read(length)

        try:
            data = json.loads(data) if length > 0 else {}
            simulation.restart(data.get('randomize_routes', False))
            return json.dumps({'status': 'ok'})
        except ValueError, e:
            print("error processing json POST data '%s' (len=%i): %s" % (data, length, e) )
            return json.dumps({'status': 'err', 'msg': 'could not parse input'})


def main(args):
    import signal
    global simulation, t, w
    global verbose_mode
    verbose_mode = args.verbose

    signal.signal(signal.SIGINT, signal_handler)

    simulation = Simulation(SimulationParameters())
    t, w = TimeLord(), World()  # globals for request handler

    httpd = HTTPServer((args.host, args.port), HTTPRequestHandler)
    print('** starting http server on port %s:%i...' % (args.host, args.port))
    httpd.serve_forever()


def signal_handler(signal, frame):
    import sys
    print('** Byebye.')
    sys.exit(0)


def get_args():
    import argparse

    parser = argparse.ArgumentParser(description='Run traffic simulation webserver/', add_help=True, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--host', type=str, help="Server host/interface to listen on", default='0.0.0.0')
    parser.add_argument('-p', '--port', type=int, help="Server port to listen on", default=8001)
    parser.add_argument('-v', '--verbose', action='store_true', help="Log HTTP requests")

    args = parser.parse_args()

    return(args)

if __name__ == '__main__':
    args = get_args()
    main(args)
