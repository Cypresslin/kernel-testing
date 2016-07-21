# TODO:
#
#    1. Use administrator/insecure for the username/passwd for ipmi.
#    2. Use the debian installer and not the fastpath installer.
#       NOTE: Try to use the fast path installer and "fixup" the install
#             after the system comes up.
#

from lib.log                                        import cdebug, center, cleave
from time                                           import sleep

from maastk.client                                  import MaasClient
from maastk.node                                    import NODE_STATUS
from maastk.error                                   import MaasTKStandardException, MaasTKTimeoutException
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
        center('nodes')
        if s._nodes is None:
            s._nodes = {}
            nodes = s.client.nodes()
            for n in nodes:
                s._nodes[n['hostname']] = n
        cleave('nodes')
        return s._nodes

    def __release(s, sut):
        center('__rlease')
        retval = True
        sut.release()
        while sut.substatus != NODE_STATUS.READY:
            cdebug(sut.substatus)
            if sut.substatus == NODE_STATUS.FAILED_RELEASING:
                retval = False
                break
            else:
                sleep(5)  # Wait for the system to be released
        cleave('__rlease')
        return retval

    # release
    #
    def release(s, target):
        center('rlease')
        fqdn = '%s.%s' % (s.target, s.target_domain)
        sut = s.nodes[fqdn]
        if sut.substatus != NODE_STATUS.READY:
            progress('       Releasing...')
            if not s.__release(sut):
                # Try to get the current power state for the system. If this fails
                # reset the PDU port for the system. This is actually powering off
                # the outlets on the PDU and then powering them back on.
                #
                try:
                    cdebug('querying power status')
                    cdebug(sut.power_state)
                except MaasTKStandardException as e:
                    cdebug('power_state exception thrown')
                    if e.status == 503:  # The call timed out
                        pdu = PDU(s.target)
                        cdebug('           resetting the pdu outlets ------------------------------------------------------------------')
                        progress('           resetting the pdu outlets')
                        pdu.cycle()
                        cdebug('cycled .. sleeping')
                        sleep(60)  # Give the BMC one minute to come back to life

                        try:
                            cdebug('querying power status')
                            cdebug(sut.power_state)
                            s.__release(sut)
                        except MaasTKStandardException as e:
                            cdebug('power_state exception thrown')
                            progress('           unable to determine the power state')
        cleave('rlease')

    # client
    #
    @property
    def client(s):
        center('client')
        if s._client is None:
            progress('       Establishing connection to MAAS @ %s...' % s.maas_server)
            s._client = MaasClient(s.maas_server, s.creds)
        cleave('client')
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

        try:
            cdebug('before: ' + str(sut.substatus))
            s.release(s.target)
            cdebug(' after: ' + str(sut.substatus))

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
                if sut.substatus == NODE_STATUS.DEPLOYED:
                    progress('       Deployed     ')
                    retval = True
                else:
                    progress('       Failed Deployment')

        except MaasTKTimeoutException:
            # This usually idicates that even after a power cycle of the system MaaS is
            # still unable to talk to the BMC.
            #
            print("  ** Error: MaaS is reporting a timout. This usually indicates that even after a power cycle of the SUT")
            print("            MaaS is unable to talk to the SUT's BMC.")
            print("")
            progress('       Failed Deployment')

        cdebug('        Leave MAAS::provision')
        return retval
