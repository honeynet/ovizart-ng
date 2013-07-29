
# Exclude unwanted analyzers

import os

OUTPUT_FOLDER = os.path.abspath("output") + "/"


class Config():

    def __init__(self):
        self.exclude_analyzer = []
        self.input_files = []
        self.output_folder = OUTPUT_FOLDER

        # Cuckoo options
        self.is_cuckoo_available = True
        self.cuckoo_ip = "localhost"
        self.cuckoo_port = 9000
        self.cuckoo_html_enabled = True
        self.cuckoo_timeout = 60
        self.cuckoo_tcpdump_enabled = True



