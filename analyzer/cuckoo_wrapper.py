__author__ = "zqzas"

import sys

from cuckoo.lib.cuckoo.core.database import Database
sys.path.append("../")
from conf import Config

try:
    import requests
except ImportError:
    print "Please check your python-requests!"

class CuckooWrapper:
    """ Use cuckoo sandbox to analyze """

    def __init__(self):
        self.db = Database()
        self.config = Config()

    def __repr__(self):
        print "A Cuckoo Sandbox Wrapper"

    def analyzeMalware(self, path, islocal = False):
        """
        Analyze malware.
        @param path     : the path of binary
        @return         : a task id
        """
        if isLocal:
            taskID = self.db.add_path(path)
            return taskID

        cuckoo_remote_ip = self.config.cuckoo_ip
        cuckoo_remote_port = self.config.cuckoo_port

        srv = "http://%s:%d/tasks/create/file" % (cuckoo_remote_ip, cuckoo_remote_port)

        binary = {'file': ('binary.exe', open(path, 'rb'))}

        r = requests.post(srv, files = binary)

        print r.text






        


