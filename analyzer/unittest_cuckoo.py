__author__ = "zqzas"

import os, sys
sys.path.append('cuckoo')
import unittest

from malware_analyzer import MalwareAnalyzer


class TestCuckooAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = MalwareAnalyzer()

    def test_binary(self):
        f_bin = open("testcases/binaries.txt", 'r')
        for line in f_bin:
            bin_path = os.getcwd() + '/testcases/' + line.strip()
            print 'Analyzing binary: %s' % (bin_path)
            result = self.analyzer.analyze(None, bin_path)
            assert(str(result).isdigit())
            


if __name__ == '__main__':
    unittest.main()




            

