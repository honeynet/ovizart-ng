#!/usr/bin/env python

__author__ = 'ggercek'

from base_reassembler import BaseReassembler
import os
import ovizutil

class HTTPReassembler(BaseReassembler):
    target = 'HTTP'

    def __init__(self, outputFolder):
        BaseReassembler.__init__(self, outputFolder)
        self.requestedFileName = None

    def processRequest(self, request):
        BaseReassembler.processRequest(self, request)
        data = request[-1]
        if data.startswith('GET') or data.startswith('POST'):
            self.requestedFileName = data.split(' ')[1]

    def processResponse(self, response):
        BaseReassembler.processResponse(self, response)
        contentType = 'plain/text'
        data = response[-1]
        if data.startswith('HTTP'):
            responseCode = data.split(' ')[1]
            if responseCode == "200":
                _resp = data.split('\r\n\r\n')
                # responseHeader = _resp[0].split('\r\n')
                # for header in responseHeader:
                #     if header.startswith('Content-Type: '):
                #         contentType = header.split('Content-Type: ')

                fileContent = '\r\n\r\n'.join(_resp[1:])

                # save file
                #print 'filename: ', self.requestedFileName
                #print 'content size in bytes:', len(fileContent)
                self.saveFile(self.requestedFileName, fileContent)

                self.requestedFileName = None

    def saveFile(self, fileName, fileContent):

        outFile = os.path.join(self.outputFolder, 'attachments')
        ovizutil.createFolder(outFile)

        fileName = fileName.replace('/', '_')
        outFile = os.path.join(self.outputFolder, 'attachments', fileName)
        # TODO: Check file and rename if necessary
        fp = open(outFile, 'w')
        fp.write(fileContent)
        fp.flush()
        fp.close()