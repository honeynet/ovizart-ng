__author__ = 'ggercek'


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import urlparse
import json


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.__do('POST')

    def do_GET(self):
        self.__do('GET')

    def do_PUT(self):
        self.__do('PUT')

    def do_DELETE(self):
        self.__do('DELETE')

    def __do(self, httpMethod):
        #print '%s method to URL: %s' % (httpMethod, self.path)
        api = API.getMethod(httpMethod, self.path)
        #print 'api:', api
        if api:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            f, data = api

            #print '##', httpMethod, ',', data, '##'
            if httpMethod != 'GET':
                data = self.__parseData()
            #print '>>', httpMethod, ',', data, '##'
            result = f(data)
            self.wfile.write(result)
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return

    def __parseData(self):
        import cgi
        postvars = {}
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'application/json':
            length = int(self.headers['content-length'])
            content = self.rfile.read(length)
            postvars = json.loads(content)

        # TODO: Add file upload support
        # A sample: https://gist.github.com/UniIsland/3346170
        return postvars


class API():
    api_methods = {
        'GET':  {},
        'POST': {},
        'PUT':  {},
        'DELETE':{}
    }

    def __init__(self, method='GET', url='/test/00/'):
        self.method = method
        self.url = url
        print 'API decorator:', 'method:', method, 'url:', url

    def __call__(self, func):
        print 'Register method'
        method = self.method
        url = self.url
        api_methods = API.api_methods

        if method in api_methods.keys():
            if url in api_methods[method].keys():
                raise Exception('URL is already registered: %s for method: %s' % (url, method))
            else:
                api_methods[method][url] = func
        else:
            raise Exception('No such registered HTTP method: %s for given url: %s' % (method, url))

        return func

    @staticmethod
    def getMethod(requestType, path):
        if API.api_methods[requestType]:
            for val in API.api_methods[requestType].iterkeys():
                m = re.search(val, path)
                if None != m:
                    data = m.groupdict()
                    return API.api_methods[requestType][val], data

        return None


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)


class OvizartRestServer():
    def __init__(self, ip, port):
        self.server = ThreadedHTTPServer((ip, port), HTTPRequestHandler)

    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def waitForThread(self):
        self.server_thread.join()

    def stop(self):
        self.server.shutdown()
        self.waitForThread()


# A sample rest method
@API(method='GET', url=r"^/(?P<first_name>\w+)/(?P<last_name>\w+)/?$")
def processGET(data):
    name = data['first_name']
    surname = data['last_name']

    return "Hello %s %s" % (name, surname)


if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='HTTP Server')
    #parser.add_argument('port', type=int, help='Listening port for HTTP Server')
    #parser.add_argument('ip', help='HTTP Server IP')
    #args = parser.parse_args()

    #server = SimpleHttpServer(args.ip, args.port)
    server = OvizartRestServer('localhost', 9009)
    print 'HTTP Server Running...........'
    server.start()
    server.waitForThread()