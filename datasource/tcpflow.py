""" Handlers for PCAP files """

__author__ = "ggercek"

from xml.dom import minidom
from subprocess import call
import os
import datetime

from core.tags import Tags
from core.engine import DataSource
from core.data import Data

PCAP = Tags.DataSource.PCAP


#@DataSource(tags=PCAP)
class TcpFlow:
    """Pcap file handler, wrapper for tcpflow. Currently this class supports only offline traffic parsing"""

    def __init__(self):
        pass

    def __repr__(self):
        return "TcpFlow Handler"

    def parse(self, filename):
        """Separates given pcap file into separate pcap files"""
        summary = {'inputFile': {'filename': filename}, 'flows': []}
        outputFolder = self.runTcpFlow(filename)
        summary['flows'] = self.parseReportXML(outputFolder + 'report.xml')

        return summary

    def runTcpFlow(self, filename):
        # TODO: Move this to conf.cfg or conf.py ?!
        outputFolder = os.path.abspath('../output') + '/'

        # get timestamp for folder name
        newDir = outputFolder + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        newDir = os.path.abspath(newDir) + '/'

        if not os.path.isdir(outputFolder):
            os.mkdir(outputFolder)
        os.mkdir(newDir)

        # Run tcpflow for given pcap file.
        cmd = 'tcpflow -r ' + filename + ' -o ' + newDir
        print cmd
        call(cmd, shell=True)
        return newDir

    def parseReportXML(self, report):
        def __getTextData(node, target):
            node.getElementsByTagName(target)[0].childNodes[0].data

        # parse the report.xml
        r = minidom.parse(report)
        fileobjects = r.getElementsByTagName('fileobject')

        flows = []
        for f in fileobjects:
            flow = Data()

            flow.data('filename', __getTextData(f, 'filename'))
            flow.data('filesize', __getTextData(f, 'filesize'))

            # TODO: Check the UDP flows as well
            finfo = f.getElementsByTagName('tcpflow')[0]

            attributeNames = ['starttime', 'endtime', 'src_ipn', 'dst_ipn',
                              'packets', 'srcport', 'dstport', 'family', 'out_of_order_count']

            # TODO: Make it dynamic
            for attributeName in attributeNames:
                flow.data(attributeName, finfo.getAttribute(attributeName))

            #<tcpflow
            #   startime='2013-06-20T15:58:46.901328Z'
            #   endtime='2013-06-20T15:59:58.043994Z'
            #   src_ipn='218.100.43.174'
            #   dst_ipn='192.168.1.103'
            #   packets='30'
            #   srcport='8001'
            #   dstport='33478'
            #   family='2'
            #   out_of_order_count='2' />

            flows.append(flow)

        return flows
