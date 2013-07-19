__author__ = 'ggercek'

from unittest import TestCase

from datasource.tcpflow import TcpFlow
import os


class TestTcpFlow(TestCase):

    def test_parseReportXML(self):
        parser = TcpFlow()
        f = os.path.abspath('./pcap/report.xml')
        parser.parseReportXML(f)

    def test_run(self):
        parser = TcpFlow()
        f = os.path.abspath('./pcap/test-http.pcap')
        print 'f: ', f
        out = parser.runTcpFlow(f)
        print out

    def test_parse(self):
        parser = TcpFlow()
        f = os.path.abspath('./pcap/test-http.pcap')
        out = parser.parse(f)
        print out
