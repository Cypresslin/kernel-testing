#!/usr/bin/env python3
from requests_oauthlib  import OAuth1
import requests
import json
from time               import sleep
from enum               import Enum
from .pdu               import PDU
from datetime           import datetime

def progress(msg):
    print(msg)

class MachineReleaseFailed(Exception):
    def __init__(s, error):
        s.msg = error

class MachineReleaseTimeout(Exception):
    def __init__(s, error):
        s.msg = error

class MachineAllocationTimeout(Exception):
    def __init__(s, error):
        s.msg = error

class MachineDeploymentTimeout(Exception):
    def __init__(s, error):
        s.msg = error

# MACHINE_STATUS
#
class MACHINE_STATUS(Enum):
    """
    The vocabulary of a `Node`'s possible statuses.
    """
    NEW                   = 0   # The node has been created and has a system ID assigned to it.
    COMMISSIONING         = 1   # Testing and other commissioning steps are taking place.
    FAILED_COMMISSIONING  = 2   # The commissioning step failed.
    MISSING               = 3   # The node can't be contacted.
    READY                 = 4   # The node is in the general pool ready to be deployed.
    RESERVED              = 5   # The node is ready for named deployment.
    DEPLOYED              = 6   # The node has booted into the operating system of its owner's choice and is ready for use.
    RETIRED               = 7   # The node has been removed from service manually until an admin overrides the retirement.
    BROKEN                = 8   # The node is broken: a step in the node lifecyle failed.
    DEPLOYING             = 9   # The node is being installed.
    ALLOCATED             = 10  # The node has been allocated to a user and is ready for deployment.
    FAILED_DEPLOYMENT     = 11  # The deployment of the node failed.
    RELEASING             = 12  # The node is powering down after a release request.
    FAILED_RELEASING      = 13  # The releasing of the node failed.
    DISK_ERASING          = 14  # The node is erasing its disks.
    FAILED_DISK_ERASING   = 15  # The node failed to erase its disks.

STATUS_MAP = [
    MACHINE_STATUS.NEW,
    MACHINE_STATUS.COMMISSIONING,
    MACHINE_STATUS.FAILED_COMMISSIONING,
    MACHINE_STATUS.MISSING,
    MACHINE_STATUS.READY,
    MACHINE_STATUS.RESERVED,
    MACHINE_STATUS.DEPLOYED,
    MACHINE_STATUS.RETIRED,
    MACHINE_STATUS.BROKEN,
    MACHINE_STATUS.DEPLOYING,
    MACHINE_STATUS.ALLOCATED,
    MACHINE_STATUS.FAILED_DEPLOYMENT,
    MACHINE_STATUS.RELEASING,
    MACHINE_STATUS.FAILED_RELEASING,
    MACHINE_STATUS.DISK_ERASING,
    MACHINE_STATUS.FAILED_DISK_ERASING,
]

