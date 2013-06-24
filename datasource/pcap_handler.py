__author__ = 'ggercek'

import pcap
from ovizart import Tags
from core import DataSource
from core import Data

PCAP = Tags.DataSource.PCAP

_count = 0

import struct
def _decode_byte(data):
    """Decodes one byte of network data into an unsigned char."""
    return struct.unpack('!B', data)[0]

def _decode_short(data):
    """Decodes two bytes of network data into an unsigned short."""
    return struct.unpack('!H', data)[0]

def address_to_string(b):
    """Converts an IP address to its string representation.
    Takes a 4-byte string representing an IP address, and returns a
    dot-separated decimal representation on the form '123.123.123.123'.
    """
    assert len(b) == 4
    b = map(lambda x: str(_decode_byte(x)), b)
    return '.'.join(b)

# TPID from IEEE 802.1Q
_tpid = '\x81\x00'

# EtherType constants
_ether_type = {
    'IPv4': '\x08\x00',
    'IPv6': '\x86\xdd',
}

# IP protocol field constants
_ip_protocol = {
    'TCP': '\x06',
    'UDP': '\x11',
}


@DataSource(tags=PCAP)
class PcapDataSourceHandler:
    """Parse pcap files and build up IP streams.
    Streams are identified as follows, <start_time, protocol, ip1, [port1,] ip2, [port2]> ports will be used if port field exists.
    Streams will be finished with timeout value of 60 sec.
    """
    def __init__(self):
        self.streams = {}

    def __repr__(self):
        return "Pcap Data Source Handler"

    def parse(self, filename):
        """Parse given pcap file
        @param filename: full path of given pcap file
        @return summary of the pcap file with stream information
        """
        summary = {'inputFile': {'filename': filename}, 'flows': []}

        p = pcap.pcapObject()
        p.open_offline(filename)
        # process all packets
        p.dispatch(-1, self.getStreamHeader)

        global _count
        print 'count: ', _count
        return summary

    def getStreamHeader(self, length, data, ts):
        global _count, _tpid, _ether_type
        ieee_8021q = data[12:14] == _tpid
        if ieee_8021q:
        #    tci = data[14:16]
            eth_type = data[16:18]
            pld = data[18:]
        else:
            eth_type = data[12:14]
            pld = data[14:]

        if eth_type == _ether_type['IPv4']:
            streamHeader = self._getIPv4Header(ts, pld)
        else:
            # TODO: Add ipv6 support
            pass

        _count += 1
        self.dumpStreamHeader(streamHeader)
        stream = self.getStream(streamHeader, data)
        if stream:
            stream = Stream.generateStream(streamHeader, data)
            # first packet automatically added to generated stream no need to add twice.
            self.streams[stream.key] = stream
        else:
            stream.addPacket(ts, data)

        print stream.key

    def _getIPv4Header(self, ts, data):
        ip_type = data[9]
        src = data[12:16]
        dst = data[16:20]
        sport = dport = None

        if ip_type == _ip_protocol['TCP'] or ip_type == _ip_protocol['UDP']:
            header_len = 4 * (_decode_byte(data[0]) & 0x0f)
            tot_len = _decode_short(data[2:4])
            pld = data[header_len:tot_len]
            #sport, dport = _process_tcp(ts, src, dst, pld)
            sport = _decode_short(pld[0:2])
            dport = _decode_short(pld[2:4])

        ipv4Header = None
        if sport and dport:
            ipv4Header = (ip_type, src, sport, dst, dport, ts)
        else:
            ipv4Header = (ip_type, src, dst, ts)

        return ipv4Header

    def dumpStreamHeader(self, streamHeader):
        proto = 0; sip = 1; dip = 3; sport = 2; dport = 4; ts = -1;
        if len(streamHeader) == 4:
            dip = 2; sport = ''; dport = ''

        proto = _decode_byte(streamHeader[proto])
        sip = address_to_string(streamHeader[sip])
        dip = address_to_string(streamHeader[dip])

        if sport and dport :
            sport = streamHeader[sport]
            dport = streamHeader[dport]

        ts = streamHeader[ts]
        print proto, sip, sport, dip, dport, ts

    def getStream(self, streamHeader, pkt):
        #protocol, srcIp, srcPort, dstIp, dstPort, ts = None

        def _getKeys(protocol, srcIp, srcPort, dstIp, dstPort):
            format = None; tuple1 = None; tuple2 = None

            if srcPort and dstPort:
                format = "%s_%s_%s"
                tuple1 = (protocol, srcIp, dstIp)
                tuple2 = (protocol, dstIp, srcIp)
            else:
                format = "%s_%s_%d_%s_%d"
                tuple1 = (protocol, srcIp, srcPort, dstIp, dstPort)
                tuple2 = (protocol, dstIp, dstPort, srcIp, srcPort)

            key1 = format % tuple1
            key2 = format % tuple2

            return key1, key2

        keys = _getKeys(protocol, srcIp, srcPort, dstIp, dstPort)
        stream = None
        if keys[0] in self.streams:
            # use src based key
            stream = self.streams[keys[0]]
        elif keys[1] in self.streams:
            # use dst based key
            stream = self.streams[keys[1]]
        #else:
            # new stream: use src based key
            #s = Stream(protocol, srcIp, srcPort, dstIp, dstPort, ts, pkt)
            #stream = self.streams[keys[0]]

        return stream


class Stream:
    def __init__(self, protocol, srcIp, srcPort, dstIp, dstPort, startTime, pkt):
        self.protocol = protocol
        self.srcIP = srcIp
        self.srcPort = srcPort
        self.dstIp = dstIp
        self.dstPort = dstPort
        self.startTime = startTime

        # TODO: Set proper key
        if srcPort and dstPort:
            self.key = "%d_%d_%d_%d" % (self.protocol, self.srcIP, self.dstIp, self.startTime)
        else:
            self.key = "%d_%d_%d_%d_%d_%d" % \
                       (self.protocol, self.srcIP, self.srcPort, self.dstIp, self.dstPort, self.startTime)

        # TODO: take first packet as argument
        self.pkts = []
        self.addPacket(startTime, pkt)

    def addPacket(self, ts, pkt):

        if pkt:
            # check the last pkt time
            if not self.isTimeoutOccured(ts):
                self.pkts.append(ts, pkt)

    def isTimeoutOccured(self, ts):
        result = False
        if self.pkts:
            last_ts = self.pkts[-1][0]
            result = ts - last_ts > 60000
        return result

    def generateStream(streamHeader, pkt):
        stream = None
        if len(streamHeader) == 4:
            stream = Stream(streamHeader[0], streamHeader[1], None,     streamHeader[2], None,     streamHeader[3], pkt)
        else:
            stream = Stream(streamHeader[0], streamHeader[1], streamHeader[2], streamHeader[3], streamHeader[4], streamHeader[5], pkt)

        return stream

if __name__ == '__main__':
    import os
    p = PcapDataSourceHandler()
    f = os.path.abspath('../output/test-http.pcap')
    p.parse(f)
