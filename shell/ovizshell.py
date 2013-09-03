__auther__ = "zqzas"

import sys
sys.path.append("..")

from ovizart import Ovizart
from ovizcli import cli_main

import cmd
#thanks to http://www.farmckon.net/?p=181
try:
        import readline
except ImportError:
        try:
                import pyreadline as readline
        # throw open a browser if we fail both readline and pyreadline
        except ImportError:
                import webbrowser
                webbrowser.open("http://ipython.scipy.org/moin/PyReadline/Intro#line-36")
                # throw open a browser
        #pass
else:
        import rlcompleter
        if(sys.platform == 'darwin'):
                readline.parse_and_bind ("bind ^I rl_complete")
        else:
                readline.parse_and_bind("tab: complete")



class OvizShell(cmd.Cmd):
    SETOPTIONS= [ 'input', 'output', 'external_tool', 'verbose' ]

    def __init__(self):
        #super(OvizShell, self).__init__()
        cmd.Cmd.__init__(self)
        
        #self.ovizcli_args = []
        self.configData = {'output':'', 'input':'', 'external_tool': '', 'verbose':''}


    def triggerOvizcli(self, args):
        try:
            cli_main(args)
        except SystemExit:
            print "Done."
        


    def getSet(self, cmd, set_dict):
        set_pos = 0
        equal_pos = cmd.find('=')
        key = cmd[set_pos: equal_pos].lstrip().strip()
        value = cmd[equal_pos + 1 :].split()[0]
        set_dict[key] = value
        return

    def do_set(self, args):
        "Set the config data."
        self.getSet(args, self.configData)

    def complete_set(self, text, line, begidx, endidx):
        if not text:
            completions = self.SETOPTIONS
        else:
            completions = [f for f in self.SETOPTIONS if f.startswith(text)]
        return completions

    def do_list(self, args):
        "List the available modules."
        self.triggerOvizcli(['-l'])

    def do_version(self, args):
        "Display the current version of Ovizart."
        self.triggerOvizcli(['-v'])

    def do_start(self, args):
        "Start analyze."

        cli_args = []
        if self.configData['input'] != '':
            cli_args += ['-i', self.configData['input']]
        if self.configData['output'] != '':
            cli_args += ['-o', self.configData['output']]
        if self.configData['external_tool'] != '':
            cli_args += [self.configData['external_tool']]
        if self.configData['verbose'] != '':
            cli_args += ['-V'] 
        self.triggerOvizcli(cli_args)

    def do_show(self, args):
        "Show the state of config data at this moment."
        print self.configData

    def do_reset(self, args):
        "Reset the config data such as input, output, etc."
        self.configData = {'output':'', 'input':'', 'external_tool': '', 'verbose':''}


    def do_EOF(self, line):
        "Stop the program."
        return True

if __name__ == '__main__':
    help_info = """
A interactive shell for ovizart-ng with the autocomplete(press tab) and help support
Example:
    > set input = http://mal.site
    > set output = /tmp
    > set external_tool = -js
    > show
    > start

For the more info, you may also refer to ovizcli.py
    """
    OvizShell().cmdloop(help_info)

 
