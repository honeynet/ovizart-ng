"""Custom Exception classes"""

__author__ = 'ggercek'

class MissingMethodException(Exception):
    """Exception for missing method definitions"""

    def __init__(self, methodName, cls):
        """
        @param methodName   : missing method name
        @param cls          : missing methods class
        @return
        """
        self.methodName = methodName
        self.cls = cls

    def __str__(self):
        return "\"%s\" method is missing on class definition \"%s\"" %(self.methodName, self.cls)


class MissingArgumentException(Exception):
    """Exception for missing argument definitions"""

    def __init__(self, argName, methodName, cls):
        """
        @param argName      : missing argument name
        @param methodName   : missing arguments method
        @param cls          : missing methods class
        @return
        """
        self.argName = argName
        self.methodName = methodName
        self.cls = cls

    def __str__(self):
        return "method %s(%s) is missing on class definition \"%s\"" % (self.methodName, self.argName, self.cls)
