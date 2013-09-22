__author__ = 'ggercek'

from scapy.fields import ByteField, StrField, ShortField, IntField
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
        return self.sprintf("HTTPS Handshake: %HTTPSHandshake.content-type% version: "
                            "%HTTPSHandshake.majVersion%.%HTTPSHandshake.minVersion%")


class SSHHandshake(Packet):
    protocol = "SSH"
    name = "SSH Handshake"
    fields_desc = [StrField("identification-string", "", fmt="H"), ]

    def mysummary(self):
        return self.sprintf("SSH Handshake: %SSHHandshake.identification-string%")


class SOCKS4Connect(Packet):
    protocol = "SOCKSv4"
    name = "SOCKS v4 Connect"
    fields_desc = [ByteField("version", ""),
                   ByteField("cmd", ""),
                   ShortField("remote-port", ""),
                   IntField("remote-ip", ""),
                   StrField("username", "")]

    def mysummary(self):
        return self.sprintf("SOCKSv4 Connect(version:%SOCKS4Connect.version%, cmd:%SOCKS4Connect.cmd%, "
                            "remote-port:%SOCKS4Connect.remote-port%, remote-ip:%SOCKS4Connect.remote-ip%, "
                            "username: %SOCKS4Connect.username%)")
