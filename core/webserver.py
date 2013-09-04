__author__ = 'ggercek'


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import urlparse
import json
import ssl
from gencert import createCert
import Cookie
import string
import random
import time


class CookieEntry():
    def __init__(self, ipAddress, value):
        self.isExpired = False
        self.isAuth = False
        self.lastVisit = time.time()
        self.ipAddress = ipAddress
        self.value = value
        self.data = {}

    def visited(self):
        self.lastVisit = time.time()

    def isValid(self, ipAddress, value):
        # TODO: check also timeout
        return (self.ipAddress == ipAddress and self.value == value)

    def __repr__(self):
        return "isExpired: %s, isAuth: %s, lastVisit: %s, ipAddress: %s, value: %s, data: %s"% \
            (self.isExpired, self.isAuth, self.lastVisit, self.ipAddress, self.value, self.data)


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.__do('POST')

    def do_GET(self):
        self.__do('GET')

    def do_PUT(self):
        self.__do('PUT')

    def do_DELETE(self):
        self.__do('DELETE')

    def __process_cookie(self):
        cookie = None
        clientIpAddress = self.client_address[0]
        print 'headers: ', self.headers
        if 'Cookie' in self.headers:
            c = Cookie.SimpleCookie(self.headers["Cookie"])
            val = c['value'].value
            print 'val:', val
            if val in self.server.cookies:
                cookie = self.server.cookies[val]
                if cookie.isValid(clientIpAddress, val):
                    cookie.visited()
                else:
                    del c['value']
                    del cookie
                    cookie = None
                    self.send_headers("Set-Cookie", "access_token=deleted; Expires=Thu, 01-Jan-1970 00:00:00 GMT")
        else:
            # New user arrivied!!!!
            cookie = Cookie.SimpleCookie()
            val = ''.join(random.choice(string.ascii_letters+string.digits) for x in xrange(200))
            cookie['value'] = val
            self.send_header('Set-Cookie', cookie.output(header=''))
            #self.end_headers()
            cookie = CookieEntry(clientIpAddress, val)
            self.server.cookies[val] = cookie

        return cookie

    def __do(self, httpMethod):
        #print '%s method to URL: %s' % (httpMethod, self.path)
        api = API.getMethod(httpMethod, self.path)
        #print 'api:', api
        if api:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')

            cookie = self.__process_cookie()
            print 'Cookie:', cookie

            self.end_headers()
            if cookie is None:
                return

            f, data = api

            #print '##', httpMethod, ',', data, '##'
            if httpMethod != 'GET':
                data = self.__parseData()
                data['cookie'] = cookie

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
        remainbytes = int(self.headers['content-length'])

        if ctype == 'application/json':
            length = int(self.headers['content-length'])
            content = self.rfile.read(length)
            postvars = json.loads(content)
        elif ctype == 'multipart/form-data':
            # Handle upload
            result, data = self.__processUpload()
            if result:
                postvars['filename'] = data

        return postvars

    def __processUpload(self):
        import os
        import datetime

        boundary = None
        try:
            boundary = self.headers.plisttext.split("=")[1]
        except IndexError:

            # STREAM upload handling
            print 'No Boundry trying to read stream'
            remainbytes = int(self.headers['content-length'])
            path = self.translate_path(self.path)

            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            fn = os.path.join(path, 'uploadedFile_%s'%timestamp)
            out = open(fn, 'wb')
            print 'fn:', fn
            rlen = 4096
            while remainbytes > 0:
                if rlen > remainbytes:
                    rlen = remainbytes
                chunk = self.rfile.read(rlen)
                remainbytes -= len(chunk)
                out.write(chunk)
                out.flush()
            out.close()
            print "Done!!!"
            return True, fn

        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return False, None  #"Content NOT begin with boundary"
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line)
        if not fn:
            return False, None  #"Can't find out file name..."
        path = self.translate_path(self.path)
        fn = os.path.join(path, fn[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return False, None  #"Can't create file to write, do you have permission to write?")
        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith('\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return True, fn  #"File '%s' upload success!" % fn
            else:
                out.write(preline)
                preline = line
        return False, None  #"Unexpected end of data."

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

    def __init__(self, server_info, handler):
        self.cookies = {}
        HTTPServer.__init__(self, server_info, handler)
        certFile = createCert()
        self.socket = ssl.wrap_socket(self.socket, certfile=certFile, server_side=True)

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
    import sys
    sys.path.append('../')
    server = OvizartRestServer('localhost', 9009)
    print 'HTTP Server Running...........'
    server.start()
    import os
    print 'pid:', os.getpid()

    server.waitForThread()