#!/usr/bin/python3.4
## Pieterjan Montens 2016
## https://github.com/PieterjanMontens
#
# Tests if data points are correctly filled in


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
    options, arguments = arguments_parse()
    tester = Tester(config.PARSER_DEFS, config.SPECIAL_TESTS)

    if options.debug:
        tester.debug_enable()

    if options.logfile:
        tester.logfile_set(options.logfile)

    ############ do your job
    try:
        for line in sys.stdin:
            Good = tester.is_ok(json.loads(line))
            if not Good:
                tester.log("Found errors in record:\n"+line+"\n\n")
        y_print(line)
    except ValueError:
        y_error('\n Warning: line failed to parse, probably not valid json\n')
        y_error(line)

    ############ Job's done !
    exit(0)

########################## ARGUMENTS'N'OPTIONS
def arguments_parse() :
    p = optparse.OptionParser()
    p.add_option('--debug','-d',action="store_true", default=False, help="Enable Debug")
    p.add_option('--logfile',action="store", default=False, help="Log file")
    options, arguments = p.parse_args()
    return options, arguments

class Tester:
    __defs = None
    __tests = None
    __debug = False

    #################################### PUBLIC METHODS
    def __init__(self,defs,tests):
        self.__defs = defs
        self.__tests = tests
        self.__logf = False
        return None

    def debug_enable(self):
        self.__debug = True
        self.__log("\nDebug Enabled\n")
        return None

    def logfile_set(self,logf):
        self.__logf = logf
        return None

    def is_ok(self,data):
        found_error = False
        for key,df in self.__defs.items():
            if not 'test_type' in df:
                continue
            if data[key] == None:
                y_error('\n Warning: key ' + key + ' not found in data')
                found_error = True
            if not self.__is_valid(data[key], df):
                y_error('\n Warning: check for ' + key + ' failed')
                self.__log('Key "' + key + '": BAD FORMAT')
                found_error = True
            #else:
            #    self.__log('Key "' + key + '": OK')

        for key,test in self.__tests.items():
            if test['applies'](data) == True:
                if test['test'](data) == False:
                    found_error = True
                    self.__log('Test ' + key +' Failed')
                #else:
                #    self.__log('Test ' + key +' Succeeded')



        return True if found_error is False else False

    def log(self,msg):
        self.__log(msg)

    #################################### PRIVATE METHODS
    def __is_valid(self,value,df):
            if df['test_type'] == 'regex_match':
                reg = re.compile(df['test_regex'])
                match = re.search(reg,value)
                if match:
                    return True
                else:
                    return False
            elif df['test_type'] == 'list_nonempty':
                if not isinstance(value,(list)):
                    return False
                if len(value) >= 1:
                    return True
                else:
                    return False
            elif df['test_type'] == 'lambda':
                return df['test_lambda'](value)
            else:
                raise Exception('unknown test type')

    def __log(self,msg):
        if (self.__debug):
            print(msg)
        if (self.__logf):
            with open(self.__logf, 'a') as out:
                out.write(msg + '\n')

######################################### INIT
if __name__ == '__main__':
  main()
