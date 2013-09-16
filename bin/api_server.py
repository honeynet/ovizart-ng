#!/usr/bin/env python
__author__ = 'ggercek'

import sys
sys.path.append('../')

import argparse
from core.daemon import Daemon


class APIServer(Daemon):

    def __init__(self, pid, host='localhost', port=9009, isSSL=True):
        Daemon.__init__(self, pid)

        self.host = host
        self.port = port
        self.isSSL = isSSL
        self.restServer = None

    def run(self):
        from core.webserver import OvizartRestServer
        import ovizapi  # Need to import to execute the decorators
        self.restServer = OvizartRestServer(self.host, self.port, self.isSSL)
        self.restServer.start()
        self.restServer.waitForThread()


def main(args):
    def portNumber(_val):
        try:
            value = int(_val)
        except:
            raise argparse.ArgumentTypeError('Value must be an integer')
        print 'value:', value
        if value > 65535 or value < 1:
            raise argparse.ArgumentTypeError('Value has to be between 1 and 65535')
        return value

    parser = argparse.ArgumentParser(prog='api_server daemon script')
    parser.add_argument('action', choices=['start', 'stop', 'restart'])
    parser.add_argument('--host', dest='host', default='localhost')
    parser.add_argument('--port', dest='port', type=portNumber, default=9009)
    parser.add_argument('--ssl', dest='isSSL', action="store_true")

    args = parser.parse_args(args)

    daemon = APIServer('/tmp/ovizart_api.pid', host=args.host, port=args.port, isSSL=args.isSSL)

    if 'start' == args.action:
        daemon.start()
    elif 'stop' == args.action:
        daemon.stop()
    elif 'restart' == args.action:
        daemon.restart()

if __name__ == "__main__":
    main(sys.argv[1:])
