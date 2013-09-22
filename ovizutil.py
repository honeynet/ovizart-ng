__author__ = 'ggercek'

import datetime


def createFolder(outputFolder):
    # TODO: make this cross platform or convert it to python-only portable code
    import subprocess
    subprocess.check_output(['mkdir', '-p', outputFolder])


def checkFileType(filename):
    # TODO: replace this approach with mimetypes
    import os
    f = os.popen('file -bi ' + filename, 'r')
    return f.read().strip()


def getTimestampStr():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')