__author__ = 'ggercek'

from datasource.pcap_handler import PcapDataSourceHandler
from ovizart import Ovizart

import os

if '__main__' == __name__:
    ovizart = Ovizart()
    ovizart.listAvailableModules()
    ovizart.setInputFile('../output/test-http.pcap')
    analysis = ovizart.start()
    print analysis

