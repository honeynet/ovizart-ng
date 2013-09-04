__author__ = 'ggercek'

import json
import requests


class OvizartProxy():

    LOGIN_URL = 'login'
    UPLOAD_URL = 'upload'

    def __init__(self, protocol, host, port=80):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.login_success = False
        self.cookies = None

    def login(self, username, password):
        url = self.__generateLink(OvizartProxy.LOGIN_URL)
        response = requests.post(url, verify=False, headers={'content-type': 'application/json'},
                                 data=json.dumps({'username': username, 'password': password}))

        # Check for login success?
        result = json.loads(response.content)
        if result['Status'] == 'OK':
            self.login_success = True
            self.cookies = response.cookies

        return result

    def uploadFile(self, filename):
        import os
        filepath = os.path.abspath(filename)
        filename = os.path.basename(filepath)
        url = self.__generateLink(OvizartProxy.UPLOAD_URL) + '/' + filename
        result = "NA"
        with open(filepath, 'r') as f:
            #response = requests.post(url, verify=False, files={'file': (filename, f)}, cookies=self.cookies)
            response = requests.post(url, verify=False, data=f, headers={'content-type': 'application/octet-stream'}, cookies=self.cookies)
            result = json.loads(response.content)


        # TODO: Consider using stream options for large files!!!
        # For streaming use following;
        # with open('massive-body') as f:
        #     requests.post('http://some.url/streamed', data=f)
        # TODO: Based on file size choose upload option!!!! Webserver have stream support now!
        #with open('/home/hforge/Downloads/target_based_frag.pdf', 'r') as f:
        #    requests.post('http://localhost:8000', data=f)
        return result

    def __generateLink(self, url):
        return "%s://%s:%s/%s"%(self.protocol, self.host, self.port, url)
