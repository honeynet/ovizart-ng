__author__ = 'ggercek'

from smtp import *
from http import *
from ftp import *
from future_protocols import *

from core.engine import Tagger
from core.tags import Tags
PCAP = Tags.DataSource.PCAP

from scapy.packet import split_layers, bind_layers
from scapy.layers.inet import IP
from scapy.layers.inet import TCP as OldTCP
from scapy.layers.inet import UDP as OldUDP
import re
import struct

from tagger.protocol import *

tcp_signatures = [
    (r'^(EHLO|DATA|AUTH|MAIL|RCPT|QUIT).*', SMTPRequest),
    (r'^(GET|HEAD|POST|OPTIONS|PUT|DELETE|TRACE|CONNECT).*', HTTPRequest),
    (r'^(HTTP\/[0-9]).*', HTTPResponse),
    (r'^(230|331).*', FTPResponse),
    (b'^(?P<contentType>[\x14\x15\x16\x17])(?P<majVersion>[\x03])(?P<minVersion>[\x00\x01\x02\x03])', HTTPSHandshake),
    (r'^SSH', SSHHandshake)
            ]

udp_signatures = [
    (),
    ()
             ]


@Tagger(tags=PCAP)
class ProtocolTagger:
    """Parse the splitted pcap files and try to recognize application layer protocol of packets, based on the
    signatures registered to system. Currently supported protocols are: SMTP, HTTP, FTP
    """

    def __repr__(self):
        return "Protocol Tagger based on Packet Signatures"

    class TCP(OldTCP):
        def guess_payload_class(self, payload):
            for sig, cls in tcp_signatures:
                if re.match(sig, payload, re.IGNORECASE):
                    return cls

            # if signatures are empty
            return OldTCP.guess_payload_class(self, payload)

    class UDP(OldUDP):
        def guess_payload_class(self, payload):
            for sig, cls in udp_signatures:
                if re.match(sig, payload, re.IGNORECASE):
                    return cls

            # if signatures are empty
            return OldUDP.guess_payload_class(self, payload)

    split_layers(IP, OldTCP)
    #split_layers(IP, OldUDP)
    bind_layers(IP, TCP, frag=0, proto=6)
    #bind_layers(IP, UDP, frag=0, proto=17)

    def tag(self, data):
        # parse the file.
        # Collect all lastlayer to check the application layer protocol.
        # tag the found protocols to stream
        stream = data.getStream()
        # TODO: Change this part
        #protocol = struct.unpack('!B', stream.protocol)[0]
        protocol = stream.protocol

        recognized_layers = []
        if protocol == 6:
            recognized_layers = [layers for signatures, layers in tcp_signatures]
        elif protocol == 17:
            #recognized_layers = [layers for signatures, layers in udp_signatures]
            pass

        pcapFile = stream.pcapFileName
        pkts = rdpcap(pcapFile)

        for p in pkts:
            for layer in recognized_layers:
                if p.haslayer(layer):
                    data.setApplicationLayerProtocol(layer.protocol)
                    return

        data.setApplicationLayerProtocol('UNKNOWN')
