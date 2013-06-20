"""Some shared utility functions"""

__author__ = "ggercek"


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
    oldVal = self.__get(dict, key)
    dict[key] = val
    return oldVal


def get_file_type(inputFiles):
    """
    @protected
    """
    result = {}
    if inputFiles:
        for inputFile in inputFiles:
            if inputFile.count('.') and (inputFile.rindex('.') != len(inputFile)-1):
                fileType = inputFile.split('.')[-1].strip().upper()
                # Only pcap supported now!!!
                result[inputFile] = fileType
            else:
                # TODO: Raise an error
                pass

    return result