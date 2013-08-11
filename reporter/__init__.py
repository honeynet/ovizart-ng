# Import inner modules

__author__ = "zqzas"

class BaseReporter:
    """Base Reporter"""

    def __init__(self):
        self.conf = None

    def setConfig(self, config):
        self.conf = config

import html
