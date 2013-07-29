#!/usr/bin/env python

__author__ = 'ggercek'

from base_reassembler import BaseReassembler
import email
from core.engine import Reassembler
from core.tags import Tags
import os

SMTP = Tags.Protocol.SMTP


#@Reassembler(tags=SMTP)
class SMTPReassembler(BaseReassembler):
    target = 'SMTP'

    def __init__(self, outputFolder):
        BaseReassembler.__init__(self, outputFolder)

    def processRequest(self, request):
        BaseReassembler.processRequest(self, request)
        data = request[-1]
        # look for FROM: statement and take the
        if data.startswith('From:'):
            # Email Body found
            msg = email.message_from_string(data)
            self.extractFiles(msg)

    def processResponse(self, response):
        BaseReassembler.processResponse(self, response)

    def extractFiles(self, msg):
        if type(msg) != str:
            #print 'msg:', msg
            fn = msg.get_filename()
            if fn:
                # write data content
                print 'file found: ', fn, 'content-type:', msg.get_content_type()
                import ovizutil
                outFile = os.path.join(self.outputFolder, 'attachments')
                ovizutil.createFolder(outFile)

                # # TODO: A recursive mkdir required, create a util function
                # print 'outputFolder:', self.outputFolder
                # import os
                # if not os.path.exists(self.outputFolder):
                #     os.mkdir(self.outputFolder)

                outFile = os.path.join(outFile, fn)
                with open(outFile, 'wb') as fp:
                    fp.write(msg.get_payload(decode=True))
                    fp.flush()
            else:
                # Look for payloads
                payload = msg.get_payload()
                for p in payload:
                    self.extractFiles(p)