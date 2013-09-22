#!/usr/bin/env python
__author__ = 'ggercek'

import sys
import argparse
from ovizart import Ovizart
from core.tags import Tags
from reporter.html_reporter import HTMLReporter
from ovizconf import PROJECT_ROOT

PCAP = Tags.DataSource.PCAP
BINARY = Tags.DataSource.BINARY
URL = Tags.DataSource.URL
PLAINTEXT = Tags.DataSource.PLAINTEXT


def checkInputValue(inputValue):
    if inputValue:
        if inputValue.endswith('.exe'):
            return BINARY
        if inputValue.endswith('.pcap'):
            return PCAP
        else:
            # check for URL
            # django url validation regex:
            # found on stackoverflow.com
            # http://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
            import re
            regex = re.compile( r'^(?:http|ftp)s?://' # http:// or https://
                                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                                r'localhost|' #localhost...
                                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                                r'(?::\d+)?' # optional port
                                r'(?:/?|[/?]\S+)$', re.IGNORECASE)

            if regex.match(inputValue):
                return URL
            else:
                import ovizutil
                ftype = ovizutil.checkFileType(inputValue)
                if ftype.endswith('binary'):
                    return BINARY
                elif ftype.startswith('text'):
                    return PLAINTEXT

    #return None
    return PLAINTEXT


def cli_main(args):
    #print args

    parser = argparse.ArgumentParser(description="Ovizart CLI")
    parser.add_argument("-i",   "--input", required=True, nargs="+", type=str, help="input value may be URL, binary or "
                                                                                  "pcap file. You can specify multiple "
                                                                                  "input file.")
    parser.add_argument("-o",  "--output",         required=True,       help="path of output folder")
    #parser.add_argument("-c", "--config", action="store_true", help="config file")
    parser.add_argument("-l",  "--list-available", action="store_true", help="list available modules")
    parser.add_argument("-v",  "--version",        action="version",    help="print version", version="%(prog)s 0.1a")
    parser.add_argument("-vt", "--virus-total",    action="store_true", help="Using VirusTotal to analyze binary or url")
    parser.add_argument("-ck", "--cuckoo",         action="store_true", help="Using Cuckoo Sandbox to analyze binary")
    parser.add_argument("-js", "--jsunpackn",      action="store_true", help="Using Jsunpack-n to analyze url")
    parser.add_argument("-V", "--verbose", action="store_true", help="Verbose mode")

    args = parser.parse_args(args)

    # process input files
    inputFiles = {PCAP: [], BINARY: [], URL: [], PLAINTEXT: []}
    for inputFile in args.input:
        if args.verbose:
            print 'Start checking input type...'
        inputType = checkInputValue(inputFile)
        print 'name:', inputFile, 'type:', inputType

        if inputType:
            if not (inputType in inputFiles):
                inputFiles[inputType] = []
            inputFiles[inputType].append(inputFile)
        else:
            print 'invalid input file: ', inputFile

    ovizart = Ovizart()
    if args.verbose:
        print "Ovizart main module is loaded..."
    if args.list_available:
        ovizart.listAvailableModules()
        return

    if not inputFiles[PCAP] and not (args.virus_total or args.cuckoo or args.jsunpackn):
        print "Error: No pcap file given."
        if inputFiles[BINARY]:
            print "Please give a pcap file or use -vt or -ck option for binary files like these.", inputFiles[BINARY]
        if inputFiles[URL]:
            print "Please give a pcap file or use -vt or -js option for urls like these.", inputFiles[URL]
        return
        

    if inputFiles[PCAP]:
        if args.verbose:
            print "Start analyzing pcap..."

        if args.output is None:
            print "Error: output folder must be set for pcap processing"
            return
        # Use only pcap files
        for inputFile in inputFiles[PCAP]:
            ovizart.setInputFile(inputFile)

        ovizart.config.output_folder = args.output
        analysis = ovizart.start()
        print analysis

    # Wrappers
    response = []
    if args.verbose:
        if args.virus_total or args.cuckoo or args.jsunpackn:
            print "Entering external analyzer..."
    if args.virus_total:
        if not (inputFiles[BINARY] or inputFiles[URL] or inputFiles[PLAINTEXT]):
            print "Error: No Binary or URL given for virus-total wrapper to process"
            if inputFiles[PCAP]:
                print "Please remove -vt option to process pcap files.", inputFiles[PCAP]
            return
            
        from analyzer.virustotal.vt_wrapper import VTWrapper
        print "Virus-total analyzing", '.' * 30
        analyzer = VTWrapper()
        if inputFiles[URL]:
            print inputFiles[URL]
            response += [analyzer.analyzeUrl(url) for url in inputFiles[URL]]

        if inputFiles[BINARY]:
            response += [analyzer.analyzeBinary(binary) for binary in inputFiles[BINARY]]



    if args.cuckoo:
        if not inputFiles[BINARY]:
            print "Error: No Binary given for cuckoo wrapper to process"
            if inputFiles[PCAP]:
                print "Please remove -ck option to process pcap files.", inputFiles[PCAP]
            if inputFiles[URL]:
                print "Please remove -ck option to process urls, use -js or -vt options for urls.", inputFiles[URL]
            return
        from analyzer.cuckoo.cuckoo_wrapper import CuckooWrapper
        print "Cuckoo analyzing", '.' * 30
        analyzer = CuckooWrapper()
        response.append(str([analyzer.analyzeMalware(binary) for binary in inputFiles[BINARY]]))

    if args.jsunpackn:
        if not inputFiles[URL] and not inputFiles[PLAINTEXT]:
            print "Error: No urls given for jsunpack-n wrapper to process"
            if inputFiles[PCAP]:
                print "Please remove -js option to process pcap files.", inputFiles[PCAP]
            if inputFiles[BINARY]:
                print "Please remove -js option to process binary files.", inputFiles[PCAP]
            return

        from analyzer.jsunpack_n.jsunpackn_wrapper import JsunpacknWrapper
        print "Jsunpack-n analyzing", '.' * 30
        analyzer = JsunpacknWrapper()

        response += [analyzer.analyzeJs(url) for url in inputFiles[URL]]
        response += [analyzer.analyzeJs(text) for text in inputFiles[PLAINTEXT]]

    if args.verbose:
        print "Analysis is done."

    print "\n\nResponse:"
    print response

    for result in response:
        if (result == None or result == ''):
            continue
        import webbrowser
        print PROJECT_ROOT + 'reporter/report.html'
        rptr = HTMLReporter()
        if (result[0] == '{'):
            rptr.report(result)
        else:
            rptr.report({"results": result})

        webbrowser.open_new_tab('file://' + PROJECT_ROOT + 'reporter/report.html')
    
    if args.verbose:
        print "Bye."

if __name__ == "__main__":
    cli_main(sys.argv[1:])
