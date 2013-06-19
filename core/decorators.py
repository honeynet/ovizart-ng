from core import register_analyzer
from core import MissingMethodException
import inspect


class Analyzer:
    """Decorator for analyzer classes"""

    methodName = 'analyze'

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
        methodName = Analyzer.methodName

        # Check for the analyze method!!!
        members = inspect.getmembers(analyzer)
        if not filter(lambda x: x[0] == methodName, members):
            raise MissingMethodException(methodName, analyzer)

        self.newAnalyzer = analyzer()
        register_analyzer(self.newAnalyzer, self.target)
        # TODO: register this analyzer with given target
        print "Analyzer -- call"