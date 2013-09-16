#!/usr/bin/env python
from IPython.utils.io import stdin, stdout, stderr

__author__ = 'ggercek'

import os
import sys
sys.path.append('../')
from ovizconf import PROJECT_ROOT
import subprocess


def main(args):
    os.chdir(os.path.join(PROJECT_ROOT, 'web/'))
    subprocess.call('python manage.py runserver', stdin=stdin, stdout=stdout, stderr=stderr, shell=True)
    pass


if __name__ == '__main__':
    main(sys.argv[1:])