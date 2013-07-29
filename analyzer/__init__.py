# Import inner modules

__author__ = "ggercek"


class BaseAnalyzer:

    def __init__(self):
        self.conf = None

    def setConfig(self, config):
        self.conf = config

import p2p
import dummy
import cuckoo
import jsunpackn
import virustotal

