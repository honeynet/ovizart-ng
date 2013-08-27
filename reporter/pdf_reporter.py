"""
PDF reporter
"""

__author__ = "zqzas"

import sys
sys.path.append("..")

from core.engine import Reporter
from core.tags import Tags
from reporter import BaseReporter

from html_reporter import HTMLReporter
from xhtml2pdf import pisa


PDF = Tags.Reporter.PDF

@Reporter(tags=PDF)
class PDFReporter(BaseReporter):
    """Report HTML"""

    def __init___(self):
        BaseAnalyzer.__init__(self)
        

    def __repr__(self):
        return "PDF Reporter"

    def report(self, data, output_path = ''):
        """
        Generate PDF
        @param results: results dict
        
        """
        self.htmlreporter = HTMLReporter()

        sourceHtml = self.htmlreporter.report(data)

        if output_path != '':
            output_path += '/'

        outputFilename = output_path + "report.pdf"

        resultFile = open(outputFilename, "w+b")

        # convert HTML to PDF
        pisaStatus = pisa.CreatePDF(
                sourceHtml,                # the HTML to convert
                dest=resultFile)           # file handle to recieve result

        # close output file
        resultFile.close()                 # close output file

        # return True on success and False on errors
        return pisaStatus.err
            




if __name__ == "__main__":
    rpt = PDFReporter()
    rpt.report({"hello": "zqzas", "13123":"131231231"})








        



        








        




