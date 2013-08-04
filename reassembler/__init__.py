__author__ = 'ggercek'

from ovizconf import PROJECT_ROOT
from base_reassembler import *
from smtp_reassembler import *
from http_reassembler import *
from core.tags import Tags

PCAP = Tags.DataSource.PCAP
BINARY = Tags.Attachment.BINARY
PLAIN_TEXT = Tags.Attachment.PLAIN_TEXT
JAVASCRIPT = Tags.Attachment.JAVASCRIPT

import os
import subprocess
import ovizutil

parsers = {
    BaseReassembler.target: 'BaseReassembler',
    SMTPReassembler.target: 'SMTPReassembler',
    HTTPReassembler.target: 'HTTPReassembler'
}

def run_reassembler(pcap_file, parser_class, output_folder):
    parser_script = PROJECT_ROOT + "reassembler/base_reassembler.py"
    #print parser_script
    pcap_file = os.path.abspath(pcap_file)
    parser_script = os.path.abspath(parser_script)
    output_folder = os.path.abspath(output_folder)

    arguments = parser_class + "|" + output_folder
    options_to_pass = list()
    options_to_pass.append("-l\>\>\>(%request.size)%request\<\<\<(%response.size)%response")
    options_to_pass.append("-f")
    options_to_pass.append(pcap_file)
    options_to_pass.append("-e")
    options_to_pass.append(parser_script + ' "' + arguments+'"')
    options_to_pass.insert(0, "justniffer")

    result = subprocess.call(options_to_pass)


@Reassembler(tags=PCAP)
class Reassembler():

    def process(self, data):
        stream = data.getStream()
        pcap_file = stream.pcapFileName
        protocol = data.getApplicationLayerProtocol()
        if protocol in parsers:
            parser_class = parsers[protocol]
        else:
            parser_class = 'BaseReassembler'

        output_folder = stream.outputFolder

        run_reassembler(pcap_file, parser_class, output_folder)
        # Check for attachment folder and add tags for those
        attachmentPath = data.getAttachmentsFolder() #os.path.join(output_folder, 'attachments')
        if os.path.exists(attachmentPath):
            # Get the list of file
            attachments = []
            filenames = [f for f in os.listdir(attachmentPath)]
            for f in filenames:
                ftype = ovizutil.checkFileType(os.path.join(attachmentPath, f))
                ftypeTag = None

                if ftype.endswith('binary'):
                    ftypeTag = BINARY
                elif ftype.startswith('text'):
                    if f.endswith('.js'):
                        ftypeTag = JAVASCRIPT
                    else:
                        ftypeTag = PLAIN_TEXT

                files = data.tag(ftypeTag)
                if files is None:
                    data.tag(ftypeTag, [f])
                else:
                    files.append(f)

                attachments.append((f, ftype, ftypeTag))

            data.setAttachments(attachments)
