#!/usr/bin/python3.4
## Pieterjan Montens 2016
## https://github.com/PieterjanMontens
##
## Checks for applicable diff files, and patches content if found
## Meant to be used in a pipe: for the moment, only reads from stdin

import optparse
import config
import sys
from pathlib import Path
from yate_tools import y_error, y_print, stdin_read, f_read, f_write, contentId_obtain
from diff_match_patch import diff_match_patch


################################### MAIN STUFF
##############################################
def main():
    ############ Handle input & parameters
    options, arguments = arguments_parse()
    text      = stdin_read()
    contentId = contentId_obtain(text, options.id_field)
    diffPath  = config.DIFF_PATH % contentId
    filepath  = Path(diffPath)

    ############ do your job
    ### No patch file ? Ok, go on
    if not filepath.is_file():
        sys.stdout.write(text)
        exit(0)

    rawPatch = f_read(diffPath)
    dmp      = diff_match_patch()
    patches  = dmp.patch_fromText(rawPatch)
    (textPatched,checks) = dmp.patch_apply(patches,text)
    #Checks are ignored for now
    sys.stdout.write(textPatched)

    ############ Job's done !
    exit(0)

########################## ARGUMENTS'N'OPTIONS
def arguments_parse() :
    p = optparse.OptionParser()
    p.add_option('--debug', '-d', action="store_true", default=False, help="Enable Debug")
    p.add_option('--id_field', '-i', action="store", default=None, help="Set field containing ID value")
    options, arguments = p.parse_args()

    if options.id_field is None:
        y_error('\n Error: No ID field given\n')
        exit(1)

    return options, arguments


######################################### INIT
if __name__ == '__main__':
  main()
