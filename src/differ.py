#!/usr/bin/python3.4
## Pieterjan Montens 2016
## https://github.com/PieterjanMontens
##
## Creates diff files between STDIN and a computed updated revision

import optparse
import config
from pathlib import Path
from yate_tools import y_error, y_print, stdin_read, f_read, f_write, contentId_obtain
from diff_match_patch import diff_match_patch
from diff_match_patch import patch_obj


################################### MAIN STUFF
##############################################
def main():
    ############ prepare values
    options, arguments = arguments_parse()
    text      = stdin_read()
    contentId = options.force_id if options.force_id is not None else contentId_obtain(text, options.id_field)
    diffPath  = config.DIFF_PATH % contentId
    txtPath   = config.TXT_PATH % contentId
    filepath  = Path(txtPath)

    ############ do your job
    ### No revised file found ? Why are you even calling me ?
    if not filepath.is_file():
        y_error('\n -- No new revision file found\n')
        print('\n -- No new revision file found\n')
        exit(1)

    ### Ok, go on..
    textNew  = f_read(txtPath)
    dmp      = diff_match_patch()
    rawPatch = dmp.patch_make(text, textNew)
    txtPatch = dmp.patch_toText(rawPatch)
    f_write(diffPath, txtPatch)

    print("\nPatch for " + contentId + " Written !\n")

    ############ job's done !
    exit(0)

########################## ARGUMENTS'N'OPTIONS
def arguments_parse() :
    p = optparse.OptionParser()
    p.add_option('--debug', '-d', action="store_true", default=False, help="Enable Debug")
    p.add_option('--id_field', '-i', action="store", default=None, help="Set field containing ID value")
    p.add_option('--force_id', '-f', action="store", default=None, help="Force ID value")
    options, arguments =  p.parse_args()

    if options.id_field is None:
        y_error('\n Error: No ID field given\n')
        exit(1)

    return options, arguments

######################################### INIT
if __name__ == '__main__':
  main()
