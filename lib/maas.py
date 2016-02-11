# TODO:
#
#    1. Use administrator/insecure for the username/passwd for ipmi.
#    2. Use the debian installer and not the fastpath installer.
#       NOTE: Try to use the fast path installer and "fixup" the install
#             after the system comes up.
#

from lib.log                                        import cdebug
from time                                           import sleep

from maastk.client                                  import MaasClient
from maastk.node                                    import NODE_STATUS
from maastk.error                                   import MaasTKStandardException
from .pdu                                           import PDU


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
        s._client = None

        cdebug('        Leave MAAS::__init__')

    # nodes
    #
    @property
    def nodes(s):
        if s._nodes is None:
            s._nodes = {}
            nodes = s.client.nodes()
            for n in nodes:
                s._nodes[n['hostname']] = n
        return s._nodes

    # release
    #
    def release(s, target):
        fqdn = '%s.%s' % (s.target, s.target_domain)
        sut = s.nodes[fqdn]
        if sut.substatus != NODE_STATUS.READY:
            progress('       Releasing...')
            sut.release()

        while sut.substatus != NODE_STATUS.READY:
            if sut.substatus == NODE_STATUS.FAILED_RELEASING:
                # Try to get the current power state for the system. If this fails
                # reset the PDU port for the system. This is actually powering off
                # the outlets on the PDU and then powering them back on.
                #
                try:
                    sut.power_state
                except MaasTKStandardException as e:
                    if e.status == 503:  # The call timed out
                        pdu = PDU(s.target)
                        progress('           resetting the pdu outlets')
                        pdu.cycle()
                        sleep(60)  # Give the BMC one minute to come back to life

                        try:
                            sut.power_state
                        except MaasTKStandardException as e:
                            progress('           unable to determine the power state')
                break
            else:
                sleep(5)  # Wait for the system to be released

    # client
    #
    @property
    def client(s):
        if s._client is None:
            progress('       Establishing connection to MAAS @ %s...' % s.maas_server)
            s._client = MaasClient(s.maas_server, s.creds)
        return s._client

    # provision
    #
    def provision(s):
        cdebug('        Enter MAAS::provision')
        retval = False

        fqdn = '%s.%s' % (s.target, s.target_domain)
        arch = '%s/%s' % (s.target_arch, s.target_sub_arch)

        sut = s.nodes[fqdn]
        cdebug('\n')
        cdebug('%s' % fqdn)
        cdebug('         sysid: %s' % sut.system_id)
        cdebug('        status: %s' % sut.status)
        cdebug('    sub-status: %s' % sut.substatus)
        cdebug('          arch: %s' % sut.architecture)
        cdebug('        series: %s' % sut.distro_series)

        s.release(s.target)

        if sut.substatus == NODE_STATUS.READY:
            if sut.architecture != arch:
                progress('       Changing arch')
                sut.architecture = arch

            progress('       Acquiring...')
            sut.acquire()

            progress('       Starting...')
            sut.start(distro_series=s.target_series)

            progress('       Deploying ...')
            while sut.substatus == NODE_STATUS.DEPLOYING:
                sleep(10)
            progress('       Deployed     ')
            retval = True
        cdebug('        Leave MAAS::provision')
        return retval
