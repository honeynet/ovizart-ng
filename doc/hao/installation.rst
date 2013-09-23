******************
Installation
******************


Installation Guide for Analyzer Wrappers
=========================================

Prerequisites:
---------------
* python-requests



Wrapper for Cuckoo Sandbox
----------------------------
Users may have two options for Cuckoo:

#. Remote Cuckoo (Central)
    Initially the remote cuckoo is set to ours. If you wanna change the remote Cuckoo from ours to yours, you may set the "self.cuckoo_ip and port" to yours in the ovizconf.py.


    *HOW IT WORKS:*
    Thanks to HoneyCloud, our team has a VPS that's able to deploy Cuckoo on the cloud. I've installed everything user needed to perform Cuckoo Sandbox. The service is provided in terms of REST API. 




#. Local Cuckoo
    In this case, the user has to install and configure Cuckoo in his own machine which might involve with virtual machine (VirtualBox, VMWare, etc.) 

    Please refer to http://docs.cuckoosandbox.org/en/latest/installation/

    And start the local REST API server, set self.cuckoo_ip to localhost.

Wrapper for Jsunpack-n
------------------------
    The packages of jsunpackn is at https://code.google.com/p/jsunpack-n/.

    After downloaded, please install it and you need to put the absolute path of the package in ovizconf.py

    For example: ::
        self.jsunpackn_path = "/Users/zqzas/Projects/ovizart-ng/analyzer/jsunpack_n/jsunpack-n-read-only"
     
    The folder "jsunpack-n-read-only" contains the source of jsunpackn.


Wrapper for VirusTotal
-----------------------

    Only thing you need to do is to get your API key form VirusTotal guys and copy it
    to self.vt_apikey in the ovizconf.py. ::
    self.vt_apikey = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


Installation Guide for the Reporters
========================================

Prerequisites:
---------------
#. Jinja2 (when you'd like to output html)
#. xhtml2pdf (may convert html to pdf file, not suggested)


Installation Guide for the Shell
========================================

Prerequisites:
----------------
#. readline (or pyreadline for Windows)

