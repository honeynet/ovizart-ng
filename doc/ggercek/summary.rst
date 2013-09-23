.. _summary-gsoc2013:

************************************
Summary of GSOC 2013 (Gurcan GERCEK)
************************************

.. _summary:

Summary and Future Work
=======================

Here is the summary of my work;

* Ovizart Infrastructure (core.engine)
    I focused on infrastructure of Ovizart rather than analyzing
    capabilities. I tried to develop an easy to extend structure. In order
    to accomplished I used decorators.
    I think I managed it but as you said the documentation is poor. For
    example any class decorated as DataSource will automatically tag the
    generated data according to decorator's specified tag.

    **Submodules**: Evaluation engine, Decorators for DataSource, Tagger,
    Analyzer, Reporter and Reassembler,

* Ovizart.py;
    This is a public interface to use the functionality of the tool.

* DataSource: Pcap parser
    This module is responsible for handling of pcap files and
    extracting streams. A Stream can be defined as whole traffic
    between 2 hosts. Streams are identified by proto, IP1, [port1], IP2,
    [port2]. port info will be used where applicable. Also this module
    generates summary information about a pcap file. Splits the given pcap
    file based on extracted streams.

* Tagger: Packet based protocol detection
    By using Scapy and regular expression based signatures our tool
    support detection of HTTP, HTTPS, SSH, SOCKSv4, FTP and SMTP.

* Reassembler: Base Reassembler
    By using justniffer as based part we are able to reassemble the
    traffic and save into three files, which contain assembled traffic
    according to direction: A->B, B->A, A<->B
    This module also is able to extract transferred files in HTTP and
    SMTP and new ones can be added easily.

* DB Handling:
    Currently I didn't save the content of pcap file into DB. DB
    contains computed or collected data and tags about the analysis. And
    the users of the system.

* Built-in web server
    For the sake of portability and dependency I used BaseHTTPServer
    from Python's core classes. At first it was quite easy to use but it
    turns out using it was a bad idea. I spent some time to add features
    like, SSL/TSL Support(currently it will generate a self signed
    certificate if non exists), Cookie management, Upload file as
    multipart/form-data or application/octet-stream(which is better for
    client side). But it is working just fine and sufficient for our
    needs, which is a rest-api friendly webserver.

* REST API
    Using @API decorator will register the decorated method to the
    webserver and will be called by one of the web server's thread. It
    takes 3 arguments which are,
    method='GET', url='/^/analysis/(?P<analysisId>.+)$', isAuth=True
    method: is http method
    url: regular expression to match and parse the incoming request line
    isAuth: boolean value indicate the authentication check is must,
    authentication is check by using cookies. If the user does not have
    the authorization then decorated method not called. And the connection
    will be closed.

    Other than API class we have a ovizapi.py module which provides
    the collection of REST API functions such as; login(), upload(),
    start(), get_analysisList(), get_analysisDetails() all these functions
    provides a remote user/device to use daemon. In order to simplify REST
    API usage I also implement OvizartProxy. This class is responsible for
    abstracting the REST API usage, so that we can replace Ovizart
    interface in our command line tool with OvizartProxy in order to
    provide a remote connection capability to our tool. OvizartProxy is
    also used by Web UI currently under construction.

* WEB UI
    It has now basic capabilities of login/logout, list the analysis,
    retrieve stream based pcap file, download extracted files from stream,
    download unidirectional and birdirectional reassembled traffic
    belongs to current user. Forgot to mention that each analysis is
    belong to a user and can only be shown/used by that user. I'm planning
    to add features like sharing analysis with other users or as json
    dumps etc. but after the final deadline. In order to use OvizartProxy
    and Ovizart Users I implemented AuthenticationBackEnd for Django. I'm
    trying to make it as a separate tool so that one can put this UI on a
    DMZ or something and use his computer for analysis.

* Test Codes
    Mostly I try to write some test code as well but for testing and
    code examples.

I think this is all.

.. _futurework:

Feature Requests
================

For feature request;
 - feel free to open an issue on github
 - or send an email: gurcangercek@gmail.com
