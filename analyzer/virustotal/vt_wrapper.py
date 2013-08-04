"""
VirusTotal Wrapper
"""

__author__ = "zqzas"

import os
import sys
import urllib, urllib2, json
import postfile

from core.engine import Analyzer
from core.tags import Tags
from analyzer import BaseAnalyzer

BINARY = Tags.Attachment.BINARY

sys.path.append("../../")
from ovizconf import Config

#APIKEY = Config().vt_apikey


@Analyzer(tags=BINARY)
class VTWrapper(BaseAnalyzer):
    """Wrapper class for Virus Total"""

    def __init__(self):
        BaseAnalyzer.__init__(self)

    def __repr__(self):
        return "A virustotal wrapper"

    def analyze(self, data):

        def retrievePath(data):
            """ get the path of data """
            stream = data.getStream()
            files = []
            attachments = data.getAttachments()
            folder = data.getAttachmentsFolder()
            for a in attachments:
                filename = a[0]
                filetype = a[1]
                if filetype.endswith('binary'):
                    filename = os.path.join(folder, filename)
                    files.append(filename)

            return files

        path = retrievePath(data)[0]
        self.analyzeBinary(path)

    def analyzeBinary(self, path):
        """
        Analyze Binary.
        @param path: the path to the file
        @return         : the report
        """

        if self.conf is None:
            self.conf = Config()

        vt = 'www.virustotal.com'

        selector = "https://www.virustotal.com/vtapi/v2/file/scan"

        fields = [("apikey", self.conf.vt_apikey)]

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

        if self.conf is None:
            self.conf = Config()

        selector = "https://www.virustotal.com/vtapi/v2/url/report"       
        parameters = {"resource": url, "apikey": self.conf.vt_apikey, 'scan': '1'}

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



