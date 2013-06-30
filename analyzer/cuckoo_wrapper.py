__author__ = "zqzas"

from cuckoo.lib.cuckoo.core.database import Database

class CuckooWrapper:
    """ Use cuckoo sandbox to analyze """

    def __init__(self):
        self.db = Database()

    def __repr__(self):
        print "A Cuckoo Sandbox Wrapper"

    def analyzeMalware(self, path):
        """
        Analyze malware.
        @param path     : the path of binary
        @return         : a task id
        """
        taskID = self.db.add_path(path)
        

        return taskID

