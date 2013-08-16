"""
HTML reporter
"""

__author__ = "zqzas"

import sys
sys.path.append("..")

from core.engine import Reporter
from core.tags import Tags
from reporter import BaseReporter

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

        if type(results) is str:
            try:
                results = json.loads(results)
            except ValueError:
                raise ValueError("No JSON object could be decoded; This method accepts json string or dict.")

        env = Environment(autoescape=True, loader = FileSystemLoader('.'))

        try:
            tpl = env.get_template("report_template.html")
            html = tpl.render({"results" : results})
        except Exception as e:
            raise Exception("HTML generation failed: %s" % e)

        if (output_path != ''):
            output_path += '/'

        try:
            report = open(output_path + "report.html", "w")
            report.write(html)
            report.close()
        except (TypeError, IOError) as e:
            raise Exception("HTML write failed: %s" % e)

        return html


'''
if __name__ == "__main__":
    rpt = HTMLReporter()
    rpt.report({"hello": "zqzas", "13123":"131231231"})
'''








        



        








        




