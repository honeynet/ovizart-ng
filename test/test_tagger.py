from numpy.testing.utils import assert_equal
from tagger.protocol.future_protocols import HTTPSHandshake, SSHHandshake, SOCKS4Connect

__author__ = 'ggercek'

import unittest
from scapy.all import *
from tagger.protocol import SMTPRequest, HTTPRequest, HTTPResponse, FTPResponse


class MyTestCase(unittest.TestCase):
    def test_smtp_request(self):
        count = 0
        pkts = rdpcap("./pcap/smtp.pcap")
        for p in pkts:
            if p.haslayer(SMTPRequest):
                print p.summary()
                count += 1
        assert_equal(count, 6)

    def test_http_request(self):
        count = 0
        pkts = rdpcap("./pcap/test-http.pcap")
        for p in pkts:
            if p.haslayer(HTTPRequest):
                print p.summary()
                count += 1
        assert_equal(count, 19)

    def test_http_response(self):
        count = 0
        pkts = rdpcap("./pcap/test-http.pcap")
        for p in pkts:
            if p.haslayer(HTTPResponse):
                print p.summary()
                count += 1
        assert_equal(count, 18)

    def test_ftp_response(self):
        count = 0
        pkts = rdpcap("./pcap/test-ftp.pcap")
        for p in pkts:
            if p.haslayer(FTPResponse):
                print p.summary()
                count += 1
        assert_equal(count, 2)

    def test_https_handshake(self):
        count = 0
        pkts = rdpcap("./pcap/test-https-handshake.pcap")
        for p in pkts:
            if p.haslayer(HTTPSHandshake):
                print p.summary()
                count += 1
        assert_equal(count, 2)

    def test_ssh_handshake(self):
        count = 0
        pkts = rdpcap("./pcap/test-ssh-handshake.pcap")
        for p in pkts:
            if p.haslayer(SSHHandshake):
                print p.summary()
                count += 1
        assert_equal(count, 2)

    def test_socksv4_connect(self):
        count = 0
        pkts = rdpcap("./pcap/test-socks4-connect.pcap")
        for p in pkts:
            if p.haslayer(SOCKS4Connect):
                print p.summary()
                count += 1
        assert_equal(count, 1)

if __name__ == '__main__':
    unittest.main()
