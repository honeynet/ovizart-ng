"""Some shared utility functions"""

__author__ = "ggercek"

def get(self, dict, key):
    """
    @private returns the value from dictionary
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
    @private add or replace val on given dict with given key
    @param dict dictionary
    @param key key value
    @param val value
    @return old value if a value exists with given key, None otherwise
    """
    oldVal = self.__get(dict, key)
    dict[key] = val
    return oldVal