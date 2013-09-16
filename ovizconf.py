
# Exclude unwanted analyzers

import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'upload') + "/"
OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, 'output') + "/"  # os.path.abspath("output") + "/"

class Config():

    def __init__(self):
        self.exclude_analyzer = []
        self.input_files = []
        self.output_folder = OUTPUT_FOLDER

        # Cuckoo options
        self.is_cuckoo_available = True
        self.cuckoo_ip = "81.167.148.242"
        self.cuckoo_port = 8090
        self.cuckoo_html_enabled = True
        self.cuckoo_timeout = 60
        self.cuckoo_tcpdump_enabled = True

        # Jsunpack-n options
        self.jsunpackn_path = ""

        # Virus Total API options
        self.vt_apikey = ""


