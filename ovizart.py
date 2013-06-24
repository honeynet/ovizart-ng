"""Ovizart interface definition"""

__author__ = "ggercek"


from core.engine import *
from datasource import *
from reporter import *
from tagger import *
from analyzer import *


class Ovizart():
    """
    Main class to define usage interface
    """

    def __init__(self, config):
        self.config = config

    def updateConfig(self, key, value):
        """Updates a config property"""
        pass

    def setConfig(self, config):
        """Overwrites config"""
        result = False
        if config:
            self.config = config
            result = True
        return result

    def setInputFile(self, inputFile):
        """Sets the input file name
        this method is used for local files or after the upload process
        """
        self.inputFile = inputFile

    def uploadFile(self, file):
        """Uploads the remote file to the server then sets the filename"""
        # TODO: upload file and return the filename. Should be this part handled by built-in web server ?!
        filename = ""
        # filename = upload(file)
        self.setInputFile(filename)

    def start(self):
        # TODO: Should be this function async or sync?
        # May be we should return some kind of handler/id for the analyze process
        pass

    def stop(self, analysisId):
        """Cancels a RUNNING analyze
        """
        pass

    def getStatus(self, analysisId):
        """Returns status of analyze as RUNNING, CANCELED, FINISHED, ERROR
        """
        pass

    def getReport(self, analysisId):
        """Returns the analyze report
        """
        pass

    def listAvailableModules(self):
        """Prints available modules in a human readable way.
        """
        list_available_modules()


if __name__ == '__main__':
    config = {}
    ovizart = Ovizart(config)
    ovizart.listAvailableModules()
    