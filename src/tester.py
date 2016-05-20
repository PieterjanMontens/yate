#!/usr/bin/python3.4
## Pieterjan Montens 2016
## https://github.com/PieterjanMontens
import optparse
import sys
import json
import config
import re
from yate_tools import y_error, y_print

################################### MAIN STUFF
##############################################
def main():
    ############ Handle input & parameters
    p = optparse.OptionParser()
    p.add_option('--debug','-d',action="store_true", default=False, help="Enable Debug")
    options, arguments = p.parse_args()

    tester = Tester(config.PARSER_DEFS)

    if options.debug:
        tester.debug_enable()

    try:
        for line in sys.stdin:
            tester.test(json.loads(line))
        y_print(line)
    except ValueError:
        y_error('\n Warning: line failed to parse, probably not valid json\n')
        y_error(line)

    ############ Job's done !
    exit(0)

class Tester:
    __defs = None
    __debug = False

    #################################### PUBLIC METHODS
    def __init__(self,defs):
        self.__defs = defs
        return None

    def debug_enable(self):
        self.__debug = True
        self.__log("\nDebug Enabled")
        return None

    def test(self,data):
        found_error = False
        for key,df in self.__defs.items():
            if not 'test_type' in df:
                continue
            if data[key] == None:
                y_error('\n Warning: key ' + key + ' not found in data')
                found_error = True
            if not self.__is_valid(data[key], df):
                y_error('\n Warning: check for ' + key + ' failed. data: ' + data[key])
                self.__log('Key "' + key + '": BAD FORMAT => ' + data[key])
                found_error = True
            else:
                self.__log('Key "' + key + '": OK')

        return False if found_error is False else True

    #################################### PRIVATE METHODS
    def __is_valid(self,value,df):
            if df['test_type'] == 'regex_match':
                reg = re.compile(df['test_regex'])
                match = re.search(reg,value)
                if match:
                    return True
                else:
                    return False
            else:
                raise Exception('unknown test type')

    def __log(self,msg):
        if (self.__debug):
            print(msg + "\n")

if __name__ == '__main__':
  main()
