import os
import requests
import pexpect
import yaml
import platform
from time                               import sleep
from lib.log                            import cdebug, center, cleave


class PDU():
    # __init__
    #
    def __init__(s, target):
        center('PDU.__init__')
        s.__cfg = s.__config()
        s.__systems = s.__cfg['systems']
        s.__cdus = s.__cfg['cdus']
        s.target = target
        s.series = platform.dist()[2]
        cleave('PDU.__init__')

    def __config(s):
        '''
        Fetch the information about mapping from a system to the CDU outlets.
        '''
        maas_ip = '10.246.72.3:5240'
        center('PDU.__config')
        before = None
        if 'NO_PROXY' in os.environ:
            before = os.environ['NO_PROXY']
        os.environ['NO_PROXY'] = maas_ip
        r = requests.get('http://' + maas_ip + '/lab-systems-power.yaml')
        retval = yaml.load(r.text)
        if before:
            os.environ['NO_PROXY'] = before
        cleave('PDU.__config')
        return retval

    # cdu
    #
    def cdu(s, outlet):
        center('PDU.cdu')
        retval = None
        if s.series in ['trusty']:
            ssh_options = '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=quiet'
        else:
            ssh_options = '-o KexAlgorithms=+diffie-hellman-group1-sha1 -o HostKeyAlgorithms=+ssh-dss -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=quiet'
        cmd = 'ssh -o MACs=hmac-sha1 %s enablement@%s' % (ssh_options, s.__systems[s.target][outlet])
        cdebug('cmd: %s' % cmd)
        retval = pexpect.spawn(cmd, timeout=60)
        retval.expect('Password: ')
        retval.sendline(s.__cdus[s.__systems[s.target][outlet]])
        retval.expect('Switched CDU: ')
        cleave('PDU.cdu')
        return retval

    # power
    #
    def power(s, state):
        center('PDU.power')
        for outlet in s.__systems[s.target]:
            ch = s.cdu(outlet)
            ch.sendline('%s %s' % (state, outlet))
            ch.expect('Switched CDU: ')
        cleave('PDU.power')

    # status
    #
    def status(s):
        center('PDU.status')
        for outlet in s.__systems[s.target]:
            ch = s.cdu(outlet)
            ch.sendline('status %s' % outlet)
            ch.expect('Switched CDU: ')
            ch.sendline('quit')
        cleave('PDU.status')

    # cycle
    #
    def cycle(s):
        center('PDU.cycle')
        print('            Cycling Power...       ')
        s.power('off')
        sleep(60)
        s.power('on')
        cleave('PDU.cycle')
