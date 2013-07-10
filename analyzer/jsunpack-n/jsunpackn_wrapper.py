"""
Server side jsunpackn

"""

__author__ = "zqzas"

__jsunpackn__ = "jsunpack-n-read-only" #the jsunpack-n folder


import sys
sys.path.append(__jsunpackn__)
from hashlib import sha1
import datetime

try:
    import jsunpackn
except ImportError:
    print "Import Error. Please check your jsunpackn!"

class Options:
    def __init__(self):
        self.options =  {
                'timeout':30,
                'redoevaltime':1,
                'maxruntime':0,
                'urlfetch':'',
                'configfile':'options.config',
                'saveallfiles':True, # for pcaps?
                'saveallexes':False,
                'quiet':True,
                'verbose':True,
                'veryverbose':True,
                'graphfile':'',
                'debug':False,
                'active':True,
                'interface':'',
                'nojs':False,
                'log_ips':'./maliciousips.txt',
                'pre':'./pre.js',
                'post':'./post.js',
                'htmlparse':'./htmlparse.config',
                'fasteval':False,
                'proxy': '',
                'currentproxy': '',
                }

        self.tmpdir = '/tmp' # these temporary files are necessary for decoding, but you can use any path and they will be deleted afterwards
        self.logdir = self.outdir = '' # an empty storage filepath means no directory of output files will be created
        self.decoded = '' #NO decoding logfile, otherwise = self.outdir + '/decoded.log'
        for item in self.options:
            setattr(self, item, self.options[item])

        #Hard Encode for rules
        fin = open(__jsunpackn__ + '/rules', 'r')
        if fin:
            self.rules = fin.read()
            fin.close()
        fin = open(__jsunpackn__ + '/rules.ascii', 'r')
        if fin:
            self.rulesAscii = fin.read()
            fin.close()
        if self.options['htmlparse']:
            fin = open(__jsunpackn__ + '/' + self.options['htmlparse'], 'r')
            self.htmlparseconfig = fin.read()
            fin.close()





class JsunpacknWrapper:
    def __init__(self):
        pass
    def __repr__(self):
        print "A jsunpack-n wrapper"

    def analyzeJs(self, userdata):
        """
        Analyze Javascript.
        @param userdata : a js file or a URL that to be analyzed
        @return         : the report
        """

        HASH = sha1(str(datetime.datetime.now()) + userdata).hexdigest()

        options = Options()

        #According to the document and exampleimport.py of jsunpack-n

        root_of_tree = ''   # This can be empty but its sometimes useful to specify a filename here
        url_or_name = '/'    # This can also be empty but if you have the URL, you'd want to set that here
        prevRooturl = {}    # This can also be empty but if you want to decode something with more context its useful to keep state  
        js = jsunpackn.jsunpack(root_of_tree, [url_or_name, userdata, root_of_tree], options, prevRooturl)

        results = ''
        for url in [js.start]: #recursive
            print 'The key %s has the following output in recursive mode' % (url)
            results = js.rooturl[url].tostring('', True)[0] + '\n'
            print results
        print 'Note that none of the files are actually created since self.outdir is empty.'

        print 'Instead, you could go through each url and look at the decodings that it creates' 
        for url in js.rooturl:
            print 'Looking at key %s, has %d files and %d messages, that follow:' % (url, len(js.rooturl[url].files), len(js.rooturl[url].msg))
            for type, hash, data in js.rooturl[url].files:
                print 'file              type=%s, hash=%s, data=%d bytes' % (type, hash, len(data))
            for printable, impact, msg in js.rooturl[url].msg:
                print 'output message    printable=%d, impact=%d, msg=%s' % (printable, impact, msg)
        
if __name__ == "__main__":
    wrapper = JsunpacknWrapper()

    wrapper.analyzeJs('http://bing.com')

