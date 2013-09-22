ovizart-ng
==========

OVIZART - NG = Open VİZual Analsis foR network Traffic

This project aims aimed to analyze the traffic data in a more human readable way. 
It will analyze the information at the application level and displays the assembled information. 
It will help you analyze malwares inside the traffic as weel as anomalies. This project is an improvement to https://github.com/oguzy/ovizart project
in the scope of Google Summer of Code 2013.

---

#Installation Guide for Analyzer Wrappers

##Prerequisites:
1. Jinja2
2. python-requests



###Wrapper for Cuckoo Sandbox
--
Users may have two options for Cuckoo:

####1. Remote Cuckoo (Central)

Initially the remote cuckoo is set to ours. If you wanna change the remote Cuckoo from ours to yours, you may set the "self.cuckoo_ip and port" to yours in the ovizconf.py.


######HOW IT WORKS: 
Thanks to HoneyCloud, our team has a VPS that's able to deploy Cuckoo on the cloud. I've installed everything user needed to perform Cuckoo Sandbox. The service is provided in terms of REST API. 




####2.	Local Cuckoo
	
In this case, the user has to install and configure Cuckoo in his own machine which might involve with virtual machine (VirtualBox, VMWare, etc.) 

Please refer to http://docs.cuckoosandbox.org/en/latest/installation/

And start the local REST API server, set self.cuckoo_ip to localhost.

###Wrapper for Jsunpack-n

The packages of jsunpackn is at https://code.google.com/p/jsunpack-n/.


After downloaded, please install it and you need to put the absolute path of the package in ovizconf.py

For example:
 self.jsunpackn_path = "/Users/zqzas/Projects/ovizart-ng/analyzer/jsunpack_n/jsunpack-n-read-only"
 
The folder "jsunpack-n-read-only" contains the source of jsunpackn.


###Wrapper for VirusTotal
Only thing you need to do is to get your API key form VirusTotal guys and copy it to self.vt_apikey in the ovizconf.py.

As self.vt_apikey = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


------
#Usage and Test

http://gsoc2013.honeynet.org/2013/09/10/network-analyzer-project-updates-hao-ma-week-12-testing-report/

-----
###History before midterm

My mission before mid-term is to implement the wrappers for Cuckoo Sandbox, Jsunpack-n, and VirusTotal. In addition, I also wrote a CLI for these wrappers which make them easier to use.

I'd like to present the wrappers and CLI separately.


###Wrapper for Cuckoo Sandbox
--
Users may have two options for Cuckoo:

####1. Local Cuckoo
	
In this case, the user has to install and configure Cuckoo in his own machine which might involve with virtual machine (VirtualBox, VMWare, etc.) 

####2.	Remote Cuckoo (Central)


Thanks to HoneyCloud, our team has a VPS that's able to deploy Cuckoo on the cloud. I've installed everything user needed to perform Cuckoo Sandbox. The service is provided in terms of REST API. When the domain of cloud is ovizart.example.com, you may add your analysis task by issuing:
	
	curl -F url="http://www.malicious.site" http://localhost:8090/tasks/create/url
	
For more details, you may refer to http://docs.cuckoosandbox.org/en/latest/usage/api/.


###Wrapper for Jsunpack-n

jsunpack is a generic Javascript unpacker, and was designed for security researchers and computer professionals. A website running the source code is the http://jsunpack.jeek.org/. 

I implemented a simple jsunpackn wrapper with unified interface accepts URL and output the reports.

####Example:
```
$ python cli.py --jsunpackn --url google.com

	Jsunpack-n analyzing ..............................
	The key / has the following output in recursive mode
[nothing detected] /
	info: [0] no JavaScript
	file: stream_baea954b95731c68ae6e45bd1e252eb4560cdc45: 10 bytes


Note that none of the files are actually created since self.outdir is empty.
Instead, you could go through each url and look at the decodings that it creates
Looking at key /, has 1 files and 1 messages, that follow:
file              type=stream, hash=baea954b95731c68ae6e45bd1e252eb4560cdc45, data=10 bytes
output message    printable=1, impact=0, msg=[0] no JavaScript

```

###Wrapper for VirusTotal
"VirusTotal is a free service that analyzes suspicious files and URLs and facilitates the quick detection of viruses, worms, trojans, and all kinds of malware." https://www.virustotal.com


The input may be url or file. The file can be pcap or binary(malware).

####Example (analyze file):
```
>>>--virustotal --file /Users/zqzas/Downloads/traceroute.pcap
Virustotal analyzing ..............................
-------------------


{"scan_id": "31f58e13a669dacb7b56b5149a77df80b5a195cebacc92b3a620eb24e4d6cc69-1374911082", "sha1": "3d4e3fc5d09575ac3192726b19bc8fbfc971dc2d", "resource": "31f58e13a669dacb7b56b5149a77df80b5a195cebacc92b3a620eb24e4d6cc69", "response_code": 1, "sha256": "31f58e13a669dacb7b56b5149a77df80b5a195cebacc92b3a620eb24e4d6cc69", "permalink": "https://www.virustotal.com/file/31f58e13a669dacb7b56b5149a77df80b5a195cebacc92b3a620eb24e4d6cc69/analysis/1374911082/", "md5": "ede49a09d2569d730a689bc3c0e49483", "verbose_msg": "Scan request successfully queued, come back later for the report"}
```

####Example (analyze url):

