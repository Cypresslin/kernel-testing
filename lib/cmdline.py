#!/usr/bin/env python
#
# This application takes a list json file as input. That json file
# contains a 'dictionary' of key value pairs where the key is a
# LauncPad bug id and the value is the source package of interest.
#

from getopt                             import getopt, GetoptError

from lib.utils                          import stdo, error
from lib.dbg                            import Dbg

# CmdlineError
#
# The type of exception that will be raised by Cmdline.process() if there
# are command line processing errors.
#
class CmdlineError(Exception):
    # __init__
    #
    def __init__(self, error):
        self.msg = error

# Cmdline
#
class Cmdline:
    """
    Handle all the command line processing for the application.
    """
    # error
    #
    def error(self, e, defaults):
        """
        Simple helper which prints out an error message and then prints out the usage.
        """
        if e != '': error("%s\n" % e)
        self.usage(defaults)

    # usage
    #
    def usage(self, defaults):
        """
        Prints out the help text which explains the command line options.
        """
        stdo("    Usage:                                                                                   \n")
        stdo("        %s [<options>] <comma-separated-list-of-bug-ids>                                     \n" % defaults['app_name'])
        stdo("                                                                                             \n")
        stdo("    Options:                                                                                 \n")
        stdo("        --help           Prints this text.                                                   \n")
        stdo("                                                                                             \n")
        stdo("        --debug=<debug options>                                                              \n")
        stdo("                         Performs additional output related to the option enabled and        \n")
        stdo("                         the application defined support for the option.                     \n")
        stdo("                                                                                             \n")
        stdo("                         Recognized debug options:                                           \n")
        stdo("                             enter                                                           \n")
        stdo("                             leave                                                           \n")
        stdo("                             verbose                                                         \n")
        stdo("                             cfg                                                             \n")
        stdo("                                                                                             \n")
        stdo("    Examples:                                                                                \n")
        stdo("        %s --debug=\"enter,leave,verbose\"                                                   \n" % defaults['app_name'])

    # process
    #
    def process(self, argv, defaults):
        """
        This method is responsible for calling the getopt function to process the command
        line. All parameters are processed into class variables for use by other methods.
        """
        result = True
        try:
            cfg = defaults

            optsShort = ''
            optsLong  = ['help', 'debug=']
            opts, args = getopt(argv[1:], optsShort, optsLong)

            for opt, val in opts:
                if (opt == '--help'):
                    raise CmdlineError('')

                elif opt in ('--debug'):
                    cfg['debug'] = val.split(',')
                    for level in cfg['debug']:
                        if level not in Dbg.levels:
                            Dbg.levels.append(level)

            if result: # No errors yet
                # There might be some bugs listed on the command line.
                #
                if len(args) > 0:
                    cfg['args'] = args


        except GetoptError, error:
            raise CmdlineError(error)

        return cfg
# vi:set ts=4 sw=4 expandtab:

