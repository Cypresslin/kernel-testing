#!/usr/bin/env python
#
from os                                 import path
from time                               import sleep

from lib.shell                          import ssh, sh, ShellError
from lib.log                            import cdebug
from lib.configuration                  import Configuration

# Cobbler
#
class Cobbler(object):
    # __init__
    #
    def __init__(s, server, target, series, arch):
        cdebug('Enter Cobbler::__init__')

        s.target  = target
        s.series  = series
        s.arch    = arch

        cdebug('Leave Cobbler::__init__')

    # configure_orchestra
    #
    def configure_orchestra(s):
        '''
        Create the appropriate profiles and system configurations to the orchestra server
        for the system we are going to provision.
        '''
        cdebug('Enter MetalProvisioner::configure_orchestra')
        if not s.quiet:
            print('Configure the Orchestra server')

        o = Configuration['systems'][s.target]['provisioner']
        o_series = o['series'][s.series]
        o_arch   = o['arch'][s.arch]
        distro = '%s%s-%s' % (s.series, o_series['server distro decoration'], o_arch)
        kickstart = path.join(s.kickstarts_root, 'kt-%s.preseed' % (o_series['preseed']))
        repos = "'%s-%s %s-%s-security'" % (s.series, o_arch, s.series, o_arch)

        server = o['server']
        t = Configuration['systems'][s.target]
        if not s.quiet:
            print('    remove profile \'%s\'' % s.name)
        ssh('%s@%s' % ('kernel', server), 'sudo cobbler profile remove --name=%s' % (s.name))

        if not s.quiet:
            print('    adding profile \'%s\' with series: %s  arch: %s' % (s.name, s.series, s.arch))
        ssh('%s@%s' % ('kernel', server), 'sudo cobbler profile add --name=%s --distro=%s --kickstart=%s --repos=%s' % (s.name, distro, kickstart, repos))

        if not s.quiet:
            print('    adding system \'%s\'' % (s.name))
        ssh('%s@%s' % ('kernel', server), 'sudo cobbler system add --name=%s --profile=%s --hostname=%s --mac=%s' % (s.name, s.name, s.name, t['mac address']))
        cdebug('Leave MetalProvisioner::configure_orchestra')

    # cycle_power
    #
    def cycle_power(s):
        '''
        Has the smarts on how to go about turning the power off to a server
        remotely and then turning it back on. In some cases, multiple ports
        must be power cycled.
        '''
        cdebug('Enter MetalProvisioner::cycle_power')
        if not s.quiet:
            print('Cycling the power on \'%s\'' % (s.target))

        t = Configuration['systems'][s.target]

        if 'ipmi' in t:
            for state in ['off', 'on']:
                cmd = "ipmitool -H %s -I lanplus -U %s -P %s power %s" % (t['ipmi']['ip'], t['ipmi']['username'], t['ipmi']['passwd'], state)
                print(cmd)
                result, output = sh(cmd, ignore_result=False)

                if state == 'off':
                    sleep(120) # Some of the systems want a little delay
                              # between being powered off and then back on.
        else:
            # Power cycle the system so it will netboot and install
            #
            server = t['provisioning']['server']
            for state in ['off', 'on']:
                for psu in t['cdu']:
                    if psu['ip'] != '':
                        try:
                            ssh('%s@%s' % ('kernel', server), 'fence_cdu -a %s -l kernel -p K3rn3! -n %s -o %s' % (psu['ip'], psu['port'], state), quiet=True)
                        except ShellError as e:
                            # Sometimes the call to the orchestra server will time-out (not sure why), just
                            # wait a minute and try again.
                            #
                            sleep(120)
                            if not s.quiet:
                                print('    Initial power cycle attempt failed, trying a second time.')
                            ssh('%s@%s' % ('kernel', server), 'fence_cdu -a %s -l kernel -p K3rn3! -n %s -o %s' % (psu['ip'], psu['port'], state), quiet=True)

                if state == 'off':
                    sleep(120) # Some of the systems want a little delay
                              # between being powered off and then back on.
        cdebug('Leave MetalProvisioner::cycle_power')

    # provision
    #
    def provision(s):
        cdebug('        Enter Cobbler::provision')
        s.configure_orchestra()
        s.cycle_power()
        cdebug('        Leave Cobbler::provision')

# vi:set ts=4 sw=4 expandtab syntax=python:
