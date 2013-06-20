"""Data class for holding general analysis information"""

__author__ = 'ggercek'

import datetime

INIT = "INIT"
ERROR = "ERROR"
RUNNING = "RUNNING"
FINISHED = "FINISHED"

count = 0


def generateId():
    global count
    count += 1
    return count


class Analysis:

    def __init__(self):
        self.id = generateId()
        self.startTime = datetime.datetime.now()
        self.user = "<NoUserDefined>"
        self.config = None
        self.status = INIT
        self.data = []
        self.summary = {}
