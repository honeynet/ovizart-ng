__author__ = 'ggercek'

from datasource.pcap_handler import PcapDataSourceHandler
from ovizart import Ovizart
from ovizconf import Config

import os

if '__main__' == __name__:
    config = Config()
    ovizart = Ovizart(config)
    ovizart.listAvailableModules()
    ovizart.setInputFile('./pcap/test-http.pcap')
    analysis = ovizart.start()
    print analysis

