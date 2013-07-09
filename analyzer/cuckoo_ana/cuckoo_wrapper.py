__author__ = "zqzas"

import sys
import json

try:
    from cuckoo.lib.cuckoo.core.database import Database
except ImportError:
    noCuckoo = True

sys.path.append("../../")
from conf import Config

try:
    import requests
except ImportError:
    print "Please check your python-requests!"

class CuckooWrapper:
    """ Use cuckoo sandbox to analyze """

    def __init__(self):
        self.config = Config()

    def __repr__(self):
        print "A Cuckoo Sandbox Wrapper"

    def analyzeMalware(self, path, islocal = False):
        """
        Analyze malware.
        @param path     : the path of binary
        @return         : a task id
        """
        if islocal:
            self.db = Database()
            taskID = self.db.add_path(path)
            return taskID

        cuckoo_remote_ip = self.config.cuckoo_ip
        cuckoo_remote_port = self.config.cuckoo_port

        srv = "http://%s:%d" % (cuckoo_remote_ip, cuckoo_remote_port)

        binary = {'file': ('binary.exe', open(path, 'rb'))}

        r = requests.post(srv + "/tasks/create/file" , files = binary).text

        print r

        dict_json = json.loads(r)
        try:
            task_id = dict_json['task_id']
        except:
            raise Exception("Create task error when sending to remote cuckoo!")

        print "You may check the reports at: ( %s/tasks/report/%d/html ) after it's available." % (srv, task_id)

        return task_id








        


