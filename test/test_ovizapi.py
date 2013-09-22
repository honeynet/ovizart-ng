__author__ = 'ggercek'

import ovizapi

import json
import requests
import unittest
from core.webserver import OvizartRestServer

HOST = 'localhost'
PORT = 9009
PROTOCOL = 'https'

class TestOvizAPI(unittest.TestCase):

    def test_basic_login(self):
        global HOST, PORT

        server = OvizartRestServer(HOST, PORT, True)
        server.start()
        response = requests.post('%s://%s:%d/login' % (PROTOCOL, HOST, PORT), verify=False,
                                 data=json.dumps({'username': 'admin', 'password': 'admin'}),
                                 headers={'content-type': 'application/json'})

        server.stop()
        assert json.loads(response.content)['Status'] == 'OK'

    def test_authentication(self):
        global HOST, PORT

        server = OvizartRestServer(HOST, PORT, True)
        server.start()
        response = requests.post('%s://%s:%d/login' % (PROTOCOL, HOST, PORT), verify=False,
                                 data=json.dumps({'username': 'admin', 'password': 'admin'}),
                                 headers={'content-type': 'application/json'})

        cookies = response.cookies
        response1 = requests.get('%s://%s:%d/name/surname' % (PROTOCOL, HOST, PORT), verify=False, headers={
            'content-type': 'application/json'}, cookies=cookies)

        assert response1.content == "Hello name surname"

        server.stop()

    def test_fileupload(self):
        global HOST, PORT

        server = OvizartRestServer(HOST, PORT, True)
        server.start()
        response = requests.post('%s://%s:%d/login' % (PROTOCOL, HOST, PORT), verify=False,
                                 data=json.dumps({'username': 'admin', 'password': 'admin'}),
                                 headers={'content-type': 'application/json'})

        cookies = response.cookies

        import os
        from ovizconf import PROJECT_ROOT
        filepath = os.path.join(PROJECT_ROOT, 'test/pcap/smtp.pcap')
        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)
        with open(filepath, 'r') as f:
            response1 = requests.post('%s://%s:%d/upload/%s' % (PROTOCOL, HOST, PORT, filename), verify=False, headers={
                'content-type': 'application/octet-stream'}, cookies=cookies, data=f)
        resp = json.loads(response1.content)
        print resp
        assert resp['Filesize'] == filesize
        server.stop()
