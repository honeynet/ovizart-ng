.. _usage:

**************
Usage Examples
**************

Currently there are different possibilities to use ovizart-ng. You can access ovizart over its web ui or through
commandline interface. If you are looking for some interactivity you can use ovizart shell. In worst case scenario with
ipython you can instantiate an OvizartProxy object and can reach all features over an API. There is also Ovizart interface
you can use but that interface is used mainly internal issues. You have to be careful if you are going to use that interface.

In this document you will find usage examples of different interfaces. This document contains some of the features not all,
I strongly suggests you should play with OvizartProxy over ipython...

.. _ovizart-api:

Using OvizartProxy API
======================

OvizartProxy provides an abstraction layer to all Ovizart REST API features. You can develop your own frontend for
ovizart with OvizartProxy. It's functions can be listed as below

* **login(self, username, password)**: Logins the core system with given username and password
* **uploadFile(self, filename, fileobj=None)**: upload the given file tocore system
* **start(self)**: starts the analysis of uploaded files
* **getAnalysis(self, analysisId=None)**: requests analysis details of analysis if analysisId is given, otherwise requests all analysis summary information, which belongs to user
* **removeAnalysisById(self, analysisId)**: deletes analysis based on given analysisId
* **addAnalyzer(self, filename)**: uploads and registers the given analyzer code to core system
* **getPcap(self, analysisId, streamKey)**: downloads split pcap file belongs to given streamKey of given analysisId
* **getReassembled(self, analysisId, streamKey, trafficType)**: downloads reassembled application layer traffic file based on trafficType

  trafficType values::

    0: A  -> B contains request-only traffic
    1: A <-  B contains response-only traffic
    2: A <-> B contains total traffic


* **getAttachment(self, analysisId, streamKey, filePath)**: downloads extracted file by given filePath streamKey and analysisId parameters.

Here is a sample ipython session

