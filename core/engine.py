from data import Analysis
import datetime
import ovizutil

__author__ = "ggercek"

_analysis = {}

analyzers = {}
taggers = {}
reassemblers = {}
reporters = {}
dataSources = {}

ANALYZER = "ANALYZER"
TAGGER = "TAGGER"
REASSEMBLER = "REASSEMBLER"
REPORTER = "REPORTER"
DATASOURCE = "DATASOURCE"

availableModules = {
    DATASOURCE:  [],
    TAGGER:      [],
    REASSEMBLER: [],
    ANALYZER:    [],
    REPORTER:    []
}


def __register(dict, newElem, tags):
    """
    @private
    Add given new element to dictionary based on given tags
    @param dict     : dictionary subject to addition
    @param newElem  : object (tagger/analyzer/reporter) to register
    @param tags     : tags to represent matching criteria
    @return
    """
    # TODO: This approach may be problematic what if there are multiple tags for the same data object.
    # No need to re-evaluate. Find a general solution...
    def add(newElem, tag):
        if tag not in dict:
            dict[tag] = []

        dict[tag].append(newElem)

    if not isinstance(tags, list):
        tags = [tags]

    for tag in tags:
        add(newElem, tag)


def register_data_source(decorator, dataSource, tags):
    """
    @protected This method should be called by decorators, no need to call this method explicitly
    Register data source according to given tags
    @param dataSource   : analyzer object to register
    @param tags         : tags to represent matching criteria
    @return
    """
    global dataSources, availableModules, DATASOURCE
    __register(dataSources, dataSource, tags)

    availableModules[DATASOURCE].append(dataSource)


def register_tagger(decorator, tagger, tags):
    """
    @protected This method should be called by decorators, no need to call this method explicitly
    Register tagger according to given tags
    @param tagger   : analyzer object to register
    @param tags     : tags to represent matching criteria
    @return
    """
    global taggers, availableModules, TAGGER
    __register(taggers, tagger, tags)

    availableModules[TAGGER].append(tagger)


def register_reassembler(decorator, reassembler, tags):
    """
    @protected This method should be called by decorators, no need to call this method explicitly
    Register analyzer according to given tags
    @param analyzer : analyzer object to register
    @param tags     : tags to represent matching criteria
    @return
    """
    global reassemblers, availableModules, REASSEMBLER
    __register(reassemblers, reassembler, tags)

    availableModules[REASSEMBLER].append(reassembler)

def register_analyzer(decorator, analyzer, tags):
    """
    @protected This method should be called by decorators, no need to call this method explicitly
    Register analyzer according to given tags
    @param analyzer : analyzer object to register
    @param tags     : tags to represent matching criteria
    @return
    """
    global analyzers, availableModules, ANALYZER
    __register(analyzers, analyzer, tags)

    availableModules[ANALYZER].append(analyzer)


def register_reporter(decorator, reporter, tags):
    """
    @protected This method should be called by decorators, no need to call this method explicitly
    Register reporter according to given tags
    @param reporter : reporter object to register
    @param tags     : tags to represent matching criteria
    @return
    """
    global analyzers, availableModules, REPORTER
    __register(reporters, reporter, tags)

    availableModules[REPORTER].append(reporter)


def list_available_modules():
    def dump(title, elem):
        print
        print "   %s: " % title

        if not elem:
            print "\t\tNo available modules!"
        else:
            for e in elem:
                print "\t- %s\n\t\t%s" % (e, e.__doc__)

    global availableModules
    print "#########################"
    print "LIST OF AVAILABLE MODULES"
    dump("DATASOURCE", availableModules[DATASOURCE])
    dump("TAGGER", availableModules[TAGGER])
    dump("ANALYZER", availableModules[ANALYZER])
    dump("REPORTER", availableModules[REPORTER])
    print "#########################"


def get_file_type(inputFiles):
    """
    @protected
    """
    result = {}
    if inputFiles:
        for inputFile in inputFiles:
            if inputFile.count('.') and (inputFile.rindex('.') != len(inputFile)-1):
                fileType = inputFile.split('.')[-1].strip().upper()
                # Only pcap supported now!!!
                result[inputFile] = fileType
            else:
                # TODO: Raise an error
                pass

    return result


def evaluate(config):
    global availableModules, dataSources, taggers, analyzers, reporters

    newAnalysis = Analysis()
    newAnalysis.config = config

    _analysis[newAnalysis.id] = newAnalysis

    # Read input file(s)
    inputFiles = config.input_files

    # Select parser based on extension
    inputFiles = get_file_type(inputFiles)

    # Filter analyzers
    # TODO: remove unwanted analyzers
    # filterAnalyzers based on config parameter config.exclude_analyzer=[]
    selectedAnalyzers = analyzers

    # Select reporter module
    # Currently only html is available
    selectedReporters = availableModules[REPORTER]

    analysisFolder = datetime.datetime.now().strftime('analysis_%Y%m%d_%H%M%S_%f')
    config.output_folder = config.output_folder + analysisFolder + "/"
    newAnalysis.status = Analysis.RUNNING
    for fileName in inputFiles.keys():
        fileType = inputFiles[fileName]
        # TODO: What if multiple parser exists?
        parser = dataSources[fileType][0]
        import os
        # create output folder
        outputFolder = config.output_folder + fileName.split("/")[-1]
        outputFolder = os.path.join(config.output_folder, fileName.split("/")[-1])
        ovizutil.createFolder(outputFolder)

        # Returns summary of pcap file with file names
        summary = parser.parse(fileName, outputFolder)
        # summary = {
        #               inputFile: {
        #                   filename: '',
        #                   numberOfPackets: '',
        #                   numberOfBytes: '',
        #                   startTime: '',
        #                   endTime: ''
        #               },
        #               flows: [
        #                   {}.
        #               ]
        # }
        newAnalysis.files.append(summary['inputFile'])
        # Select taggers based on file type
        selectedTaggers = []
        if fileType in taggers:
            selectedTaggers = taggers[fileType]

        flows = summary['data']
        # flow is an instance of data class
        for flow in flows:
            newAnalysis.data.append(flow)
            for tagger in selectedTaggers:
                tagger.tag(flow)

        reassembler = reassemblers[fileType][0]
        for flow in flows:
            reassembler.process(flow)

        for flow in flows:
            for tag in selectedAnalyzers.keys():
                for analyzer in selectedAnalyzers[tag]:
                    if flow.tag(tag):
                        analyzer.analyze(flow)

        for flow in flows:
            for tag, reporter in selectedReporters:
                reporter.report(flow)

    newAnalysis.status = Analysis.FINISHED
    return newAnalysis
