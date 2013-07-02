"""
This module holds the most common tags for ease of use.
Important Note: Try to avoid use strings directly during development
"""

__author__ = "ggercek"


class Tags:

    class DataSource:
        PCAP = "PCAP"

    # TODO: Not a fancy way! Need to change it
    class Protocol:
        HTTP = "HTTP"
        FTP = "FTP"
        DNS = "DNS"
        IRC = "IRC"
        SMTP = "SMTP"

    class Attachment:
        BINARY = "BINARY"
        PLAIN_TEXT = "PLAIN_TEXT"
        JAVASCRIPT = "JAVASCRIPT"