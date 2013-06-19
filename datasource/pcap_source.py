""" Handlers for PCAP files """
from ovizart import Tags
from core import DataSource

PCAP = Tags.DataSource.PCAP

@DataSource(tags=PCAP)
class PcapHandler:
    """Pcap file handler, wrapper for tcpflow. Currently this class supports only offline traffic parsing"""

    def __init__(self):
        pass

    def __repr__(self):
        return "PcapHandler"

    def parse(self, data):
        pass