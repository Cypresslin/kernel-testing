#!/usr/bin/env python3
from lib3.shell                         import sh

def progress(msg):
    print(msg)

class JuJu(object):

    # __init__
    #
    def __init__(s, cloud, hostname, series, domain=None):
        s.cloud    = cloud
        s.hostname = hostname
        s.domain   = domain
        if domain is not None:
            s.qhn = '%s.%s' % (hostname, domain)
        else:
            s.qhn = hostname
        s.series   = series

    def release(s, target):
        cmd = 'juju destroy-controller --yes %s' % (target)
        r, o = sh(cmd)

    def provision(s):
        retval = False

        progress('        Deploying...       ')
        cmd = 'juju bootstrap %s %s --to %s --bootstrap-series %s --no-gui' % (s.hostname, s.cloud, s.qhn, s.series)
        r, o = sh(cmd, quiet=True)
        progress('        Deployed       ')

        return True
