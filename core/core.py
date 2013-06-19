analyzers = {}
taggers = {}
reporters = {}
dataSources = {}

ANALYZER = "ANALYZER"
TAGGER = "TAGGER"
REPORTER = "REPORTER"
DATASOURCE = "DATASOURCE"

availableModules = {
    DATASOURCE: [],
    TAGGER:     [],
    ANALYZER:   [],
    REPORTER:   []
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
    def dump(title, elem) :
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


## EXCEPTION DEFINITIONS ##
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