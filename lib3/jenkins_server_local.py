#!/usr/bin/env python3
#

import re
from jenkinsapi.jenkins                 import Jenkins
from lib3.shell                         import sh

# JenkinsServerLocal
#
class JenkinsServerLocal(object):
    @classmethod
    def connect(c):
        # Determine the local ip address by processing the results from "ip address"
        #
        ip = 'bogus'
        cmd = 'ip address'
        retval, output = sh(cmd, quiet=True)
        for line in output:
            m = re.search('inet (\d+\.\d+\.\d+\.\d+)\/\d+ brd \d+\.\d+\.\d+\.\d+ scope', line)
            if m:
                ip = m.group(1)
                break

        jenkins_url_default = "http://%s:8080" % ip
        return Jenkins(jenkins_url_default)

# vi:set ts=4 sw=4 expandtab syntax=python:
