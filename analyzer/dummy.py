from ovizart import Analyzer
from ovizart import Tags

# TODO: Revise this part. too long to use
IRC = Tags.Protocol.IRC

@Analyzer(target=IRC)
class MyAwesomeIRCAnalyzer:
    """Here is the awesome description of awesome irc analyzer..."""

    def __init__(self):
        print "I'm awesome"

    def __repr__(self):
        return "MyAwesomeIRCAnalyzer"

    def analyze(self):
        # Do some awesome stuff here
        pass