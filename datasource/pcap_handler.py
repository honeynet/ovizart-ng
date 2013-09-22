__author__ = 'ggercek'

import os
import pcap
import struct
import dpkt

from core.tags import Tags
from core.engine import DataSource
from core.data import Data

PCAP = Tags.DataSource.PCAP

_numberOfPacket = 0


class IDCacheNode():
    def __init__(self, ip_type, ip1, port1, ip2, port2, id):
        self.ip_type = ip_type
        self.ip1 = ip1
        self.ip2 = ip2
        self.port1 = port1
        self.port2 = port2
        self.id = id

def _decode_byte(data):
    """Decodes one byte of network data into an unsigned char."""
    return struct.unpack('!B', data)[0]


def _decode_short(data):
    """Decodes two bytes of network data into an unsigned short."""
    return struct.unpack('!H', data)[0]

def _decode_int(data):
    return struct.unpack('!L', data)[0]

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
    Streams are identified as follows, <start_time, protocol, ip1, [port1,] ip2, [port2]>
    ports will be used if port field exists.
    Streams will be finished with timeout value of 60 sec.
    """
    def __init__(self):
        self.streams = {}
        self.outputFolder = None
        self.ipIdentificationCacheIndexByIP = {}
        self.ipIdentificationCacheIndexByIPandPort = {}

    def __repr__(self):
        return "Pcap Data Source Handler"

    def parse(self, filename, outputFolder):
        """Parse given pcap file
        @param filename: full path of given pcap file
        @return summary of the pcap file with stream information
        """
        summary = {'inputFile': {'filename': filename,
                                 'numberOfPacket': 0,
                                 'numberOfStreams': 0},
                   'outputFolder': outputFolder,
                   'data': []}
        self.outputFolder = outputFolder

        p = pcap.pcapObject()
        p.open_offline(filename)
        # process all packets
        p.dispatch(-1, self.processPacket)

        global _numberOfPacket
        summary['inputFile']['numberOfPacket'] = _numberOfPacket
        summary['inputFile']['numberOfStreams'] = len(self.streams)
        for k in self.streams.keys():
            data = Data()
            data.setStream(self.streams[k])
            summary['data'].append(data)
            self.streams[k].closePcapFile()

        self.outputFolder = None
        return summary

    def processPacket(self, length, data, ts):
        global _numberOfPacket, _tpid, _ether_type
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

        _numberOfPacket += 1
        #self.dumpStreamHeader(streamHeader)
        stream = self.getStream(streamHeader, data)
        if not stream:
            stream = Stream.generateStream(streamHeader, data, self.outputFolder)
            # first packet automatically added to generated stream no need to add twice.
            self.streams[stream.key] = stream
        else:
            stream.addPacket(ts, data)

    def _getIPv4Header(self, ts, data):
        ip_type = data[9]
        src = data[12:16]
        dst = data[16:20]
        sport = dport = None

        # Check for fragmentation
        ip_identification = data[4:6]
        ip_identification = _decode_short(ip_identification)
        #print 'ip_identification:', ip_identification
        fragOffset = data[6:8]
        fragOffset = _decode_short(fragOffset)
        fragOffset = (fragOffset & 0x1fff) << 3
        # TODO: find session based on IP.identification and flag
        #print fragOffset

        if fragOffset == 0 and (ip_type == _ip_protocol['TCP'] or ip_type == _ip_protocol['UDP']):
            header_len = 4 * (_decode_byte(data[0]) & 0x0f)
            tot_len = _decode_short(data[2:4])
            pld = data[header_len:tot_len]
            #sport, dport = _process_tcp(ts, src, dst, pld)
            sport = _decode_short(pld[0:2])
            dport = _decode_short(pld[2:4])

            self.updateIpIdentification(ip_type, src, sport, dst, dport, ip_identification)
        else :
            # if fragoffset is non zero then we can not read port values
            # TODO: use fragmented packets on reassembler.
            # TODO: store the streams in a hierarchical structure so that we can find the fragmented streams easier.
            # TODO: apply RFC815 http://tools.ietf.org/html/rfc815
            src, sport, dst, dport = self.updateIpIdentification(ip_type, src, None, dst, None, ip_identification)

        ipv4Header = None
        if sport and dport:
            ipv4Header = (ip_type, src, sport, dst, dport, ts)
        else:
            # Something must be wrong ?! Check this issue...
            ipv4Header = (ip_type, src, dst, ts)
        print '#### returning ths value ########'
        self.dumpStreamHeader(ipv4Header)
        print '#################################'
        return ipv4Header

    def updateIpIdentification(self, ip_type, ip1, port1, ip2, port2, ip_identification):
        def _keys(ip_type, ip1, port1, ip2, port2):
            if port1 and port2:
                key1 = "%d%d%d%d%d" % (_decode_byte(ip_type), _decode_int(ip1), port1, _decode_int(ip2), port2)
                key2 = "%d%d%d%d%d" % (_decode_byte(ip_type), _decode_int(ip2), port2, _decode_int(ip1), port1)
            else:
                key1 = "%d%d%d" % (_decode_byte(ip_type), _decode_int(ip1), _decode_int(ip2))
                key2 = "%d%d%d" % (_decode_byte(ip_type), _decode_int(ip2), _decode_int(ip1))
            return key1, key2

        def _findClosestNodeById(idCacheNodeArray, idToSearch):
            # Improve this part !!!
            minDistance = 99999999
            minNode = None

            for node in idCacheNodeArray:
                distance = abs(node.id - idToSearch)
                if distance < minDistance:
                    minDistance = distance
                    minNode = node

            return minNode

        #print 'ip_type', type(ip_type), _decode_byte(ip_type), 'ip1', type(ip1), _decode_int(ip1), 'port1', type(port1), port1, 'ip2', type(ip2), _decode_int(ip2), 'port2', type(port2), port2

        key1, key2 = _keys(ip_type, ip1, port1, ip2, port2)
        # TODO: What if fragmentation occurs on handshake
        if port1 and port2:
            if key1 in self.ipIdentificationCacheIndexByIPandPort:
                self.ipIdentificationCacheIndexByIPandPort[key1].id = ip_identification
            if key2 in self.ipIdentificationCacheIndexByIPandPort:
                self.ipIdentificationCacheIndexByIPandPort[key2].id = ip_identification
            else:
                # new session create a IDCacheNode
                node = IDCacheNode(ip_type, ip1, port1, ip2, port2, ip_identification)
                self.ipIdentificationCacheIndexByIPandPort[key1] = node
                key1, key2 = _keys(ip_type, ip1, None, ip2, None)
                if not key1 in self.ipIdentificationCacheIndexByIP:
                    self.ipIdentificationCacheIndexByIP[key1] = []

                self.ipIdentificationCacheIndexByIP[key1].append(node)
        else:
            if key1 in self.ipIdentificationCacheIndexByIP:
                nodeArray = self.ipIdentificationCacheIndexByIP[key1]
            if key2 in self.ipIdentificationCacheIndexByIP:
                nodeArray = self.ipIdentificationCacheIndexByIP[key2]
            else:
                # TODO: Something is not right!!!!
                return ip1, port1, ip2, port2

            node = _findClosestNodeById(nodeArray, ip_identification)
            if node:
                # Update the last id
                node.id = ip_identification
                print 'for fragmented ip_id:', ip_identification, 'found values: ****************************************'
                self.dumpStreamHeader((node.ip_type, node.ip1, node.port1, node.ip2, node.port2))
                return node.ip1, node.port1, node.ip2, node.port2
            else:
                print 'Can not find any session for this id:', ip_identification
                self.dumpStreamHeader((ip_type, ip1, port1, ip2, port2))

            return ip1, port1, ip2, port2

    def dumpStreamHeader(self, streamHeader):
        proto = 0; sip = 1; dip = 3; sport = 2; dport = 4; ts = -1;
        if len(streamHeader) == 4:
            dip = 2; sport = ''; dport = ''

        proto = _decode_byte(streamHeader[proto])
        sip = address_to_string(streamHeader[sip])
        dip = address_to_string(streamHeader[dip])

        if sport and dport:
            sport = streamHeader[sport]
            dport = streamHeader[dport]

        ts = streamHeader[ts]
        print proto, sip, sport, dip, dport, ts

    def getStream(self, streamHeader, pkt):
        #protocol, srcIP, srcPort, dstIP, dstPort, ts = None

        keys = Stream.generateKeys(streamHeader)
        stream = None
        if keys[0] in self.streams:
            # use src based key
            stream = self.streams[keys[0]]
        elif keys[1] in self.streams:
            # use dst based key
            stream = self.streams[keys[1]]
        return stream


class Stream:
    def __init__(self, protocol, srcIP, srcPort, dstIP, dstPort, startTime, pkt, outputFolder):
        self.protocol = _decode_byte(protocol)
        self.srcIP = address_to_string(srcIP)
        self.srcPort = str(srcPort)
        self.dstIP = address_to_string(dstIP)
        self.dstPort = str(dstPort)
        self.startTime = str(startTime)

        self.key = Stream.generateKeys((protocol, srcIP, srcPort, dstIP, dstPort, startTime))[0]

        # File based variables
        self.outputFolder = os.path.join(outputFolder, self.key)
        self.pcapFileName = os.path.join(self.outputFolder, self.key + ".pcap")
        self.pcapFile = None
        self.fileHandler = None
        self.__openPcapFile()

        # TODO: take first packet as argument
        #self.pkts = []
        self.pktCount = 0
        self.last_ts = None
        self.addPacket(startTime, pkt)

    def __repr__(self):
        s = 'Stream Object {key: %s, protocol: %d, srcIP: %s, srcPort: %s, dstIP: %s, dstPort: %s, startTime: %s, numberOfPacket: %d, pcapFile: %s}' \
            % (self.key, self.protocol, self.srcIP, self.srcPort, self.dstIP, self.dstPort, self.startTime,
               self.pktCount, self.pcapFileName)
        #% (self.key, _decode_byte(self.protocol), address_to_string(self.srcIP), str(self.srcPort),
            #address_to_string(self.dstIP), str(self.dstPort), str(self.startTime), self.pktCount, self.pcapFileName)

        return s

    def addPacket(self, ts, pkt):
        if pkt:
            # check the last pkt time
            if not self.isTimeoutOccured(ts):
                if self.fileHandler:
                    self.fileHandler.writepkt(pkt, ts)
                    self.last_ts = ts
                    self.pktCount += 1
                #self.pkts.append((ts, pkt))

    def __openPcapFile(self):
        import ovizutil
        result = False
        if not self.pcapFile or self.pcapFile.closed:
            ovizutil.createFolder(self.outputFolder)

            self.pcapFile = open(self.pcapFileName, 'wb')
            self.fileHandler = dpkt.pcap.Writer(self.pcapFile, snaplen=65535)
            result = True
        return result

    def closePcapFile(self):
        result = False
        if self.pcapFile or not self.pcapFile.closed:
            self.pcapFile.flush()
            self.fileHandler.close()
            self.fileHandler = None
            self.pcapFile = None
            result = True
        return result

    def isTimeoutOccured(self, ts):
        result = False
        if self.last_ts:
            result = ts - self.last_ts > 60000

        return result

    @staticmethod
    def generateStream(streamHeader, pkt, outputFolder):
        stream = None
        if len(streamHeader) == 4:
            stream = Stream(streamHeader[0], streamHeader[1],
                            None,     streamHeader[2],
                            None,     streamHeader[3],
                            pkt, outputFolder)
        else:
            stream = Stream(streamHeader[0], streamHeader[1],
                            streamHeader[2], streamHeader[3],
                            streamHeader[4], streamHeader[5],
                            pkt, outputFolder)

        return stream

    @staticmethod
    def generateKeys(streamHeader):
        proto = 0; sip = 1; dip = 3; sport = 2; dport = 4; ts = -1;

        if len(streamHeader) == 4 :
            dip = 2
            sport = None
            dport = None
        elif not (streamHeader[sport] and streamHeader[dport]):
            sport = None
            dport = None

        proto = _decode_byte(streamHeader[proto])
        sip = address_to_string(streamHeader[sip])
        dip = address_to_string(streamHeader[dip])

        if sport and dport:
            sport = streamHeader[sport]
            dport = streamHeader[dport]
            key1 = "%s_%s_%d_%s_%d" % (proto, sip, sport, dip, dport)
            key2 = "%s_%s_%d_%s_%d" % (proto, dip, dport, sip, sport)
        else:
            key1 = "%s_%s_%s" % (proto, sip, dip)
            key2 = "%s_%s_%s" % (proto, dip, sip)

        return key1, key2
