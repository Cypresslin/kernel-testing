#!/usr/bin/env python
#

from sys                                import stdout

# _o2ascii
#
# Convert a unicode string or a decial.Decimal object to a str.
#
def _o2ascii(obj):
    retval = None
    if type(obj) != str:
        if type(obj) == unicode:
            retval = obj.encode('ascii', 'ignore')
        else:
            retval = str(obj)
    else:
        retval = obj
    return retval

# Dbg
#
class Dbg:
    """
    A class which hopefully makes adding debug print statements easier and outputs better
    looking results.
    """
    levels = []
    indent_level = 0

    @classmethod
    def __print(cls, txt):
        stdout.write("%*s%s" % (cls.indent_level * 4, ' ', txt))
        stdout.flush()

    @classmethod
    def p(cls, txt):
        cls.__print(txt)

    @classmethod
    def enter(cls, txt):
        """
        Print a debug message preceeded by 'Enter'.
        """
        if 'enter' in cls.levels:
            cls.__print("Enter: %s\n" % (txt))
            cls.indent_level += 1

    @classmethod
    def leave(cls, txt):
        """
        Print a debug message preceeded by 'Leave'.
        """
        if 'leave' in cls.levels:
            cls.indent_level -= 1
            cls.__print("Leave: %s\n" % (txt))

    @classmethod
    def ret(cls, txt, result):
        """
        Print a debug message preceeded by 'Leave'.
        """
        if 'leave' in cls.levels:
            cls.indent_level -= 1
            cls.__print("Leave: %s (%s)\n" % (txt, _o2ascii(result)))

    @classmethod
    def progress(cls, txt):
        """
        Print a debug message preceeded by 'Leave'.
        """
        if 'progress' in cls.levels:
            cls.__print(txt)

    @classmethod
    def verbose(cls, txt):
        """
        Print a debug message preceeded by 'Leave'.
        """
        if 'verbose' in cls.levels:
            cls.__print(txt)

    @classmethod
    def warn(cls, txt):
        """
        Print a debug message preceeded by 'Warning:'.
        """
        if 'warning' in cls.levels:
            cls.__print("Warning: %s\n" % (txt))

    @classmethod
    def error(cls, txt):
        """
        Print a debug message preceeded by 'Error:'.
        """
        if 'error' in cls.levels:
            cls.__print("Error: %s\n" % (txt))

# vi:set ts=4 sw=4 expandtab:
