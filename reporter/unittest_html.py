__auther__ = "zqzas"

import os, sys
import unittest

from html_reporter import HTMLReporter

'''Testing HTML Reporter'''

class TestHTMLReporter(unittest.TestCase):
    def setUp(self):
        self.rptr = HTMLReporter()

    def test_1(self):
        data = '{"permalink": "https://www.virustotal.com/url/b618f0bfbd90176adfcbc2ee9854140f0739063d87807144e26283b0e44791f7/analysis/1370430938/", "url": "http://zqzas.com/", "response_code": 1, "scan_date": "2013-06-05 11:15:38", "scan_id": "b618f0bfbd90176adfcbc2ee9854140f0739063d87807144e26283b0e44791f7-1370430938", "verbose_msg": "Scan finished, scan information embedded in this object", "filescan_id": null, "positives": 0, "total": 39, "scans": {"CLEAN MX": {"detected": false, "result": "clean site"}, "MalwarePatrol": {"detected": false, "result": "clean site"}, "ZDB Zeus": {"detected": false, "result": "clean site"}, "K7AntiVirus": {"detected": false, "result": "clean site"}, "Quttera": {"detected": false, "result": "clean site"}, "Yandex Safebrowsing": {"detected": false, "result": "clean site"}, "MalwareDomainList": {"detected": false, "result": "clean site"}, "ZeusTracker": {"detected": false, "result": "clean site"}, "zvelo": {"detected": false, "result": "clean site"}, "Google Safebrowsing": {"detected": false, "result": "clean site"}, "Kaspersky": {"detected": false, "result": "unrated site"}, "BitDefender": {"detected": false, "result": "clean site"}, "Opera": {"detected": false, "result": "clean site"}, "G-Data": {"detected": false, "result": "clean site"}, "C-SIRT": {"detected": false, "result": "clean site"}, "CyberCrime": {"detected": false, "result": "unrated site"}, "Sucuri SiteCheck": {"detected": false, "result": "clean site"}, "VX Vault": {"detected": false, "result": "clean site"}, "ADMINUSLabs": {"detected": false, "result": "clean site"}, "SCUMWARE.org": {"detected": false, "result": "clean site"}, "Dr.Web": {"detected": false, "result": "clean site"}, "AlienVault": {"detected": false, "result": "clean site"}, "Sophos": {"detected": false, "result": "unrated site"}, "Malc0de Database": {"detected": false, "result": "clean site"}, "SpyEyeTracker": {"detected": false, "result": "clean site"}, "Phishtank": {"detected": false, "result": "clean site"}, "Avira": {"detected": false, "result": "clean site"}, "Antiy-AVL": {"detected": false, "result": "clean site"}, "Comodo Site Inspector": {"detected": false, "result": "clean site"}, "Malekal": {"detected": false, "result": "clean site"}, "ESET": {"detected": false, "result": "clean site"}, "SecureBrain": {"detected": false, "result": "unrated site"}, "Websense ThreatSeeker": {"detected": false, "result": "unrated site"}, "Netcraft": {"detected": false, "result": "clean site"}, "ParetoLogic": {"detected": false, "result": "clean site"}, "URLQuery": {"detected": false, "result": "unrated site"}, "Wepawet": {"detected": false, "result": "unrated site"}, "Fortinet": {"detected": false, "result": "unrated site"}, "Minotaur": {"detected": false, "result": "clean site"}}}'

        self.rptr.report(data)


if __name__ == '__main__':
    unittest.main()








