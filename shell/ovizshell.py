__auther__ = "zqzas"

import sys
sys.path.append("..")

from ovizart import Ovizart
import ovizcli

'''
import fysom

fsm = Fysom({
  'initial': 'initial',
  'events': [
    {'name': 'set_input',   'src': 'initial',   'dst': 'input_ok'},
    {'name': 'set_tool',    'src': 'input_ok',  'dst': 'ready'},
    {'name': 'set_tool',    'src': 'initial',   'dst': 'ready'},
    {'name': 'analyze',     'src': 'ready',     'dst': 'analyzing'},
    {'name': 'done',        'src': 'analyzing', 'dst': 'ready'},
  ]
})
'''

configData = {'output':'', 'input':'', 'external_tool': '', 'verbose':''}

def getSet(cmd, set_dict):
    set_pos = cmd.find('set ') + 4
    equal_pos = cmd.find('=')
    key = cmd[set_pos: equal_pos].lstrip().strip()
    value = cmd[equal_pos + 1 :].split()[0]
    set_dict[key] = value
    return


while True:
    if configData['input'] == '':
        print   """Please set input: a file or an url. \nExample:
                set input=http://google.com
                """

    

    print '>>>'

    cmd = str(raw_input())

    
    if cmd.startswith('set'):
        getSet(cmd, configData)
    else:
        if cmd.startswith('list-available'):
            cli_args = ['-l']
        else:
            if cmd.startswith('version'):
                cli.args = ['-v']
            else:
                cli_args = []
                
                cli_args += ['-i', configData['input']]
                if configData['output'] != '':
                    cli_args += ['-o', configData['output']]
                if configData['external_tool'] != '':
                    cli_args += [configData['external_tool']]
                if configData['verbose'] != '':
                    cli_args += ['-V']
        cli_main(cli_args)
        


        


        


