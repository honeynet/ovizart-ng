
__author__ = "ggercek"

from outil import set, get


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
            return set(self.__data, key, val)
        else:
            return get(self.__data, key)

    def tag(self, key, val=None):
        """Add or replace a tag value if val is defined otherwise
        Returns the tag value from dictionary
        @param tagKey: key value for requested tag
        @return value of tag if tagKey exists, None otherwise
        """
        if val:
            # TODO: Find a better solution, bug possibility!
            return set(self.__tags, key, val)
        else:
            return get(self.__tags, key)
