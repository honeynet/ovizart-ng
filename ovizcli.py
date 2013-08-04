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
            if args.file is None and args.url is None:
                print "You need to specify --file and/or --url parameters"
                print "Usage: ovizcli.py -vt --file FILE --url URL"
                sys.exit(1)

            from analyzer.virustotal.vt_wrapper import VTWrapper
            print "Virustotal analyzing", '.' * 30
            analyzer = VTWrapper()
            if args.url:
                response.append(analyzer.analyzeUrl(args.url))

            if args.file:
                response.append(analyzer.analyzeBinary(args.file))

        if args.cuckoo:
            if args.file is None:
                print "You need to specify --file parameter"
                print "Usage: ovizcli.py -ck --file FILE"
                sys.exit(1)

            from analyzer.cuckoo.cuckoo_wrapper import CuckooWrapper
            print "Cuckoo analyzing", '.' * 30
            analyzer = CuckooWrapper()
            if args.file:
                response.append(str(analyzer.analyzeMalware(args.file)))

        if args.jsunpackn:
            if args.url is None:
                print "You need to specify --url parameter"
                print "Usage: ovizcli.py -js --url URL"
                sys.exit(1)

            from analyzer.jsunpack_n.jsunpackn_wrapper import JsunpacknWrapper
            print "Jsunpack-n analyzing", '.' * 30
            analyzer = JsunpacknWrapper()

            if args.url:
                response.append(analyzer.analyzeJs(args.url))

        print "\n\nResponse:"
        print response

if __name__ == "__main__":
    main(sys.argv[1:])
