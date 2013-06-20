__author__ = 'ggercek'

from unittest import TestCase

from datasource.tcpflow import TcpFlow

class TestTcpFlow(TestCase):

    def test_parseReportXML(self):
        parser = TcpFlow()
        parser.parseReportXML('../output/report.xml')
