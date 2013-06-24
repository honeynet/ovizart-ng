
__author__ = "ggercek"

import datetime


class Analysis:
    """Data class for holding general analysis information"""
    count = 0

    INIT = "INIT"
    ERROR = "ERROR"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"

    def __init__(self):
        self.id = Analysis.generateId()
        self.startTime = datetime.datetime.now()
        self.user = "<NoUserDefined>"
        self.config = None
        self.status = Analysis.INIT
        self.data = []
        self.summary = {}

    @staticmethod
    def generateId():
        Analysis.count += 1
        return Analysis.count


class Data():
    """ Basic data representation class """

    def __init__(self):
        self.__data = {}
        self.__tags = {}

    def data(self, key, val=None):
        """Add or replace a data value if val is defined otherwise
        Returns the data value from dictionary
        @param key: key value for requested data
        @return value of tag if dataKey exists,None otherwise
        """
        if val:
            # TODO: Find a better solution, bug possibility!
            return self.set(self.__data, key, val)
        else:
            return self.get(self.__data, key)

    def tag(self, key, val=None):
        """Add or replace a tag value if val is defined otherwise
        Returns the tag value from dictionary
        @param tagKey: key value for requested tag
        @return value of tag if tagKey exists, None otherwise
        """
        if val:
            # TODO: Find a better solution, bug possibility!
            return self.set(self.__tags, key, val)
        else:
            return self.get(self.__tags, key)

    def get(self, dict, key):
        """
        @protected returns the value from dictionary
        @param dict : dictionary
        @param key  : key value for requested info
        @return value if key exists, None otherwise
        """
        val = None
        try:
            val = dict[key]
        except KeyError:
            # TODO: We should log such events
            pass
        return val

    def set(self, dict, key, val):
        """
        @protected add or replace val on given dict with given key
        @param dict dictionary
        @param key key value
        @param val value
        @return old value if a value exists with given key, None otherwise
        """
        oldVal = self.get(dict, key)
        dict[key] = val
        return oldVal
