#!/usr/bin/env python
#

from sys                                import argv
from os                                 import path
from logging                            import debug
import json

# __config
#
def __config():
    """
    Load the configuration file, returning the same as a python object.
    """
    retval = None

    file_name = 'kernel-testing.cfg'

    # Find it ...
    #
    fid = path.join(path.expanduser('~'), file_name)
    if not path.exists(fid): # Users home directory
        debug("not %s" % fid)
        fid = path.join(path.expanduser('~'), '.%s' % file_name)
        if not path.exists(fid): # Hidden file in the Users home directory
            debug("not %s" % fid)
            fid = path.join(path.dirname(argv[0]), file_name)
            if not path.exists(fid):
                fid = file_name
                if not path.exists(fid): # Current directory
                    debug("not %s" % fid)
                    fid = None

    if fid is not None:
        with open(fid, 'r') as f:
            cfg = json.load(f)

    else:
        print('')
        print("Error: Failed to find the configuration file.")
        print('')

    return cfg

KTConfig = __config()
