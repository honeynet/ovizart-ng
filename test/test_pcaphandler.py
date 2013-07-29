

__author__ = "ggercek"

from unittest import TestCase
from datasource.pcap_handler import PcapDataSourceHandler

import os

OUTPUT_FOLDER = os.path.abspath("../output/test_pcaphandler/")


class TestPcapHandler(TestCase):

    def test_generic_pcap(self):
        p = PcapDataSourceHandler()
        f = os.path.abspath('pcap/test-http.pcap')
        p.parse(f, OUTPUT_FOLDER)

    def test_fragmented_pcap(self):
        p = PcapDataSourceHandler()
        f = os.path.abspath('pcap/test-fragmentation.pcap')
        p.parse(f, OUTPUT_FOLDER)
