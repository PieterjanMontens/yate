## Pieterjan Montens 2016
## https://github.com/PieterjanMontens

import sys
from yate_parser import Parse

def y_error(Msg):
    sys.stderr.write(Msg)
    return None

def y_print(Msg):
    sys.stdout.write(Msg)
    return None

def stdin_read():
    buffr = ""
    for line in sys.stdin:
        buffr += line
    return buffr

def f_read(fpath):
    with open(fpath) as f:
        contents = f.read()
    return contents

def f_write(fpath, contents):
    with open(fpath, 'w') as out:
        out.write(contents)
    return None

def contentId_obtain(text, id_field):
    parser    = Parse()
    parser.set_data(text)
    fieldDef  = config.PARSER_DEFS[id_field]
    contentId = parser.use(fieldDef)

    if contentId is 'not_found':
        y_error('\n Error: ID field not found in content\n')
        sys.stdout.write(text)
        exit(1)

    return contentId


