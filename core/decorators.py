class Analyzer:
    """Decorator for analyzer classes"""

    def __init__(self, target):
        """
        Constructor for decorator
        @param target may be single value or a list of values to match the analyzer with given data
        """
        # TODO: This part needs to revise, need to specify the parameters.
        self.target = target
        print "Analyzer -- init"

    def __call__(self, analyzer):
        """ This method does invoked automatically.
            Instantiate analyzer first then register it with given target value
        """
        newAnalyzer = analyzer()
        # TODO: register this analyzer with given target
        print "Analyzer -- call"