ovizart-ng
==========

OVIZART - NG = Open VİZual Analsis foR network Traffic

This project aims aimed to analyze the traffic data in a more human readable way. 
It will analyze the information at the application level and displays the assembled information. 
It will help you analyze malwares inside the traffic as weel as anomalies. This project is an improvement to https://github.com/oguzy/ovizart project
in the scope of Google Summer of Code 2013.

Install VirtualBox on OS X
---------
VirtualBox can be easilly installed through https://www.virtualbox.org/wiki/Downloads with several platforms supported.
I choose Mac OS X 10.8.3 for testing in this case.

Prepare for Cuckoo Sandbox
----------
In order to install Cuckoo, some preparations are needed according to Cuckoo Sandbox Documents. 

First, Installing Python libraries, you may find details at http://docs.cuckoosandbox.org/en/latest/installation/host/requirements.html
as well as http://docs.cuckoosandbox.org/en/latest/installation/host/installation.html.

Second, we may configure the Cuckoo Sandbox by specifing [machine_manager] which is vitualbox in this case, IP & port, and datebase.
Then <machinemanager>.conf is also important. You may see details here http://docs.cuckoosandbox.org/en/latest/installation/host/configuration.html.

In addition, you can also fill your Virustotal API key in processing.conf, if needed.



