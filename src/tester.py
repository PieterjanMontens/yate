#!/usr/bin/python3.4
## Pieterjan Montens 2016
## https://github.com/PieterjanMontens
#
# Tests if data points are correctly filled in


import optparse, sys, re
import json, yaml
import config
import logger

abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

with open('./logging.conf','r') as f:
    logConf = yaml.load(f)
logging.config.dictConfig(logConf)
logger = logging.getLogger('yateLogger')

################################### MAIN STUFF
##############################################
def main():
    ############ Handle input & parameters
    options, arguments = arguments_parse()
    tester = Tester(config.PARSER_DEFS, config.SPECIAL_TESTS)
    quiet = False
    discard = False

    if options.debug:
        tester.debug_enable()

    if options.quiet:
        tester.quiet_enable()
        quiet = True

    if options.logfile:
        tester.logfile_set(options.logfile)

    id_field    = options.id_field if options.id_field is not None else "undefined"
    discard_field = options.discard_field if options.discard_field is not None else "undefined"

    ############ do your job
    try:
        for line in sys.stdin:
            data = json.loads(line)
            identifier = data[id_field] if id_field is not "undefined" else "undefined"
            if discard_field is not "undefined" and data[options.discard_field] is True:
                tester.log("Record with Contentid " + identifier +" is discarded")
                logger.warning("Record with Contentid " + identifier +" is discarded\n\n")
                continue
            Good = tester.is_ok(json.loads(line))
            if not Good and not quiet:
                    logger.warning("Found errors. Contentid: "+identifier+"\n\n")
                    tester.log("Found errors. Contentid: "+identifier+"\nRecord: "+line+"\n\n")
            if Good and options.validate:
                logger.info(line)
    except ValueError as e:
        if not quiet:
            logger.warning('line failed to parse, probably not valid json: %s' % line)

        ############ Job's done !
    exit(0)

########################## ARGUMENTS'N'OPTIONS
def arguments_parse() :
    p = optparse.OptionParser()
    p.add_option('--debug','-d',action="store_true", default=False, help="Enable Debug")
    p.add_option('--quiet','-q',action="store_true", default=False, help="Quiet mode")
    p.add_option('--id_field', '-i', action="store", default=None, help="Set field containing ID value")
    p.add_option('--discard_field', '-x', action="store", default=None, help="Set a field (boolean) which signifies the record should be discarded")
    p.add_option('--validate', '-v', action="store_true", default=False, help="Sets validation mode, outputs stdin to stdout if checks are OK")
    p.add_option('--logfile',action="store", default=False, help="Log file")
    options, arguments = p.parse_args()
    return options, arguments

class Tester:
    __defs = None
    __tests = None
    __debug = False
    __quiet = False

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

    def quiet_enable(self):
        self.__quiet = True
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
                logger.warning('key ' + key + ' not found in data')
                found_error = True
            if not self.__is_valid(data[key], df):
                logger.warning('check for ' + key + ' failed')
                self.__log('\n\tKey "' + key + '": BAD FORMAT')
                found_error = True
            #else:
            #    self.__log('Key "' + key + '": OK')

        for key,test in sorted(self.__tests.items()):
            if test['applies'](data) == True:
                if test['test'](data) == False:
                    found_error = True
                    self.__log('Test ' + key +' Failed')
                    logger.warning('check for ' + key + ' failed')
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
            elif df['test_type'] == 'list':
                if not isinstance(value,(list)):
                    return False
                return True
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
        if (self.__quiet):
            return None
        if (self.__debug):
            logger.debug(msg)
        if (self.__logf):
            with open(self.__log, 'a') as out:
                out.write(msg + '\n')

######################################### INIT
if __name__ == '__main__':
  main()
