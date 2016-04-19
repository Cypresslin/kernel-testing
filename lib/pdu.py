import requests
import pexpect
import yaml
from time                                           import sleep


class PDU():
    # __init__
    #
    def __init__(s, target):
        s.__cfg = s.__config()
        s.__systems = s.__cfg['systems']
        s.__cdus = s.__cfg['cdus']
        s.target = target

    def __config(s):
        '''
        Fetch the information about mapping from a system to the CDU outlets.
        '''
        r = requests.get('http://kernel-maas.kernel/lab-systems-power.yaml')
        retval = yaml.load(r.text)
        return retval

    # cdu
    #
    def cdu(s, outlet):
        retval = None
        retval = pexpect.spawn('ssh -o MACs=hmac-sha1 -oKexAlgorithms=+diffie-hellman-group1-sha1 -oHostKeyAlgorithms=+ssh-dss enablement@%s' % s.__systems[s.target][outlet], timeout=600)
        retval.expect('Password: ')
        retval.sendline(s.__cdus[s.__systems[s.target][outlet]])
        retval.expect('Switched CDU: ')
        return retval

    # power
    #
    def power(s, state):
        for outlet in s.__systems[s.target]:
            ch = s.cdu(outlet)
            ch.sendline('%s %s' % (state, outlet))
            ch.expect('Switched CDU: ')

    # status
    #
    def status(s):
        for outlet in s.__systems[s.target]:
            ch = s.cdu(outlet)
            ch.sendline('status %s' % outlet)
            ch.expect('Switched CDU: ')
            ch.sendline('quit')

    # cycle
    #
    def cycle(s):
        s.power('off')
        sleep(60)
        s.power('on')