class MAAS(object):

    # __init__
    #
    def __init__(s, maas_server_address, creds, hostname, domain, series, arch, flavour='generic', api='2.0'):
        s.api = api
        (s.consumer_key, s.key, s.secret) = creds.split(':')
        s.oauth = OAuth1(s.consumer_key,
                         client_secret="",
                         resource_owner_key=s.key,
                         resource_owner_secret=s.secret,
                         signature_method='PLAINTEXT',
                         signature_type='auth_header')
        s.api_url = 'http://%s/MAAS/api/%s' % (maas_server_address, api)
        s.__machines = None
        if api == '2.0':
            s.hostname = hostname
        else:
            s.hostname = '%s.%s' % (hostname, domain)
        s.domain   = domain
        s.series   = series
        s.arch     = arch
        s.flavour  = flavour

    # ------------------------------------------------------------------------------------------------------
    #

    def _raw_get(s, uri, params=None):
        url = "%s%s" % (s.api_url, uri)
        return requests.get(url=url, auth=s.oauth, params=params, headers={'Accept' : 'application/json'})

    def _raw_post(s, uri, params=None):
        url = "%s%s" % (s.api_url, uri)
        return requests.post(url=url, auth=s.oauth, data=params, headers={'Accept' : 'application/json'})

    def _raw_put(s, uri, params=None):
        url = "%s%s" % (s.api_url, uri)
        return requests.put(url=url, auth=s.oauth, data=params)

    def get(s, uri, params=None):
        return json.loads(s._raw_get(uri, params).text)

    def post(s, uri, params=None):
        return s._raw_post(uri, params)

    def put(s, uri, params=None):
        return s._raw_put(uri, params)

    # ------------------------------------------------------------------------------------------------------
    #

    def _release(s, hostname):
        sysid = s.machines[hostname]['system_id']
        if s.api == '2.0':
            request = s.post('/machines/%s/' % sysid, params={'op': 'release'})
        else:
            request = s.post('/nodes/%s/' % sysid, params={'op': 'release'})
        return request

    def _allocate(s, hostname):
        if s.api == '2.0':
            request = s.post('/machines/', params={'op': 'allocate', 'name': hostname})
        else:
            request = s.post('/nodes/', params={'op': 'acquire', 'name': hostname})
        return request

    def _deploy(s, hostname, series, arch):
        sysid = s.machines[hostname]['system_id']
        if s.api == '2.0':
            request = s.put('/machines/%s/' % sysid, params={'architecture': '%s/%s' % (arch, s.flavour)})
            request = s.post('/machines/%s/' % sysid, params={'op': 'deploy', 'distro_series': series})
        else:
            request = s.put('/nodes/%s/' % sysid, params={'architecture': arch})
            request = s.post('/nodes/%s/' % sysid, params={'op': 'start', 'distro_series': series})
        return request

    # ------------------------------------------------------------------------------------------------------
    #

    @property
    def machines(s):
        if s.__machines is None:
            s.__machines = {}
            if s.api == '2.0':
                result = s.get('/machines/')
            else:
                result = s.get('/nodes/', params={'op': 'list'})
            for machine in result:
                s.__machines[machine['hostname']] = machine
        return s.__machines

    def status(s, hostname):
        s.__machines = None  # invalidate the cache, we want the latest status
        if s.api == '2.0':
            retval = STATUS_MAP[s.machines[hostname]['status']]
        else:
            retval = STATUS_MAP[s.machines[hostname]['substatus']]
        return retval

    def allocate(s, hostname, timeout=30):
        progress('        Allocating...       ')
        s._allocate(hostname)

        start = datetime.utcnow()
        while True:
            if s.status(hostname) == MACHINE_STATUS.ALLOCATED:
                break

            now = datetime.utcnow()
            delta = now - start
            if delta.seconds > (timeout * 60):
                raise MachineAllocationTimeout('The specified timeout (%d) was reached while waiting for the system (%s) to be allocated.' % ((timeout * 60), hostname))

            sleep(10)

        return

    def release(s, hostname, timeout=30):
        if s.status(hostname) != MACHINE_STATUS.READY:
            progress('        Releasing...       ')
            s._release(hostname)

            power_cycled = False
            start = datetime.utcnow()
            while True:
                if s.status(hostname) == MACHINE_STATUS.READY:
                    break

                if s.status(hostname) == MACHINE_STATUS.FAILED_RELEASING:
                    if power_cycled:
                        raise MachineReleaseFailed('Failed to release (%s).' % hostname)

                    # Power the system completely off and then back on using the pdu. This
                    # may reset the BMC to a good state so it can be released.
                    #
                    pdu = PDU(hostname)
                    pdu.cycle()
                    sleep(60) # Give the BMC one minute to come back to life
                    s._release(hostname)
                    power_cycled = True

                now = datetime.utcnow()
                delta = now - start
                if delta.seconds > (timeout * 60):
                    raise MachineReleaseTimeout('The specified timeout (%d) was reached while waiting for the system (%s) to release.' % ((timeout * 60), hostname))

                sleep(10)

        return

    def deploy(s, hostname, series, arch, timeout=30):
        progress('        Deploying...       ')
        s._deploy(hostname, series, arch)

        start = datetime.utcnow()
        while True:
            if s.status(hostname) == MACHINE_STATUS.DEPLOYED:
                break

            now = datetime.utcnow()
            delta = now - start
            if delta.seconds > (timeout * 60):
                raise MachineDeploymentTimeout('The specified timeout (%d) was reached while waiting for the system (%s) to be allocated.' % ((timeout * 60), hostname))

            sleep(30)

    def provision(s):
        retval = False

        s.release(s.hostname)
        s.allocate(s.hostname)
        s.deploy(s.hostname, s.series, s.arch)

        if s.status(s.hostname) == MACHINE_STATUS.DEPLOYED:
            progress('        Deployed       ')
            retval = True
        else:
            progress('        Failed Deployment')

        return retval
