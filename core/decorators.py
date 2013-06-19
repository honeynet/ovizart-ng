from core import register_analyzer
from core import MissingMethodException
import inspect


def checkMethod(cls, methodName):
    """
    @private checks given class for given method name
    @param cls          : class to check
    @param methodName   : methodName to control
    @raise MissingMethodException if searched methodName does not exists in cls
    @return
    """
    members = inspect.getmembers(cls)
    if not filter(lambda x: x[0] == methodName, members):
        raise MissingMethodException(methodName, cls)


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

    def __call__(self, analyzer):
        """ This method does invoked automatically.
            Instantiate analyzer first then register it with given target value
        """
        # Check for the analyze method!!!
        checkMethod(analyzer, Analyzer.methodName)

        self.newAnalyzer = analyzer()
        register_analyzer(self.newAnalyzer, self.target)
