"""
VirusTotal Wrapper
"""

__author__ = "zqzas"

import sys
import urllib, urllib2, json
import postfile

sys.path.append("../../")
from conf import Config

APIKEY = Config().vt_apikey

class VTWrapper:
    def __init__(self):
        pass
    def __repr__(self):
        print "A virustotal wrapper"

    def analyzeBinary(self, path):
        """
        Analyze Binary.
        @param path: the path to the file
        @return         : the report
        """

        vt = 'www.virustotal.com'

        selector = "https://www.virustotal.com/vtapi/v2/file/scan"

        fields = [("apikey", APIKEY)]

        binary = open(path, "rb").read()

        files = [("file", "test.bin", binary)]

        json = postfile.post_multipart(vt, selector, fields, files)

        print '-------------------\n\n'
        print json

        return json



    def analyzeUrl(self, url):
        """
        Analyze URL
        @param url      : the url to be analyzed
        @return         : the report
        """

        selector = "https://www.virustotal.com/vtapi/v2/url/report"       
        parameters = {"resource": url, "apikey": APIKEY, 'scan': '1'}

        data = urllib.urlencode(parameters)
        req = urllib2.Request(selector, data)
        response = urllib2.urlopen(req)
        json = response.read()
        print '-------------------\n\n'
        print json

        return json


if __name__ == '__main__':
    vt = VTWrapper()
    vt.analyzeUrl('www.zqzas.com')



