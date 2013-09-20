from scapy.fields import ByteField, StrField
from scapy.packet import Packet

__author__ = 'ggercek'


class HTTPSHandshake(Packet):
    protocol = "HTTPS"
    name = "HTTPS Handshake"
    fields_desc = [ByteField("content-type", ""),
                   ByteField("majVersion", ""),
                   ByteField("minVersion", ""),
                   #StrField("rest", "", "")
                   ]

    def mysummary(self):
        return self.sprintf("HTTPS Handshake: %SMTPRequest.cmd% req_param: %SMTPRequest.req_param%")


