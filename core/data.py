from ovizutil import set, get


class Data():
    """ Basic data representation class """

    def __init__(self):
        self.__data = {}
        self.__tags = {}

    def data(self, key, val):
        """Add or replace a data value"""
        set(self.__data, key, val)

    def data(self, dataKey):
        """
        Returns the data value from dictionary
        @param dataKey: key value for requested tag
        @return value of tag if dataKey exists,None otherwise
        """
        return get(self.__data, dataKey)

    def tag(self, key, val):
        """Add or replace a tag value"""
        set(self.__tags, key, val)

    def tag(self, tagKey):
        """
        Returns the tag value from dictionary
        @param tagKey: key value for requested tag
        @return value of tag if tagKey exists, None otherwise
        """
        return get(self.__tag, tagKey)

