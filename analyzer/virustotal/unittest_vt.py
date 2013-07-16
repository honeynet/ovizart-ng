__author__ = "zqzas"

import os, sys
import unittest

from vt_wrapper import *

'''Testing VirusTotal'''

class TestVTAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = VTWrapper()

    def test_url(self):
        urls = ["zqzas.com"]

        for url in urls:
            self.analyzer.analyzeUrl(url)

if __name__ == '__main__':
    unittest.main()




            


