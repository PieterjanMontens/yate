#!/usr/bin/python3.4
## Pieterjan Montens 2016
## https://github.com/PieterjanMontens

import optparse
import sys
import json
import config
from pathlib import Path
from yate_parser import Parse

################################### MAIN STUFF
##############################################
def main():

    ############ Handle input & parameters
    data_out = 'stdout'
    data_in = 'param'
    buffr   = ''
    p = optparse.OptionParser()
    p.add_option('--inp','-i', action="store", default=None, help="Input file (utf-8 text only)")
    p.add_option('--json','-j',action="store_true", default=False, help="Output JSON")
    options, arguments = p.parse_args()

    if options.json:
        data_out = 'json'

    if options.inp == None:
        linecount = 0
        stdinbuffer = ""
        for line in sys.stdin:
            linecount += 1
            stdinbuffer += line

        if linecount > 1:
            data_in = 'pipe'
            buffr = stdinbuffer
        else:
            print('\n Error: No input file defined.\n')
            exit(1)
    else:
        filepath = Path(options.inp)
        if not filepath.is_file():
            print('\n Error: Given input is not a file.\n')
            exit(1)
        with open(self.filename, 'r+') as fl:
            buffr = fl.read()

    ############ Do your job
    parser = Parse()
    parser.set_data(buffr)
    output = {}
    for key, pdef in config.PARSER_DEFS.items():
        if 'key' in pdef:
            key = pdef.key
        output[key] = parser.use(pdef)


    ############ Handle output
    if data_out == 'stdout':
        for key,value in sorted(output.items()):
            if type(value) is list:
                print ('{0: <10}'.format(key.upper()),
                       ':',
                       ', '.join(value))
            else:
                print ('{0: <10}'.format(key.upper()),
                       ':',
                       value)
    elif data_out == 'json':
        print(json.dumps(output))

    ############ Job's done !
    exit(0)

if __name__ == '__main__':
  main()
