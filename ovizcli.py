#!/usr/bin/env python
__author__ = 'ggercek'

import sys
import argparse
from ovizart import Ovizart


def main(args):
    parser = argparse.ArgumentParser(description="Ovizart CLI")
    parser.add_argument("-i", "--input", nargs="+", type=str, help="path of pcap file")
    parser.add_argument("-o", "--output", help="path of output folder")
    parser.add_argument("-c", "--config", action="store_true", help="config file")
    parser.add_argument("-l", "--list-available", action="store_true", help="list available modules")
    parser.add_argument("-v", "--version", action="version", help="print version", version="%(prog)s 0.1a")
    parser.add_argument("-vt", "--virustotal", action="store_true", help = "Using VirusTotal to analyze binary, pcap or url")
    parser.add_argument("-ck", "--cuckoo", action = "store_true", help = "Using Cuckoo Sandbox to analyze binary")
    parser.add_argument("-js", "--jsunpackn", action = "store_true", help = "Using Jsunpack-n to analyze url")
    parser.add_argument('--url', type=str, help="Input an url to analyze")
    parser.add_argument("--file", help="Input a file (path) to analyze(binary, js or pcap)")

    args = parser.parse_args(args)

    ovizart = Ovizart()
    if args.list_available:
        ovizart.listAvailableModules()
    elif not (args.virustotal or args.cuckoo or args.jsunpackn):
        for inputFile in args.input:
            ovizart.setInputFile(inputFile)

        ovizart.config.output_folder = args.output
        analysis = ovizart.start()
        print analysis
    else:

        response = []
        if args.virustotal:
            from analyzer.virustotal.vt_wrapper import VTWrapper
            print "Virustotal analyzing", '.' * 30
            analyzer = VTWrapper()
            if args.url != None:
                response += analyzer.analyzeUrl(args.url)
            else:
                response += analyzer.analyzeBinary(args.file)

        if args.cuckoo:
            from analyzer.cuckoo.cuckoo_wrapper import CuckooWrapper
            print "Cuckoo analyzing", '.' * 30
            analyzer = CuckooWrapper()
            if args.file != None:
                response += str(analyzer.analyzeMalware(args.file))

        if args.jsunpackn:
            from analyzer.jsunpack_n.jsunpackn_wrapper import JsunpacknWrapper
            print "Jsunpack-n analyzing", '.' * 30
            analyzer = JsunpacknWrapper()

            if args.url != None:
                response += analyzer.analyzeJs(args.url)

        print response

if __name__ == "__main__":
    main(sys.argv[1:])