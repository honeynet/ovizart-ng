#!/usr/bin/env python
__author__ = 'ggercek'

# Taken from: http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/

import sys
import os
import time
import atexit

from signal import SIGTERM


class Daemon:
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        print '1'
        try:
            pf = file(self.pidfile,'r')
            print '2'
            pid = int(pf.read().strip())
            print '3'
            pf.close()
            print '4'
        except IOError:
            print '5'
            pid = None
        print '6'
        if not pid:
            print '7'
            message = "pidfile %s does not exist. Daemon not running?\n"
            print '8'
            sys.stderr.write(message % self.pidfile)
            print '9'
            return # not an error in a restart
        print '10'
        # Try killing the daemon process
        try:

            while 1:
                print '11'
                os.kill(pid, SIGTERM)
                print '12'
                time.sleep(0.1)
        except OSError, err:
            print '13'
            err = str(err)
            print '14'
            if err.find("No such process") > 0:
                print '15'
                if os.path.exists(self.pidfile):
                    print '16'
                    os.remove(self.pidfile)
                    print '17'
            else:
                print '18'
                print str(err)
                print '19'
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """