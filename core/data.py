
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
        self.id = Analysis.__generateId()
        self.startTime = datetime.datetime.now()
        self.user = "<NoUserDefined>"
        self.config = None
        self.status = Analysis.INIT
        self.data = []
        self.files = []

    @staticmethod
    def __generateId():
        Analysis.count += 1
        return Analysis.count

    def __repr__(self):
        s = 'Analysis Object{\n\tid: %d\n\tstartTime: %s\n\tuser: %s' \
            '\n\tconfig: %s\n\tstatus: %s\n\tdata: %s\n\tfiles: %s\n}' % \
            (self.id, str(self.startTime), self.user, self.config, self.status,self.data, self.files)
        return s


class Data():
    """ Basic data representation class """

    STREAM = 'stream'
    DATA_SOURCE = 'data_source'
    APP_LAYER_PROTOCOL = 'app_layer_protocol'

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
            return self.__set(self.__data, key, val)
        else:
            return self.__get(self.__data, key)

    def tag(self, key, val=None):
        """Add or replace a tag value if val is defined otherwise
        Returns the tag value from dictionary
        @param tagKey: key value for requested tag
        @return value of tag if tagKey exists, None otherwise
        """
        if val:
            # TODO: Find a better solution, bug possibility!
            return self.__set(self.__tags, key, val)
        else:
            return self.__get(self.__tags, key)

    def __repr__(self):
        s = "Data Object{\n\t\ttags: %s\n\t\tdata: %s\n\t}" % (self.__tags, self.__data)
        return s

    def __get(self, dict, key):
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

    def __set(self, dict, key, val):
        """
        @protected add or replace val on given dict with given key
        @param dict dictionary
        @param key key value
        @param val value
        @return old value if a value exists with given key, None otherwise
        """
        oldVal = self.__get(dict, key)
        dict[key] = val
        return oldVal

    def setStream(self, stream):
        return self.data(Data.STREAM, stream)

    def getStream(self):
        return self.data(Data.STREAM)

    def setDataSource(self, dataSource):
        return self.tag(Data.DATA_SOURCE, dataSource)

    def getDataSource(self):
        return self.tag(Data.DATA_SOURCE)

    def setApplicationLayerProtocol(self, protocol):
        return self.tag(Data.APP_LAYER_PROTOCOL, protocol)

    def getApplicationLayerProtocol(self):
        return self.tag(Data.APP_LAYER_PROTOCOL)