```
>>>--virustotal --url http://google.com
Virustotal analyzing ..............................
-------------------

{"permalink": "https://www.virustotal.com/url/cf4b367e49bf0b22041c6f065f4aa19f3cfe39c8d5abc0617343d1a66c6a26f5/analysis/1374870884/", "url": "http://google.com/", "response_code": 1, "scan_date": "2013-07-26 20:34:44", "scan_id": "cf4b367e49bf0b22041c6f065f4aa19f3cfe39c8d5abc0617343d1a66c6a26f5-1374870884", "verbose_msg": "Scan finished, scan information embedded in this object", "filescan_id": null, "positives": 0, "total": 39, "scans": {"CLEAN MX": {"detected": false, "result": "clean site"}, "MalwarePatrol": {"detected": false, "result": "clean site"}, "ZDB Zeus": {"detected": false, "result": "clean site"}, "K7AntiVirus": {"detected": false, "result": "clean site"}, "Quttera": {"detected": false, "result": "clean site"}, "Yandex Safebrowsing": {"detected": false, "result": "clean site"}, "MalwareDomainList": {"detected": false, "result": "clean site"}, "ZeusTracker": {"detected": false, "result": "clean site"}, "zvelo": {"detected": false, "result": "clean site"}, "Google Safebrowsing": {"detected": false, "result": "clean site"}, "Kaspersky": {"detected": false, "result": "clean site"}, "BitDefender": {"detected": false, "result": "clean site"}, "Opera": {"detected": false, "result": "clean site"}, "G-Data": {"detected": false, "result": "clean site"}, "C-SIRT": {"detected": false, "result": "clean site"}, "CyberCrime": {"detected": false, "result": "unrated site"}, "Sucuri SiteCheck": {"detected": false, "result": "clean site"}, "VX Vault": {"detected": false, "result": "clean site"}, "ADMINUSLabs": {"detected": false, "result": "clean site"}, "SCUMWARE.org": {"detected": false, "result": "clean site"}, "Dr.Web": {"detected": false, "result": "clean site"}, "AlienVault": {"detected": false, "result": "clean site"}, "Sophos": {"detected": false, "result": "unrated site"}, "Malc0de Database": {"detected": false, "result": "clean site"}, "SpyEyeTracker": {"detected": false, "result": "clean site"}, "Phishtank": {"detected": false, "result": "clean site"}, "Avira": {"detected": false, "result": "clean site"}, "Antiy-AVL": {"detected": false, "result": "clean site"}, "Comodo Site Inspector": {"detected": false, "result": "clean site"}, "Malekal": {"detected": false, "result": "clean site"}, "ESET": {"detected": false, "result": "clean site"}, "SecureBrain": {"detected": false, "result": "unrated site"}, "Websense ThreatSeeker": {"detected": false, "result": "clean site"}, "Netcraft": {"detected": false, "result": "unrated site"}, "ParetoLogic": {"detected": false, "result": "clean site"}, "URLQuery": {"detected": false, "result": "unrated site"}, "Wepawet": {"detected": false, "result": "clean site", "detail": null}, "Fortinet": {"detected": false, "result": "unrated site"}, "Minotaur": {"detected": false, "result": "clean site"}}}
```


Command Line Interface (CLI)
------------
Using argparse, I built a concise CLI for wrappers, users may input url or file, and get reports. It also supports shell type interface(like a continuous conversation).


####Help information:
```
Zs-MBP:analyzer zqzas$ python cli.py 
You must input an url or file(path).
usage: cli.py [-h] [-v] [-c] [-j] [-u URL] [-f FILE]

An CLI for analyzer wrappers. Example: --virustotal --url http://google.com

optional arguments:
  -h, --help            show this help message and exit
  -v, --virustotal      Using VirusTotal to analyze binary, pcap or url
  -c, --cuckoo          Using Cuckoo Sandbox to analyze binary
  -j, --jsunpackn       Using Jsunpack-n to analyze url
  -u URL, --url URL     Input an url
  -f FILE, --file FILE  Input a file (path)
  
>>>
```
Other examples have been presented above in the wrapper part.

----

Install VirtualBox on OS X
---------
VirtualBox can be easilly installed through https://www.virtualbox.org/wiki/Downloads with several platforms supported.
I choose Mac OS X 10.8.3 for testing in this case.

Prepare for Cuckoo Sandbox
----------
In order to install Cuckoo, some preparations are needed according to Cuckoo Sandbox Documents. 

1. Install Python libraries, you may find details at http://docs.cuckoosandbox.org/en/latest/installation/host/requirements.html
as well as http://docs.cuckoosandbox.org/en/latest/installation/host/installation.html.

2. we may configure the Cuckoo Sandbox by specifing [machine_manager] which is vitualbox in this case, IP & port, and datebase.
Then <machinemanager>.conf is also important. You may see details here http://docs.cuckoosandbox.org/en/latest/installation/host/configuration.html.

In addition, you can also fill your Virustotal API key in processing.conf, if needed.



Configure Guest Machine
---------

1. Get a Win XP SP3 first, please be carefull about piracy issues.

2. Install XP on VirtualBox

3. Configure networking stuffs (Normally, this will be done by VirtualBox automatically)

4. Install Python inside WinXP

5. Got the cuckoo/agent/agent.py and run it in WinXP

6. Backup the VM, if needed.

7. (Important) Save a snapshot of WinXP like this:

	>$ VBoxManage snapshot "Name of VM" take "Name of snapshot" --pause	
	
	as suggested here: http://docs.cuckoosandbox.org/en/latest/installation/guest/saving.html
	

Get Cuckoo Sandbox Started
----

1. Basically, "python cuckoo.py" would be fine.

2. If it starts successfully, you may use its utils/submit.py, python API, or REST API to submit your analysis request. 

  Follow http://docs.cuckoosandbox.org/en/latest/usage/submit.html

3. The analysis reports will be stored in the "storage" folder. By default, it will generate html and json files unless the python packages cuckoo depends on are missing. 




	