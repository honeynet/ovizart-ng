#!/usr/bin/env python
import sys

__author__ = 'ggercek'


class BaseReassembler():

    def __init__(self, outputFolder):
        self.outputFolder = outputFolder
        pass

    def process(self, _in):
        size = 0
        request = self.parseMessage(_in)
        print request[0], ' -- ', request[1], '###' #, request[2]
        self.processRequest(request)

        response = self.parseMessage(_in)
        self.processResponse(response)
        print response[0], ' -- ', response[1], ' ### ' #, response[2]

    def processRequest(self, request):
        pass

    def processResponse(self, response):
        pass

    def parseMessage(self, _in):
        dir = _in.read(6)
        sizeStr = ""
        while True:
            c = _in.read(1)
            if c == '(':
                continue

            if c == ')':
                size = int(sizeStr)
                break

            sizeStr += c

        if size > 0:
            data = _in.read(size)
        else:
            data = ""

        return dir, size, data


if __name__ == '__main__':
    arguments = sys.argv[-1].split('|')
    parser_name = arguments[0]
    outputFolder = arguments[1]
    print parser_name

    def getReassemblerbyName(name):
        import reassembler
        c = getattr(reassembler, name)
        print 'c:', c

        return c

    ParserClass = getReassemblerbyName(parser_name)

    if not ParserClass:
        # Use generic reassembler and store it to folder as session
        ParserClass = BaseReassembler
        pass

    res = ParserClass(outputFolder)
    res.process(sys.stdin)