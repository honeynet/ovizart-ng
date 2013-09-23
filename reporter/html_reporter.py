"""
HTML reporter
"""

__author__ = "zqzas"

import sys, os
sys.path.append("..")
REPORTER_ROOT = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.append(REPORTER_ROOT)

from core.engine import Reporter
from core.data import Data
from core.tags import Tags
from reporter import BaseReporter

import json


HTML = Tags.Reporter.HTML

try:
    from jinja2 import Environment, FileSystemLoader
    HAVE_JINJA2 = True
except ImportError:
    HAVE_JINJA2 = False

@Reporter(tags=HTML)
class HTMLReporter(BaseReporter):
    """Report HTML"""

    def __init___(self):
        BaseAnalyzer.__init__(self)

    def __repr__(self):
        return "HTML Reporter"

    def report(self, data, output_path = ''):
        """
        Generate HTML
        @param results: results dict
        @param output_path: optional
        
        """

        if not HAVE_JINJA2:
            raise Exception("Failed to report HTML: Jinja2 Python Library is missing.")

        #report path
        results = data

         #debug
        print results

        
        if type(results) is str:
            try:
                results = json.loads(results)
            except ValueError:
                raise ValueError("No JSON object could be decoded; This method accepts json string or dict.")

        if isinstance(results, Data):
            results = results.getDict()

       
        env = Environment(autoescape=True, loader = FileSystemLoader(REPORTER_ROOT))
        try:
            tpl = env.get_template("report_template.html")
            html = tpl.render({"results" : results})
        except Exception as e:
            raise Exception("HTML generation failed: %s" % e)

        if (output_path != ''):
            output_path += '/'

        try:
            report = open(REPORTER_ROOT + "report.html", "w")
            report.write(html)
            report.close()
        except (TypeError, IOError) as e:
            raise Exception("HTML write failed: %s" % e)

        return html


if __name__ == "__main__":
    rpt = HTMLReporter()
    #rpt.report({"hello": "zqzas", "13123":"131231231"})
    rpt.report("""[['{"permalink": "https://www.virustotal.com/url/11cbf5999b31feeb6a28fa3be00c89658d154bec65b26850f188ed8915da68d4/analysis/1378467371/", "url": "http://qq.com/", "response_code": 1, "scan_date": "2013-09-06 11:36:11", "scan_id": "11cbf5999b31feeb6a28fa3be00c89658d154bec65b26850f188ed8915da68d4-1378467371", "verbose_msg": "Scan finished, scan information embedded in this object", "filescan_id": null, "positives": 0, "total": 39, "scans": {"CLEAN MX": {"detected": false, "result": "clean site"}, "MalwarePatrol": {"detected": false, "result": "clean site"}, "ZDB Zeus": {"detected": false, "result": "clean site"}, "K7AntiVirus": {"detected": false, "result": "clean site"}, "Quttera": {"detected": false, "result": "suspicious site"}, "Yandex Safebrowsing": {"detected": false, "result": "clean site"}, "MalwareDomainList": {"detected": false, "result": "clean site"}, "ZeusTracker": {"detected": false, "result": "clean site"}, "zvelo": {"detected": false, "result": "clean site"}, "Google Safebrowsing": {"detected": false, "result": "clean site"}, "Kaspersky": {"detected": false, "result": "clean site"}, "BitDefender": {"detected": false, "result": "clean site"}, "Opera": {"detected": false, "result": "clean site"}, "G-Data": {"detected": false, "result": "clean site"}, "C-SIRT": {"detected": false, "result": "clean site"}, "CyberCrime": {"detected": false, "result": "unrated site"}, "Sucuri SiteCheck": {"detected": false, "result": "clean site"}, "VX Vault": {"detected": false, "result": "clean site"}, "ADMINUSLabs": {"detected": false, "result": "clean site"}, "SCUMWARE.org": {"detected": false, "result": "clean site"}, "Dr.Web": {"detected": false, "result": "clean site"}, "AlienVault": {"detected": false, "result": "clean site"}, "Sophos": {"detected": false, "result": "unrated site"}, "Malc0de Database": {"detected": false, "result": "clean site"}, "SpyEyeTracker": {"detected": false, "result": "clean site"}, "Phishtank": {"detected": false, "result": "clean site"}, "Avira": {"detected": false, "result": "clean site"}, "Antiy-AVL": {"detected": false, "result": "clean site"}, "Comodo Site Inspector": {"detected": false, "result": "clean site"}, "Malekal": {"detected": false, "result": "clean site"}, "ESET": {"detected": false, "result": "clean site"}, "SecureBrain": {"detected": false, "result": "unrated site"}, "Websense ThreatSeeker": {"detected": false, "result": "clean site"}, "Netcraft": {"detected": false, "result": "unrated site"}, "ParetoLogic": {"detected": false, "result": "clean site"}, "URLQuery": {"detected": false, "result": "unrated site"}, "Wepawet": {"detected": false, "result": "clean site", "detail": null}, "Fortinet": {"detected": false, "result": "unrated site"}, "Minotaur": {"detected": false, "result": "clean site"}}}']]""")







        



        








        




