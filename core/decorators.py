from core import register_data_source, register_tagger, register_analyzer, register_reporter
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


class GenericDecorator:
    """Generic Decorator class"""

    # method name to search
    methodName = None

    # register method callback
    registerMethod = None

    def __init__(self, tags):
        """
        Constructor
        @param tags may be single value or a list of values to match the analyzer with given data
        """
        self.tags = tags
        self.cls = None

    def __call__(self, cls):
        """ This method does invoked automatically.
            Instantiate cls first then register it with given target value
        """
        # Check for the analyze method!!!
        self.cls = cls
        checkMethod(self.cls, self.__class__.methodName)

        self.newAnalyzer = self.cls()
        self.__class__.registerMethod(self, self.newAnalyzer, self.tags)


class DataSource(GenericDecorator):
    """Decorator for data source classes"""

    methodName = 'parse'
    registerMethod = register_data_source


class Tagger(GenericDecorator):
    """Decorator for tagger classes"""

    methodName = 'tag'
    registerMethod = register_tagger


class Analyzer(GenericDecorator):
    """Decorator for analyzer classes"""

    methodName = 'analyze'
    registerMethod = register_analyzer


class ReporterSource(GenericDecorator):
    """Decorator for reporter classes"""

    methodName = 'report'
    registerMethod = register_reporter
