__author__ = 'ggercek'

import subprocess, os
from reassembler import run_reassembler
from unittest import TestCase


class TestSMTPReassembler(TestCase):

    def test_smtp(self):
        pcap_file = "../output/smtp.pcap"
        parser_class = "SMTPReassembler"
        output_folder = "../output/reassembler-test/smtp"
        run_reassembler(pcap_file, parser_class, output_folder)

