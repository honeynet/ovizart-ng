__author__ = 'ggercek'

from scapy.packet import Packet
from scapy.fields import StrFixedLenField, StrField


class SMTPReqField(StrField):
    #holds_packets = 1
    name = "SMTPReqField"

    cmds = ["EHLO", "DATA", "AUTH", "MAIL", "RCPT", "QUIT"]

    def getfield(self, pkt, s):
        ls = s.split()
        length = len(ls)
        cmd = ls[0].upper()
        if cmd in SMTPReqField.cmds:
            return " ".join(ls[1:]), cmd

    def __init__(self, name, default, fmt, remain=0):
        """
class constructor for initializing the instance variables
@param name: name of the field
@param default: Scapy has many formats to represent the data
internal, human and machine. anyways you may sit this param to None.
@param fmt: specifying the format, this has been set to "H"
@param remain: this parameter specifies the size of the remaining
data so make it 0 to handle all of the data.
"""
        self.name = name
        StrField.__init__(self, name, default, fmt, remain)


class SMTPRequest(Packet):
    protocol = "SMTP"
    name = "SMTP Request"
    fields_desc = [SMTPReqField("cmd", "", "H"),
                   StrField("req_param", "",),
                   StrFixedLenField("sep", "\r\n", 2)]

    def mysummary(self):
        return self.sprintf("SMTPRequest cmd: %SMTPRequest.cmd% req_param: %SMTPRequest.req_param%")
