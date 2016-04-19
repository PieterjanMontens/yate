#!/usr/bin/python3.4
## Pieterjan Montens 2016
## https://github.com/PieterjanMontens

import optparse
import json
import config
from pathlib import Path
from yate_parser import Parse



################################### MAIN STUFF
##############################################
def main():

    ############ Handle input & parameters
    out = 'stdout'
    p = optparse.OptionParser()
    p.add_option('--inp','-i', action="store", default=None, help="Input file (utf-8 text only)")
    p.add_option('--json','-j',action="store_true", default=False, help="Output JSON")
    options, arguments = p.parse_args()

    if options.json:
        out = 'json'

    if options.inp == None:
        print('\n Error: No input file defined.\n')
        exit(1)

    filepath = Path(options.inp)
    if not filepath.is_file():
        print('\n Error: Given input is not a file.\n')
        exit(1)

    ############ Do your job
    parser = Parse(options.inp)
    output = {}
    for key, pdef in config.PARSER_DEFS.items():
        if hasattr(pdef,'key'):
            key = pdef.key
        output[key] = parser.use(pdef)


    ############ Handle output
    if out == 'stdout':
        for key,value in output.items():
            if type(value) is list:
                print ('{0: <10}'.format(key.upper()),
                       ':',
                       value.join(', '))
            else:
                print ('{0: <10}'.format(key.upper()),
                       ':',
                       value)
    elif out == 'json':
        print(json.dumps(output))

    ############ Job's done !
    exit(0)

if __name__ == '__main__':
  main()
