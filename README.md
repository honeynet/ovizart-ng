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




	