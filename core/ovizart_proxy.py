__author__ = 'ggercek'

import json
import requests


class OvizartProxy():

    LOGIN_URL = 'login'
    UPLOAD_URL = 'upload'
    START_URL = 'start'
    LIST_ANALYSIS = 'analysis'

    def __init__(self, protocol='https', host='localhost', port=9009):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.login_success = False
        self.cookies = None
        self.userid = None
        self.username = None
        self.password = None

    def __generateLink(self, url):
        return "%s://%s:%s/%s"%(self.protocol, self.host, self.port, url)

    def login(self, username, password):
        url = self.__generateLink(OvizartProxy.LOGIN_URL)
        response = requests.post(url, verify=False, headers={'content-type': 'application/json'},
                                 data=json.dumps({'username': username, 'password': password}))

        # Check for login success?
        result = json.loads(response.content)
        if result['Status'] == 'OK':
            userid = result['userid']
            self.login_success = True
            self.cookies = response.cookies
            self.username = username
            self.password = password
            self.userid = userid

        return result

    def uploadFile(self, filename, fileobj=None):
        import os
        result = "NA"
        filepath = os.path.abspath(filename)
        filename = os.path.basename(filepath)

        if fileobj:
                url = self.__generateLink(OvizartProxy.UPLOAD_URL) + '/' + filename
                response = requests.post(url, verify=False, data=fileobj, headers={'content-type': 'application/octet-stream'},
                                         cookies=self.cookies)
                result = json.loads(response.content)

        elif filename:
            url = self.__generateLink(OvizartProxy.UPLOAD_URL) + '/' + filename
            with open(filepath, 'r') as f:
                # Form based approach
                #response = requests.post(url, verify=False, files={'file': (filename, f)}, cookies=self.cookies)
                # Stream based approach
                response = requests.post(url, verify=False, data=f, headers={'content-type': 'application/octet-stream',
                                                                             'Connection':'close'},
                                         cookies=self.cookies)
                result = json.loads(response.content)


        return result

    def start(self):
        url = self.__generateLink(OvizartProxy.START_URL)
        response = requests.post(url, verify=False, headers={'content-type': 'application/json'}, cookies=self.cookies)
        result = json.loads(response.content)
        return result

    def getAnalysis(self, analysisId=None):
        url = self.__generateLink(OvizartProxy.LIST_ANALYSIS)

        if analysisId:
            url = url + '/' + analysisId

        response = requests.get(url, verify=False, headers={'content-type': 'application/json'}, cookies=self.cookies)
        result = json.loads(response.content)
        return result
