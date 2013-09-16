
__author__ = "ggercek"

from core.engine import Analyzer
from core.tags import Tags
from analyzer import BaseAnalyzer

# TODO: Revise this part. too long to use
IRC = Tags.Protocol.IRC

# For tags one may use array as well, both of them accepted.
@Analyzer(tags=IRC)
class MyAwesomeDynamicAnalyzer(BaseAnalyzer):
    """Here is the awesome description of awesome dynamic analyzer..."""

    def __init__(self):
        BaseAnalyzer.__init__(self)
        print "I'm a dynamic analyzer"

    def __repr__(self):
        return "MyAwesomeDynamicAnalyzer"

    def analyze(self, data):
        # Do some awesome stuff here
        pass
