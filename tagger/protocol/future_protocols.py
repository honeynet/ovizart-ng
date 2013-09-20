__author__ = 'ggercek'

from scapy.fields import ByteField, StrField
from scapy.packet import Packet


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


class SSHHandshake(Packet):
    protocol = "SSH"
    name = "SSH Handshake"
    fields_desc = [StrField("identification-string", None, fmt="H"), ]

    def mysummary(self):
        return self.sprintf("SSH Handshake: %SMTPRequest.cmd% req_param: %SMTPRequest.req_param%")


