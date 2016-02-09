# TODO:
#
#    1. Use administrator/insecure for the username/passwd for ipmi.
#    2. Use the debian installer and not the fastpath installer.
#       NOTE: Try to use the fast path installer and "fixup" the install
#             after the system comes up.
#

from logging                                        import debug
import json
from lib.maas_shell                                 import mssh
from lib.log                                        import cdebug
from time                                           import sleep
from datetime                                       import datetime

from maastk.client                                  import MaasClient
from maastk.node                                    import NODE_STATUS


def progress(msg):
    print(msg)


# MAAS
#
class MAAS(object):
    # __init__
    #
    def __init__(s, maas_server, creds, target, target_domain, target_series, target_arch, target_sub_arch='generic'):
        cdebug('        Enter MAAS::__init__')

        s.maas_server       = maas_server
        s.creds             = creds
        s.target            = target
        s.target_domain     = target_domain
        s.target_series     = target_series
        s.target_arch       = target_arch
        s.target_sub_arch   = target_sub_arch

        s._sysids = None
        s._nodes = None

        cdebug('        Leave MAAS::__init__')

    # nodes
    #
    @property
    def nodes(s):
        if s._nodes is None:
            s._nodes = {}
            nodes = s.mc.nodes()
            for n in nodes:
                s._nodes[n['hostname']] = n
        return s._nodes

    # provision
    #
    def provision(s):
        cdebug('        Enter MAAS::provision')

        progress('       Establishing connection to MAAS @ %s...' % s.maas_server)
        s.mc = MaasClient(s.maas_server, s.creds)

        name = '%s.%s' % (s.target, s.target_domain)
        series = s.target_series
        arch = '%s/%s' % (s.target_arch, s.target_sub_arch)
        s.target = name

        sut = s.nodes[name]
        cdebug('\n')
        cdebug('%s' % name)
        cdebug('         sysid: %s' % sut.system_id)
        cdebug('        status: %s' % sut.status)
        cdebug('    sub-status: %s' % sut.substatus)
        cdebug('          arch: %s' % sut.architecture)
        cdebug('        series: %s' % sut.distro_series)

        if sut.substatus != NODE_STATUS.READY:
            progress('       Releasing...')
            sut.release()
            while sut.substatus != NODE_STATUS.READY:
                sleep(5)

        if sut.architecture != arch:
            progress('       Changing arch')
            sut.architecture = arch

        progress('       Acquiring...')
        sut.acquire()

        progress('       Starting...')
        sut.start(distro_series=series)

        progress('       Deploying ...')
        while sut.substatus == NODE_STATUS.DEPLOYING:
            sleep(10)
        progress('       Deployed     ')
        cdebug('        Leave MAAS::provision')
        return True


def release(s):
        cdebug('        Enter MAAS::release')
        name = '%s.%s' % (s.target, s.target_domain)
        sut = s.nodes[name]
        if sut.substatus != NODE_STATUS.READY:
            progress('       Releasing...')
            sut.release()
            while sut.substatus != NODE_STATUS.READY:
                sleep(5)
        cdebug('        Leave MAAS::release')
