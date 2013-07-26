"""
A CLI for analyzer wrappers

"""

__author__ = "zqzas"

import argparse
import sys
sys.path.append("cuckoo")
sys.path.append("jsunpack-n")
sys.path.append("virustotal")
sys.path.append("../")



def main():
    parser = argparse.ArgumentParser(description = "An CLI for analyzer wrappers.")

    parser.add_argument("-v", "--virustotal", action = "store_true", help = "Using VirusTotal to analyze binary or url")
    parser.add_argument("-c", "--cuckoo", action = "store_true", help = "Using Cuckoo Sandbox to analyze binary")

    parser.add_argument("-j", "--jsunpackn", action = "store_true", help = "Using Jsunpack-n to analyze url")
    
    parser.add_argument("-u" , "--url", help = "Input an url")

    parser.add_argument("-b", "--binary", help = "Input an binary (path)")

    args = parser.parse_args()

    if args.url == None and args.binary == None:
        print "You must input an url or binary(path)."
        print parser.print_help()
        return
        

    response = []
    if args.virustotal:
        from vt_wrapper import VTWrapper
        print "Virustotal analyzing", '.' * 30
        analyzer = VTWrapper()
        if args.url != None:
            response += analyzer.analyzeUrl(args.url)
        else:
            response += analyzer.analyzeBinary(args.binary)

    if args.cuckoo:
        from cuckoo_wrapper import CuckooWrapper
        print "Cuckoo analyzing", '.' * 30
        analyzer = CuckooWrapper()
        if args.binary != None:
            response += str(analyzer.analyzeMalware(args.binary))


    if args.jsunpackn:
        from jsunpackn_wrapper import JsunpacknWrapper
        print "Jsunpack-n analyzing", '.' * 30
        analyzer = JsunpacknWrapper()

        if args.url != None:
            response += analyzer.analyzeJs(args.url)

if __name__ == "__main__":
    main()
