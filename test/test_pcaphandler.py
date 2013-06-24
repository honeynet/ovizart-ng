

__author__ = "ggercek"

from unittest import TestCase
from datasource.pcap_handler import PcapDataSourceHandler

import os


class TestPcapHandler(TestCase):

    def test_generic_pcap(self):
        p = PcapDataSourceHandler()
        f = os.path.abspath('../output/test-http.pcap')
        p.parse(f)

    def test_fragmented_pcap(self):
        p = PcapDataSourceHandler()
        f = os.path.abspath('../output/test-fragmentation.pcap')
        p.parse(f)
