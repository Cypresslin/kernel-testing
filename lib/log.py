#!/usr/bin/env python
#
from logging                            import info, debug, warning
from ktl.termcolor                      import colored

def cinfo(msg, color='white'):
    Clog.info(msg, color)

def cdebug(msg, color='magenta'):
    Clog.debug(msg, color)

def cwarn(msg, color='red'):
    Clog.warn(msg, color)

def cerror(msg, color='red'):
    Clog.warn(msg, color)

def cnotice(msg, color='yellow'):
    Clog.notice(msg, color)

class Clog:
    '''
    Colored logging.
    '''
    dbg = False

    @classmethod
    def info(c, msg, color='white'):
        if c.dbg:
            # I do this becaus i'm weird and like things lined up in my log output
            # and "INFO -" is fewer chars then "DEBUG -" and so things don't line
            # up.
            #
            debug(colored(msg, color))
        else:
            info(colored(msg, color))

    @classmethod
    def debug(c, msg, color='magenta'):
        debug(colored(msg, color))

    @classmethod
    def warn(c, msg, color='red'):
        c.info(colored(msg, color))

    @classmethod
    def notice(c, msg, color='yellow'):
        c.info(colored(msg, color))

# vi:set ts=4 sw=4 expandtab syntax=python:
