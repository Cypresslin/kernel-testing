#!/usr/bin/env python
#

from re                                 import compile

class Debian:
    version_line_rc = compile("^(linux[-\S]*) \(([0-9]+\.[0-9]+\.[0-9]+[-\.][0-9]+\.[0-9]+[~\S]*)\) (\S+); urgency=\S+$")
    version_rc      = compile("^(\d+\.\d+)\.\d+[-\.](\d+)\.(\d+)([~\S]*)$")

# vi:set ts=4 sw=4 expandtab:
