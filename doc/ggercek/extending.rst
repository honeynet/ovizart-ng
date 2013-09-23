.. _extending:

*****************
Extending Ovizart
*****************

If you have questions about how to do some stuff you want to add feel free to contact me (gurcangercek@gmail.com)

.. _extending-reassembler:

How to add new protocol reassembler?
====================================
Adding new ProtocolReassembler is quite simple. Here is an skeleton of ProtocolReassembler;::

    class MySuperProtocolReassembler(BaseReassembler):
        target = 'MySuperProtocol'

        def __init__(self, outputFolder):
            BaseReassembler.__init__(self, outputFolder)
            # Init some variable here, if you need

        def processRequest(self, request):
            # Make sure to call this line
            BaseReassembler.processRequest(self, request)
            # process request here !!!

        def processResponse(self, response):
            # Make sure to call this line
            BaseReassembler.processResponse(self, response)
            # process response here !!!

It is important to extend BaseReassembler and define ‘target’ class attribute. Any stream object contains the
‘MySuperProtocol‘ tag will be processed by this class’ instance. You can find full code for http reassembler
here: https://github.com/honeynet/ovizart-ng/blob/ovizart-ng-devel/reassembler/http_reassembler.py

Last step for adding, we need to register our ProtocolReassembler to reassembler/__init__.py by updating ‘parsers’
dictionary. I’ll add decorators for this structure later for simplicity. Here is the sample;::

    parsers = {
        BaseReassembler.target: 'BaseReassembler',
        SMTPReassembler.target: 'SMTPReassembler',
        HTTPReassembler.target: 'HTTPReassembler',
        # Register MySuperProtocolReassembler
        MySuperProtocolReassembler.target, 'MySuperProtocolReassembler'
    }

That would do the job...

.. _extending-tagger:

How to add new protocol tagger?
===============================
Let us add a tagger for SOCKSv4 protocol. The easiest signature to detect this protocol is signature of connection
request packet. http://en.wikipedia.org/wiki/SOCKS#SOCKS4 the packet is in the form of::

    version(1 byte) | commandCode(1 byte) | portNum (2 byte) | ipaddress (4 byte) | user ID String (x byte)\x00

According to this info lets create a subclass of scapy.packet.Packet class::

    class SOCKS4Connect(Packet):
        protocol = "SOCKSv4"
        name = "SOCKS v4 Connect"
        fields_desc = [ByteField("version", ""),
                       ByteField("cmd", ""),
                       ShortField("remote-port", ""),
                       IntField("remote-ip", ""),
                       StrField("username", "")]

        def mysummary(self):
            return self.sprintf("SOCKSv4 Connect(version:%SOCKS4Connect.version%, cmd:%SOCKS4Connect.cmd%, "
                                "remote-port:%SOCKS4Connect.remote-port%, remote-ip:%SOCKS4Connect.remote-ip%, "
                                "username: %SOCKS4Connect.username%)")

with fields_dec variable we are defining the fields of new class with order. For further detail you can check this entry:
http://gsoc2013.honeynet.org/2013/08/01/network-analyzer-project-updates-week-5/

Lets prepare regular expression which will be our signature.::

    b'^\x04\x01.{2}.{4}.*\x00$'

Last step is to register the signature to our system. just add our new signature to tagger/protocol/__init__.py with its class and that's it::

    tcp_signatures = [
        # ...
        # other signatures
        (b'^\x04\x01.{2}.{4}.*\x00$', SOCKS4Connect),
                ]


.. _extending-rest-api:

How to extend REST API?
=======================
Just write your function. Your function should have one parameter 'data' and decorate it with API class. You don't need
to specify isAuth=True because True is its default value. My suggestion is that put all rest api functions in ovizapi.py
would be easier to follow.::

    @API(method='GET', url=r"^/coolFunction/(?P<analysisId>.+)/(?P<streamId>.+)/?$", isAuth=True)
    def myCoolFunction(data):
        # ...
        analysisId = data['analysisId']
        streamId = data['streamId']

        # ...

