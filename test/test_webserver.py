from unittest import TestCase

import httplib2
import json
from core.webserver import API, OvizartRestServer

WS_PORT = 9009
WS_HOST = 'localhost'
TEST_URL = 'http://%s:%d/test/' % (WS_HOST, WS_PORT)

class TestWebServer(TestCase):

    @classmethod
    def setUpClass(cls):
        global WS_HOST, WS_PORT
        ## Set up dummy test methods ##

        @API(method='GET', url='^/test/$')
        def processGET0(data):
            return '{"method":"GET", "data": %s}' % json.dumps(data)

        @API(method='GET', url='^/test/(?P<name>\w+)/(?P<surname>\w+)/?$')
        def processGETNameSurname(data):
            return '{"method":"GET", "data": %s}' % json.dumps(data)

        @API(method='POST', url=r"^/test/$")
        def processPOST(data):
            return '{"method":"POST", "data": %s}' % json.dumps(data)

        @API(method='PUT', url=r"^/test/$")
        def processPUT(data):
            return '{"method":"PUT", "data": %s}' % json.dumps(data)

        @API(method='DELETE', url=r"^/test/$")
        def processDELETE(data):
            return '{"method":"DELETE", "data": %s}' % json.dumps(data)

        ## Start the server
        cls.webServer = OvizartRestServer(WS_HOST, WS_PORT)
        cls.webServer.start()

    @classmethod
    def tearDownClass(cls):
        cls.webServer.stop()

    def test_GET_method(self):
        requestData = {'name': 'Bill', 'surname': 'Cosby'}
        url = '%s%s/%s' % (TEST_URL, requestData['name'], requestData['surname'])
        responseData = self.__requestTestURL('GET', json.dumps(requestData), url)
        assert responseData['data'] == requestData

    def test_GET_method_no_argument(self):
        requestData = {'name': 'Bill', 'surname': 'Cosby'}
        responseData = self.__requestTestURL('GET', json.dumps(requestData))
        assert not responseData['data']

    def test_POST_method(self):
        requestData = {'name': 'Bill', 'surname': 'Cosby'}
        responseData = self.__requestTestURL('POST', json.dumps(requestData))
        assert requestData == responseData['data']

    def test_DELETE_method(self):
        requestData = {'name': 'Bill', 'surname': 'Cosby'}
        responseData = self.__requestTestURL('DELETE', json.dumps(requestData))
        assert requestData == responseData['data']

    def test_PUT_method(self):
        requestData = {'name': 'Bill', 'surname': 'Cosby'}
        responseData = self.__requestTestURL('PUT', json.dumps(requestData))
        assert requestData == responseData['data']

    def __requestTestURL(self, method, data, url=TEST_URL):
        h = httplib2.Http()
        a = h.request(method=method,
                uri=url,
                headers={'content-type': 'application/json'},
                body=data)

        responseData = json.loads(a[1])
        return responseData