.. sourcecode:: ipython

    In [1]: from core.ovizart_proxy import OvizartProxy

    In [2]: op = OvizartProxy('http', 'localhost', '9009')

    In [3]: op = OvizartProxy('https', 'localhost', '9009')

    In [4]: op.login('ovizart', '123456')
    Out[4]:
    {u'Status': u'OK',
     u'userid': u'5227e32268caca1a3c047374',
     u'username': u'ovizart'}

    In [5]: op.uploadFile('./test/pcap/test-http.pcap')
    Out[5]: {u'Filesize': 326754, u'Status': u'OK', u'filename': u'test-http.pcap'}

    In [6]: op.start()
    Out[6]: {u'AnalysisId': u'522a734968caca1103775079', u'Status': u'INIT'}

    In [7]: op.getAnalysis()
    Out[7]:
    [{u'_id': u'5227f5b968caca205d6fba93',
      u'files': [{u'filename': u'/home/ovizart/src/ovizart-ng/upload/smtp_2.pcap',
        u'numberOfPacket': 60,
        u'numberOfStreams': 4}],
      u'startTime': 1378350521.216652,
      u'status': u'FINISHED'},
     {u'_id': u'5227f5d468caca205d6fba94',
      u'files': [],
      u'startTime': 1378350548.074157,
      u'status': u'INIT'},
     {u'_id': u'522a734968caca1103775079',
      u'files': [{u'filename': u'/home/ovizart/src/ovizart-ng/upload/test-http.pcap',
        u'numberOfPacket': 483,
        u'numberOfStreams': 21}],
      u'startTime': 1378513737.705265,
      u'status': u'FINISHED'}]

    In [8]: op.getAnalysis('522a734968caca1103775079')
    Out[8]:
    {u'_id': u'522a734968caca1103775079',
     u'config': {u'cuckoo_html_enabled': True,
      u'cuckoo_ip': u'81.167.148.242',
      u'cuckoo_port': 8090,
      u'cuckoo_tcpdump_enabled': True,
      u'cuckoo_timeout': 60,
      u'exclude_analyzer': [],
      u'input_files': [u'/home/ovizart/src/ovizart-ng/upload/test-http.pcap'],
      u'is_cuckoo_available': True,
      u'jsunpackn_path': u'',
      u'output_folder': u'/home/ovizart/src/ovizart-ng/test/output/analysis_20130907_032857_706265/',
      u'vt_apikey': u'545b985a35ca91e6bd5232c9cfb3549dd5e74a506ea960336472f86be156ec8d'},
     u'data': [{u'_Data__data': {u'stream': {u'dstIp': u'10.1.1.1',
         u'dstPort': u'80',
         u'fileHandler': None,
         u'key': u'6_10.1.1.101_3188_10.1.1.1_80',
         u'last_ts': 1100903355.562335,
         u'outputFolder': u'/home/ovizart/src/ovizart-ng/test/output/analysis_20130907_032857_706265/test-http.pcap/6_10.1.1.101_3188_10.1.1.1_80',
         u'pcapFile': None,
         u'pcapFileName': u'/home/ovizart/src/ovizart-ng/test/output/analysis_20130907_032857_706265/test-http.pcap/6_10.1.1.101_3188_10.1.1.1_80/6_10.1.1.101_3188_10.1.1.1_80.pcap',
         u'pktCount': 14,
         u'protocol': 6,
         u'srcIP': u'10.1.1.101',
         u'srcPort': u'3188',
         u'startTime': u'1100903355.43'}},
       u'_Data__tags': {u'PLAIN_TEXT': [u'_Websidan_index.html'],
        u'app_layer_protocol': u'HTTP',
        u'attachments': [[u'_Websidan_index.html',
          u'text/html; charset=iso-8859-1',
          u'PLAIN_TEXT']],
        u'data_source': u'PCAP'}},

     [[ ... output truncated ... ]]



.. _command-line-interface:

Using Commandline/Shell Interface
=================================

This feature is implemented by Hao MA. You can check following blog posts as example usages:

Interactive Shell Demonstration: http://gsoc2013.honeynet.org/2013/09/03/network-analyzer-project-updates-hao-ma-week-11-interactive-shell-demonstration/

Usage Examples for Shell/CLI: http://gsoc2013.honeynet.org/2013/09/10/network-analyzer-project-updates-hao-ma-week-12-testing-report/

CLI Demonstration: http://gsoc2013.honeynet.org/2013/08/27/network-analyzer-project-updates-hao-ma-week-10-cli-demonstration/

CLI Description: http://gsoc2013.honeynet.org/2013/07/23/474/

.. _web-ui:

Using Web UI
============

In this post I'll introduce our simple Web UI prototype.

Before we open the browser we need to start 2 different scripts under ovizart-ng/bin/ directory. First one is the daemon service, which is a basically a small REST API providing HTTP  Server. To start;::

  ./api_server.py start</pre>

This command will start a https server on localhost:9009 in order to change this values you can use this syntax::


  api_server.py [-h] [--host HOST] [--port PORT] [--ssl] {start,stop,restart}

Second command is responsible for  starting Web UI, which is based on Django 1.5. To start;::

  ./ui_server.py

this command will start Web UI on localhost:8000. Now we are ready; open a browser and on address bar write http://localhost:8000/

This screen will show up for login and daemon settings. Before we move on, Daemon Options will be moved to a configuration file,
for the ease of development and debugging I put those fields on the login form. These options should match with daemon parameters,
for default parameters user do not need to change anything.

In order to login, a user must be created with create_user.py script under directory ./ovizart-ng/bin/. In our example the user and
password is admin. This is not a default user account. Actually, system has no default users, one must be created right after installation.

.. figure:: _static/webui/WebUI-1.png
            :width: 625px
            :height: 441px
            :alt: Login Page

After login, (because of the first login) system does not contain any analysis. In order to start one click on the 'New' button on the left corner.

.. figure:: _static/webui/WebUI-2.png
            :width: 625px
            :height: 441px
            :alt: Empty Analysis Listing

This screen needs some makeup, but it has some nice feature. For example besides uploading your pcap file you can upload your analyzers as well.
so that you don't need to have an account on the core machine to use your own analyzer. I'm well aware that this feature could be very dangerous.
I'm planing to take 2 measures in order to improve security. First, improving user management by adding roles and rights, so that only certain users
will have right to upload analyzers. Second one is sand-boxing. Running analyzer module in a sandbox will make this feature a little bit safer.

.. figure:: _static/webui/WebUI-3.png
            :width: 625px
            :height: 441px
            :alt: Upload Screen

Select your pcap file to upload and click on 'Upload & Start' button. Your next screen will be this one

.. figure:: _static/webui/WebUI-4.png
            :width: 625px
            :height: 441px
            :alt: Analysis Listing - Init

After some time (system does not have a progressbar to show the current status of the evaluation), click on the 'Browse' button or refresh the page
to see changed status of the analysis. If you want to delete an analysis click on the checkbox on the left side of the analysis and click on the
'Delete' button. This action can not be done, will delete each information, files, reports, etc. generated during that analysis.

.. figure:: _static/webui/WebUI-5.png
            :width: 625px
            :height: 441px
            :alt: Analysis Listing - Finished

Finished analyses have a summary on the rightmost column, number of packet, name of the pcap file and number of streams extracted from given pcap file. Clicking on ID will open the details screen.

.. figure:: _static/webui/WebUI-8.png
            :width: 625px
            :height: 441px
            :alt: Show Details - No attachments

At the top part we have the summary section which contains basic information about the given pcap file. The next section
contains the information about the streams extracted from given pcap file. Stream list is a collapsible table. Each row
of this table starts Application/Transport Layer protocol information. Then we have standard stream identifiers Source IP,
Source Port, Destination IP, Destination Port. Number of Packets follows the identifiers.

On rightmost column we can observe an icon of file and magnifier. File means that system extracted some file(s) from
that specific stream. Magnifier means that system has analyzer reports for that specific stream's extracted files.

.. figure:: _static/webui/WebUI-6.png
            :width: 625px
            :height: 441px
            :alt: Show Details - Attachments

Clicking on a row will expand that row and show additional info about that stream.

* **Pcap File**: clicking on the filename will start download of that stream specific pcap file.
* **Reassembled Traffic**: Those links provide reconstructed application layer traffic in a file for further analysis/study/examination. You can see 3 different links, clicking on links will start the download of files, that are

  A  -> B, this file contains all requests made by A

  A <-  B, this file contains all responses given by B

  A <-> B, this file contains whole request response pair between A and B.


* **Attachments**: This section contains information about extracted files from that stream. On the right column you can see the mime-type of the extracted file as well. Clicking on the link will start the download of extracted file.
* **Analyzer Reports**: Current system does have Virus Total and Cuckoo wrappers as analyzers. Clicking on those links will open a new tab for the results to see. Because of the limitations analyze results may take some time to be ready. Here is a sample screen-shot from virustotal.

.. figure:: _static/webui/WebUI-7.png
            :width: 625px
            :height: 441px
            :alt: Show Details - Attachments
