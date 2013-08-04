"""Ovizart interface definition"""

__author__ = "ggercek"

import os
import sys
from ovizconf import Config, PROJECT_ROOT


def addToPath(pathToAdd):
    PROJECT_ROOT = os.path.abspath(__file__)
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
    pathToAdd = os.path.join(PROJECT_ROOT, pathToAdd)
    sys.path.append(pathToAdd)

addToPath("analyzer")
addToPath("core")
addToPath("datasource")
addToPath("reassembler")
addToPath("reporter")
addToPath("tagger")
addToPath("test")

from core import *
from datasource import *
from reporter import *
from tagger import *
from reassembler import *
from analyzer import *


class Ovizart():
    """
    Main class to define usage interface
    """

    def __init__(self, config=None):
        if config is None:
            config = Config()

        self.config = config
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
