#!/usr/bin/env python
#

from os                                 import path
from os                                 import _exit
from dbg                                import Dbg
from utils                              import dump
import json


# CfgError
#
class CfgError(Exception):
    # __init__
    #
    def __init__(self, error):
        self.msg = error

    # __str__
    #
    def __str__(self):
        return self.msg

class Cfg():
    # load_user_config
    #
    @classmethod
    def load_user_config(cls, fname):
        """
        Load the passed in file as a json format configuration file.
        """
        Dbg.enter("utils.load_user_config")

        user_config = {}
        if path.exists(fname):
            with open(fname, 'r') as f:
                user_config = json.load(f)
                Dbg.verbose("user config file (%s) loaded\n" % (fname))

        Dbg.leave("utils.load_user_config")
        return user_config

    # merge_options
    #
    @classmethod
    def merge_options(cls, defaults, cmdline_options):
        """
        Merge the application options together into a final options dictionary. Options
        are taken from application defaults, an optional configuration file and from the
        command line.
        """
        Dbg.enter("utils.merge_config_options")

        cfg = {}

        # First: Load the application defaults into the final configuration dictionary.
        #
        for k in defaults:
            cfg[k] = defaults[k]

        # Second: If there is a configuration file specified, load that configuration
        #         file and merge that with the final configuration. Any existing config
        #         values are replaced by those from the config file.
        #
        cfg_fname = None
        if 'configuration_file' in cmdline_options:
            cfg['configuration_file'] = cmdline_options['configuration_file']
        elif 'configuration_file' in defaults:
            cfg['configuration_file'] = defaults['configuration_file']
        else:
            Dbg.verbose("No configuration_file option specified\n")

        if 'configuration_file' in cfg:
            Dbg.verbose("configuration_file option specified (%s)\n" % (cfg['configuration_file']))
            if '~' in cfg['configuration_file']:
                cfg['configuration_file'] = cfg['configuration_file'].replace('~', path.expanduser('~'))

            cfg_file_options = cls.load_user_config(cfg['configuration_file'])
            for k in cfg_file_options:
                cfg[k] = cfg_file_options[k]

        # Finaly: Any command line options are merge in, replacing any existing options
        #         from either the defaults or the configuration file.
        #
        for k in cmdline_options:
            cfg[k] = cmdline_options[k]

        if 'cfg' in Dbg.levels:
            Dbg.verbose("Configuration:\n")
            Dbg.verbose("-------------------------------------------------\n")
            for k in cfg:
                str = "%s" % (k)
                Dbg.verbose('    %-25s = "%s"\n' % (str, cfg[k]))
            if 'exit' in Dbg.levels: _exit(0)

        Dbg.leave("utils.merge_config_options")
        return cfg

# vi:set ts=4 sw=4 expandtab:
