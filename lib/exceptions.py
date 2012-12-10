#!/usr/bin/env python
#

# ErrorExit
#
class ErrorExit(Exception):
    """
    If an error message has already been displayed and we want to just exit the app, this
    exception is raised.
    """
    def __init__(self, emsg):
        self.__message = emsg

    @property
    def message(self):
        '''
        The shell command that was being executed when the timeout occured.
        '''
        return self.__message

# Timeout
#
class Timeout(Exception):
    """
    A task took longer than the specified timeout.
    """
    pass

# vi:set ts=4 sw=4 expandtab syntax=python:
