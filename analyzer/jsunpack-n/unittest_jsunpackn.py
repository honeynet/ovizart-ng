__author__ = "zqzas"

import os, sys
import unittest

from jsunpackn_wrapper import *

class TestCuckooAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = JsunpacknWrapper()

    def test_binary(self):
        f_url = open("testcases/urls.txt", 'r')
        for line in f_url:
            url = line.strip()
            print 'Analyzing js from url: %s' % (url)
            result = self.analyzer.analyzeJs(url)
            print '-' * 30


if __name__ == '__main__':
    unittest.main()




            

