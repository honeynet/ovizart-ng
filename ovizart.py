"""Ovizart interface definition"""

__author__ = "ggercek"

import os
from core import *
from datasource import *
from reporter import *
from tagger import *
from analyzer import *

from conf import Config


class Ovizart():
    """
    Main class to define usage interface
    """

    def __init__(self):
        self.config = Config()
        self.analysis = {}

    def updateConfig(self, key, value):
        """Updates a config property"""
        self.config[key] = value
        pass

    def setConfig(self, config):
        """Overwrites config"""
        result = False
        if config and type(config) == Config:
            self.config = config
            result = True
        return result

    def setInputFile(self, inputFile):
        """Sets the input file name
        this method is used for local files or after the upload process
        """
        result = False
        if inputFile and inputFile not in self.config.input_files:
            inputFile = os.path.abspath(inputFile)
            self.config.input_files.append(inputFile)
            result = True
        return result

    def uploadFile(self, file):
        """Uploads the remote file to the server then sets the filename"""
        # TODO: upload file and return the filename. Should be this part handled by built-in web server ?!
        filename = ""
        # filename = upload(file)
        self.setInputFile(filename)

    def start(self):
        # TODO: Should be this function async or sync?
        # May be we should return some kind of handler/id for the analyze process
        # Currently sync!!!
        analysis = engine.evaluate(self.config)
        self.analysis[analysis.id] = analysis
        return analysis

    def stop(self, analysisId):
        """Cancels a RUNNING analyze
        """
        result = False
        if analysisId in self.analysis:
            result = engine.stop(analysisId)
        return result

    def getStatus(self, analysisId):
        """Returns status of analyze as RUNNING, CANCELED, FINISHED, ERROR
        """
        result = None
        if analysisId in self.analysis:
            result = self.analysis[analysisId].status

        return result

    def getReport(self, analysisId):
        """Returns the analyze report
        """
        pass

    def listAvailableModules(self):
        """Prints available modules in a human readable way.
        """
        engine.list_available_modules()


if __name__ == '__main__':
    ovizart = Ovizart()
    ovizart.listAvailableModules()