################################
################################
### Custom Exception classes ###
################################
################################


class MissingMethodException(Exception):
    """Exception for missing method definitions"""

    def __init__(self, methodName, cls):
        """
        @param methodName   : missing method name
        @param cls          : missing methods class
        @return
        """
        self.methodName = methodName
        self.cls = cls

    def __str__(self):
        return "\"%s\" method is missing on class definition \"%s\"" %(self.methodName, self.cls)


class MissingArgumentException(Exception):
    """Exception for missing argument definitions"""

    def __init__(self, argName, methodName, cls):
        """
        @param argName      : missing argument name
        @param methodName   : missing arguments method
        @param cls          : missing methods class
        @return
        """
        self.argName = argName
        self.methodName = methodName
        self.cls = cls

    def __str__(self):
        return "method %s(%s) is missing on class definition \"%s\"" % (self.methodName, self.argName, self.cls)

#######################################
#######################################
### END OF Custom Exception classes ###
#######################################
#######################################

##################
### DECORATORS ###
##################
import inspect


class GenericDecorator:
    """Generic Decorator class"""

    # method name to search
    methodName = None

    # argument name to search
    argNames = None

    # register method callback
    registerMethod = None

    clsMethod = None
    newMethod = None

    def __init__(self, tags):
        """
        Constructor
        @param tags may be single value or a list of values to match the analyzer with given data
        """
        self.tags = tags
        self.cls = None

    def __call__(self, cls):
        """ This method does invoked automatically.
            Instantiate cls first then register it with given target value
        """
        # Check for the analyze method!!!
        self.cls = cls
        self.checkMethod(self.cls, self.__class__.methodName, self.__class__.argNames)

        self.newObject = self.cls()
        self.__class__.registerMethod(self, self.newObject, self.tags)
        return cls

    def checkMethod(self, cls, methodName, argNames):
        """
        @private checks given class for given method name
        @param cls          : class to check
        @param methodName   : methodName to control
        @param argNames      : list of arguments to control
        @raise MissingMethodException if searched methodName does not exists in cls
        @raise MissingArgumentException if searched method does not defined with parameter data
        @return
        """

        # check method
        members = inspect.getmembers(cls)
        methods = filter(lambda x: x[0] == methodName, members)
        if not methods:
            raise MissingMethodException(methodName, cls)

        # check methods argument
        found = False
        for m in methods:
            m = m[1]
            args = inspect.getargs(m.im_func.func_code).args
            # TODO: Refactor this control later.
            if args and len(args) == len(argNames) + 1 and args[1:] == argNames:
                found = True
                if self.__class__.newMethod:
                    self.__class__.clsMethod = m
                    cls.__dict__['decorator_tags'] = self.tags
                    # newMethod has to be a tuple otherwise it will throw an exception
                    cls.__dict__[methodName] = self.__class__.newMethod[0]
                break

        if not found:
            raise MissingArgumentException(argNames, methodName, cls)


class DataSource(GenericDecorator):
    """Decorator for data source classes"""

    methodName = 'parse'
    argNames = ['filename', 'outputFolder']
    registerMethod = register_data_source
    clsMethod = None

    def __init__(self, tags):
        GenericDecorator.__init__(self, tags)
        # TODO: Seems a bit weird find a soultion!!!
        # If we directly set self.parse to newMethod variable then it will throw an exception but with this approach
        # it is OK, no complain from python.
        self.__class__.newMethod = (self.parse, )

    # TODO: Find out why we must use a static function for this job
    @staticmethod
    def parse(cls, filename, outputFolder):
        summary = DataSource.clsMethod(cls, filename, outputFolder)
        for d in summary['data']:
            d.setDataSource(cls.decorator_tags)
        return summary


class Tagger(GenericDecorator):
    """Decorator for tagger classes"""

    methodName = 'tag'
    argNames = ['data']
    registerMethod = register_tagger


class Analyzer(GenericDecorator):
    """Decorator for analyzer classes"""

    methodName = 'analyze'
    argNames = ['data']
    registerMethod = register_analyzer


class Reporter(GenericDecorator):
    """Decorator for reporter classes"""

    methodName = 'report'
    argNames = ['data']
    registerMethod = register_reporter


class Reassembler(GenericDecorator):
    """Decorator for re-assembler classes"""
    methodName = 'process'
    argNames = ['data']
    registerMethod = register_reassembler

#########################
### END OF DECORATORS ###
#########################