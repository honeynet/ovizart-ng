__author__ = 'ggercek'

from datasource.pcap_handler import PcapDataSourceHandler

import os

if '__main__' == __name__:
    filename = os.path.abspath('../output/test-http.pcap')
    parser = PcapDataSourceHandler()
    summary = parser.parse(filename)
    print summary

    for d in summary['data']:
        # print data source value
        print d.tag('data_source')
