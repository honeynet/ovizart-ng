__author__ = 'ggercek'


from base_reassembler import *
from smtp_reassembler import *

import os, subprocess


def run_reassembler(pcap_file, parser_class, output_folder):
    parser_script = "base_reassembler.py"
    pcap_file = os.path.abspath(pcap_file)
    parser_script = os.path.abspath(parser_script)
    output_folder = os.path.abspath(output_folder)

    arguments = parser_class + "|" + output_folder
    options_to_pass = list()
    options_to_pass.append("-l\>\>\>(%request.size)%request\<\<\<(%response.size)%response")
    options_to_pass.append("-f")
    options_to_pass.append(pcap_file)
    options_to_pass.append("-e")
    options_to_pass.append(parser_script + ' -d "' + arguments+'"')
    options_to_pass.insert(0, "justniffer")

    result = subprocess.call(options_to_pass)
