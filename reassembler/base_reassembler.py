#!/usr/bin/env python
import sys
import os

def addToPath(pathToAdd):
    PROJECT_ROOT = os.path.abspath(__file__)
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
    pathToAdd = os.path.join(PROJECT_ROOT, pathToAdd)
    sys.path.append(pathToAdd)

addToPath("../")
#addToPath('reassembler')


import reassembler

__author__ = 'ggercek'


class BaseReassembler():
    target = 'UNKNOWN'
    requestFile = 'request.traffic'
    responseFile = 'response.traffic'
    totalFile = 'total.traffic'

    def __init__(self, outputFolder):
        self.outputFolder = outputFolder

    def __appendToFile(self, filename, data):
        filename = os.path.join(self.outputFolder, filename)
        f = open(filename, 'ab')
        f.write(data)
        f.write('\n\r')
        f.flush()
        f.close()

    def process(self, _in):
        size = 0
        request = self.parseMessage(_in)
        #print request[0], ' -- ', request[1], '###' #, request[2]
        self.processRequest(request)

        response = self.parseMessage(_in)
        self.processResponse(response)
        #print response[0], ' -- ', response[1], ' ### ' #, response[2]

    def processRequest(self, request):
        self.__appendToFile(BaseReassembler.requestFile, request[2])
        self.__appendToFile(BaseReassembler.totalFile, request[2])

    def processResponse(self, response):
        self.__appendToFile(BaseReassembler.responseFile, response[2])
        self.__appendToFile(BaseReassembler.totalFile, response[2])

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
    #print parser_name

    def getReassemblerbyName(name):
        c = getattr(reassembler, name)
        #print 'c:', c
        return c

    ParserClass = getReassemblerbyName(parser_name)

    if not ParserClass:
        # Use generic reassembler and store it to folder as session
        ParserClass = BaseReassembler

    res = ParserClass(outputFolder)
    res.process(sys.stdin)