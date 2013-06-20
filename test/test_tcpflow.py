__author__ = 'ggercek'

from unittest import TestCase

from ovizart.tcpflow import TcpFlow


class TestPcapHandler(TestCase):

    def test_parseReportXML(self):

        parser = TcpFlow()

        parser.parseReportXML('output/report.xml')

