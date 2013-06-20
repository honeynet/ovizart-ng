
__author__ = "ggercek"

from core import register_data_source, register_tagger, register_analyzer, register_reporter
from exceptions import MissingMethodException, MissingArgumentException
import inspect


def checkMethod(cls, methodName, argName):
    """
    @private checks given class for given method name
    @param cls          : class to check
    @param methodName   : methodName to control
    @raise MissingMethodException if searched methodName does not exists in cls
    @raise MissingArgumentException if searched method does not defined with parameter data
    @return
    """

    # check method
    members = inspect.getmembers(cls)
    methods = filter(lambda x: x[0] == methodName, members)
    if not methods:
        raise MissingMethodException(methodName, cls)

    # check methods argument
    found = False
    for m in methods:
        m = m[1]
        args = inspect.getargs(m.im_func.func_code).args
        # TODO: Refactor this control later.
        if args and len(args) == 2 and args[1] == argName:
            found = True
            break

    if not found:
        raise MissingArgumentException(argName, methodName, cls)


class GenericDecorator:
    """Generic Decorator class"""

    # method name to search
    methodName = None

    # argument name to search
    argName = None

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
        checkMethod(self.cls, self.__class__.methodName, self.__class__.argName)

        self.newAnalyzer = self.cls()
        self.__class__.registerMethod(self, self.newAnalyzer, self.tags)
        return cls

class DataSource(GenericDecorator):
    """Decorator for data source classes"""

    methodName = 'parse'
    argName = 'filename'
    registerMethod = register_data_source


class Tagger(GenericDecorator):
    """Decorator for tagger classes"""

    methodName = 'tag'
    argName = 'data'
    registerMethod = register_tagger


class Analyzer(GenericDecorator):
    """Decorator for analyzer classes"""

    methodName = 'analyze'
    argName = 'data'
    registerMethod = register_analyzer


class Reporter(GenericDecorator):
    """Decorator for reporter classes"""

    methodName = 'report'
    argName = 'data'
    registerMethod = register_reporter
