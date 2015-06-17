# TODO:
#
#    1. Use administrator/insecure for the username/passwd for ipmi.
#    2. Use the debian installer and not the fastpath installer.
#       NOTE: Try to use the fast path installer and "fixup" the install
#             after the system comes up.
#

from os                                 import path
from logging                            import debug
import json
from lib.shell                          import sh, ssh
from lib.log                            import cdebug
from time                               import sleep
from datetime                           import datetime, timedelta

# MAAS
#
class MAAS(object):
    # __init__
    #
    def __init__(s, profile, server, creds, target, series, arch):
        cdebug('        Enter MAAS::__init__')

        s.profile = profile
        s.server  = server
        s.creds   = creds
        s.target  = target
        s.series  = series
        s.arch    = arch

        cdebug('        Leave MAAS::__init__')

    # provision
    #
    def provision(s):
        cdebug('        Enter MAAS::provision')
        maas = MAASCore(s.profile, s.server, s.creds)
        mt = maas.node(s.target)
        mt.stop_and_release()
        mt.acquire()
        mt.series(s.series)
        mt.arch(s.arch)
        mt.start()
        cdebug('        Leave MAAS::provision')

# MAASCore
#
class MAASCore():

    # __init__
    #
    def __init__(s, profile, server, creds):
        debug('MAASCore::__init__')

        s.profile = profile
        s.server  = server
        s.creds   = creds

        # Log into the maas server
        #
        # maas login maas http://thorin.ubuntu-ci/MAAS/api/1.0  jg2XAHBWGK8yzUn84F:M47jVf8JFbDBad26HV:AA8xyn7paqXvZE9rPAdPFQnqfm9yYaME
        ssh(s.server, 'maas login %s http://%s/MAAS/api/1.0 %s' % (s.profile, s.server, s.creds), quiet=True)

        s.__nodes = None
        s.__nodes_by_name = None
        s.prefix = 'maas %s ' % s.profile
        s.previous_node_cmd = datetime.utcnow()
        s.cmd_delay = 60 * 3

    def delay(s):
        # MAAS can't handle commands comming in too quickly to the same node.
        #
        now = datetime.utcnow()
        delta = now - s.previous_node_cmd
        if delta.seconds < s.cmd_delay:
            sleep(s.cmd_delay - delta.seconds)
        s.previous_node_cmd = datetime.utcnow()

    def node_cmd(s, hostname, cmd, properties=None):
        s.delay()
        if properties:
            cmd = '%s node %s %s %s' % (s.prefix, cmd, s.nodes_by_name[hostname]['system_id'], properties)
        else:
            cmd = '%s node %s %s' % (s.prefix, cmd, s.nodes_by_name[hostname]['system_id'])
        debug(cmd)
        ssh(s.server, cmd, quiet=True)
        s.__stale()

    @property
    def nodes(s):
        '''
        Build a dictionary of node information and return it.
        '''
        if s.__nodes is None:
            s.__nodes_by_name = None
            rc, ni = ssh(s.server, 'maas %s nodes list' % s.profile, quiet=True)
            ni = ' '.join(ni)
            s.__nodes = json.loads(ni)
        return s.__nodes

    @property
    def nodes_by_name(s):
        '''
        Build an index of the node info using the hostname
        '''
        if s.__nodes_by_name is None:
            for n in s.nodes:
                if s.__nodes_by_name is None:
                    s.__nodes_by_name = {}
                hostname = n['hostname']
                s.__nodes_by_name[hostname] = n
                if '.' in hostname:
                    h = hostname.split('.')
                    s.__nodes_by_name[h[0]] = n
        return s.__nodes_by_name

    def stop(s, hostname):
        '''
        Perform a "node stop".
        '''
        s.node_cmd(hostname, 'stop')

    def release(s, hostname):
        '''
        Perform a "node release".
        '''
        s.node_cmd(hostname, 'release')

    def start(s, hostname):
        '''
        Perform a "node start".
        '''
        s.node_cmd(hostname, 'start')

    def acquire(s, hostname):
        '''
        Perform a "nodes acquire".
        '''
        cmd = '%s nodes acquire name=%s' % (s.prefix, s.nodes_by_name[hostname]['hostname'])
        debug(cmd)
        ssh(s.server, cmd, quiet=True)
        s.__stale()

    def status(s, hostname):
        '''
        Return the status for a particular node.
        '''
        return s.nodes_by_name[hostname]['status']

    def node(s, hostname):
        return MAASNode(s, hostname)

    def update_series(s, hostname, series):
        s.node_cmd(hostname, 'update', 'osystem=ubuntu distro_series=ubuntu/%s' % series)

    def update_arch(s, hostname, arch):
        s.node_cmd(hostname, 'update', 'osystem=ubuntu architecture=%s/generic' % arch)

    def update_series_and_arch(s, hostname, series, arch):
        s.node_cmd(hostname, 'update', 'osystem=ubuntu distro_series=ubuntu/%s architecture=%s/generic' % (series, arch))

    def __stale(s):
        s.__nodes = None
        s.__nodes_by_name = None

# MAASNode
#
class MAASNode():
    '''
    '''

    # __init__
    #
    def __init__(s, maas, hostname):
        '''
        '''

        s.__maas  = maas
        s.__hostname = hostname

    def start(s):
        '''
        '''
        s.__maas.start(s.__hostname)

    def stop(s):
        '''
        '''
        s.__maas.stop(s.__hostname)

    def release(s):
        '''
        '''
        s.__maas.release(s.__hostname)

    def stop_and_release(s):
        '''
        '''
        s.stop()
        sleep(60)   # Pause for a bit while the stop completes.
        s.release()

    def status(s):
        '''
        '''
        return s.__maas.status(s.__hostname)

    def series(s, series):
        '''
        '''
        return s.__maas.update_series(s.__hostname, series)

    def arch(s, arch):
        '''
        '''
        return s.__maas.update_arch(s.__hostname, arch)

    def series_and_arch(s, series, arch):
        '''
        '''
        return s.__maas.update_arch(s.__hostname, series, arch)

    # acquire
    #
    # maas maas nodes acquire system_id=<system id>
    def acquire(s):
        '''
        '''
        return s.__maas.acquire(s.__hostname)

    def acquire_and_start(s):
        '''
        '''
        s.acquire()
        s.start()

