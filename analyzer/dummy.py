
__author__ = "ggercek"

from core.engine import Analyzer
from core.tags import Tags
from analyzer import BaseAnalyzer

# TODO: Revise this part. too long to use
IRC = Tags.Protocol.IRC

# For tags one may use array as well, both of them accepted.
@Analyzer(tags=IRC)
class MyAwesomeIRCAnalyzer(BaseAnalyzer):
    """Here is the awesome description of awesome irc analyzer..."""

    def __init__(self):
        BaseAnalyzer.__init__(self)
        print "I'm awesome"

    def __repr__(self):
        return "MyAwesomeIRCAnalyzer"

    def analyze(self, data):
        # Do some awesome stuff here
        pass