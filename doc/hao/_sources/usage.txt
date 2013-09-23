************************
Usage and Test Reports
************************


**The Ovizart-ng is able to handle basically 4 types of input:**

#. PCAP: use the core analyzer

#. URL: may call the extended analyzer like VirusTotal, and Jsunpack-n

#. binary file: VirusTotal and Cuckoo analyzer may handle

#. text file: (like html and javascript file): Jsunpack-n analyzer may handle.

HOWTO:
===============

1. If you’d like to analyze a pcap, there’re 2 ways :

    1). use cli tool of ovizart-ng: ::

        Example:

        $ sudo python ovizcli.py -i /Users/zqzas/Projects/ovizart-ng/test/pcap/test-http.pcap -o /tmp
        I’m awesome
        name: /Users/zqzas/Projects/ovizart-ng/test/pcap/test-http.pcap type: PCAP
        Analysis Object{
        id: 1
        startTime: 2013-09-10 15:41:14.105801
        user: <NoUserDefined>
        config: <ovizconf.Config instance at 0x101b9a0e0>
        status: FINISHED
        data: [Data Object{
        tags: {'data_source': 'PCAP', 'app_layer_protocol': 'HTTP', 'attachments': [('_Websidan_index.html', 'regular file', None)], None: ['_Websidan_index.html']}
        data: {‘stream’: Stream Object {key: 6_10.1.1.101_3188_10.1.1.1_80, protocol: 6, srcIP: 10.1.1.101, srcPort: 3188, dstIP: 10.1.1.1, dstPort: 80, startTime: 1100903355.43, numberOfPacket: 14, pcapFile: /tmpanalysis_20130910_154114_105820/test-http.pcap/6_10.1.1.101_3188_10.1.1.1_80/6_10.1.1.101_3188_10.1.1.1_80.pcap}}
        }, ...omitted

    2). use interactive tool of ovizart-ng: ::

        $cd shell/

        $python ovizshell.py

        (Cmd) set input = /Users/zqzas/Projects/ovizart-ng/test/pcap/test-http.pcap
        (Cmd) set output = /tmp
        (Cmd) show
        {‘output’: ‘/tmp’, ‘external_tool’: ”, ‘verbose’: ”, ‘input’: ‘/Users/zqzas/Projects/ovizart-ng/test/pcap/test-http.pcap’}
        (Cmd) start
        name: /Users/zqzas/Projects/ovizart-ng/test/pcap/test-http.pcap type: PCAP
        Analysis Object{
        id: 1
        startTime: 2013-09-10 15:20:15.713222
        user: <NoUserDefined>
        config: <ovizconf.Config instance at 0x101c99908>
        status: FINISHED
        data: ….omitted
         

2. To analyze a url: ::

    (Cmd) set input = http://honeynet.org
    (Cmd) set output = /tmp
    (Cmd) set external_tool = -vt
    (Cmd) start
    name: http://honeynet.org type: URL
    Virus-total analyzing …………………………
    ['http://honeynet.org']
    ——————-
    {“permalink”: “https://www.virustotal.com/url/7547b57712941e07a6f9f786a6f311b534c94c0e2ba59126d7f1ef4ff24866e4/analysis/1377971788/”, “url”: “http://honeynet.org/”, “response_code”: 1, “scan_date”: “2013-08-31 17:56:28″, “scan_id”: “7547b57712941e07a6f9f786a6f311b534c94c0e2ba59126d7f1ef4ff24866e4-1377971788″,….omitted
    set to another external analyzer, “jsunpack-n” :

    (Cmd) set external_tool = -js
    (Cmd) show
    {‘output’: ‘/tmp’, ‘external_tool’: ‘-js’, ‘verbose’: ”, ‘input’: ‘http://honeynet.org’}
    (Cmd) start
    name: http://honeynet.org type: URL
    Jsunpack-n analyzing …………………………

    http://honeynet.org

    !!! /Users/zqzas/Projects/ovizart-ng/analyzer/jsunpack_n/jsunpack-n-read-only
    The key / has the following output in recursive mode
    [nothing detected] /
    info: [0] no JavaScript
    file: stream_bf9b49684b9623595fbb8e12648d3d19ecb5c77c: 19 bytes
    Note that none of the files are actually created since self.outdir is empty.
    Instead, you could go through each url and look at the decodings that it creates
    Looking at key /, has 1 files and 1 messages, that follow:
    file type=stream, hash=bf9b49684b9623595fbb8e12648d3d19ecb5c77c, data=19 bytes
    output message printable=1, impact=0, msg=[0] no JavaScript

    Response:
    [['The reports has been saved in /Users/zqzas/Projects/ovizart-ng/analyzer/jsunpack_n/jsunpack-n-read-only/log.'], []]

 

 

 

 
3. To analyze a binary: 

    1). VirusTotal: ::

        (Cmd) set input = /Users/zqzas/Downloads/anyexe.exe
        (Cmd) set output = /tmp
        (Cmd) set external_tool = -vt
        (Cmd) start
        name: /Users/zqzas/Downloads/anyexe.exe type: BINARY
        Virus-total analyzing …………………………

        {“scan_id”: “209342a2755315c7cef091f4f56de0875ee9cafee73814c05faf5db1a3955ee4-1378802153″, “sha1″: “5d92013fe866395a1c5370192d9ad83e88328a64″, “resource”: “209342a2755315c7cef091f4f56de0875ee9cafee73814c05faf5db1a3955ee4″, “response_code”: 1, “sha256″: “209342a2755315c7cef091f4f56de0875ee9cafee73814c05faf5db1a3955ee4″, “permalink”: “https://www.virustotal.com/file/209342a2755315c7cef091f4f56de0875ee9cafee73814c05faf5db1a3955ee4/analysis/1378802153/”, “md5″: “fb086841437211545b5260209fa9ecf7″, “verbose_msg”: “Scan request successfully queued, come back later for the report“}

    2). Cuckoo: ::

        (Cmd) set input = /Users/zqzas/Downloads/anyexe.exe
        (Cmd) set output = /tmp
        (Cmd) set external_tool = -ck
        (Cmd) start
        name: /Users/zqzas/Downloads/anyexe.exe type: BINARY
        Cuckoo analyzing …………………………
        You may check the reports at: ( http://81.167.148.242:8090/tasks/view/202 ) after it’s available.

 

 
4. text file, a html file with js: ::

        (Cmd) set input = /Users/zqzas/Projects/ovizart-ng/shell/report.html
        (Cmd) set output = /tmp
        (Cmd) set external_tool = -js
        (Cmd) start
        name: /Users/zqzas/Projects/ovizart-ng/shell/report.html type: PLAINTEXT
        Jsunpack-n analyzing …………………………
        /Users/zqzas/Projects/ovizart-ng/shell/report.html
        !!! /Users/zqzas/Projects/ovizart-ng/analyzer/jsunpack_n/jsunpack-n-read-only
        The key / has the following output in recursive mode
        [nothing detected] /
        info: [0] no JavaScript
        file: stream_e4a62c83ace44261a545060c454a6c6fd3c677f1: 50 bytes
        Note that none of the files are actually created since self.outdir is empty.
        Instead, you could go through each url and look at the decodings that it creates
        Looking at key /, has 1 files and 1 messages, that follow:
        file type=stream, hash=e4a62c83ace44261a545060c454a6c6fd3c677f1, data=50 bytes
        output message printable=1, impact=0, msg=[0] no JavaScript
        Response:
        [[], ['The reports has been saved in /Users/zqzas/Projects/ovizart-ng/analyzer/jsunpack_n/jsunpack-n-read-only/log.']]
        Above are the cases of using interactive shell, which can be achieved by ovizcli.py equivalently as well.



More Examples:
===============
    http://gsoc2013.honeynet.org/2013/09/22/network-analyzer-project-updates-hao-ma-week-13-more-examples/




