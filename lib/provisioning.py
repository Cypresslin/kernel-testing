#!/usr/bin/env python
#
from os                                 import path
from logging                            import error
from datetime                           import datetime
from time                               import sleep
from logging                            import info
import re

from lib.infrastructure                 import Orchestra, LabHW, MAASConfig
from lib.hwe                            import HWE
from lib.shell                          import sh, ShellError, ssh, Shell
from lib.ubuntu                         import Ubuntu
from lib.exceptions                     import ErrorExit
from lib.maas                           import MAAS, MAASNode
from configuration                      import Configuration

# Provisioner
#
class Provisioner():

    _dry_run = False
    _quiet = False

    # __init__
    #
    def __init__(self, name, series, arch, hwe=False, debs=None, ppa=None, dry_run=False):
        self.name   = name
        self.series = series
        self.arch   = arch
        self.hwe    = hwe
        self.debs   = debs
        self.ppa    = ppa
        Provisioner.ppa = ppa
        self.quiet  = False
        Provisioner.quiet  = False
        self.dry_run= dry_run
        Provisioner._dry_run = dry_run
        Shell._dry_run = dry_run
        self.kickstarts_root = '/var/lib/cobbler/kickstarts/kernel'
        self.ubuntu = Ubuntu()

    # enable_proposed
    #
    def enable_proposed(self, target, series):
        '''
        On the target system, enable the -proposed archive pocket for the
        specified series.
        '''
        if not self.quiet:
            print('    enabling proposed')

        ssh(target, '\'echo deb http://us.archive.ubuntu.com/ubuntu/ %s-proposed restricted main multiverse universe | sudo tee -a /etc/apt/sources.list\'' % (series))

    # enable_ppa
    #
    def enable_ppa(self, target, series):
        '''
        On the target system, enable the -proposed archive pocket for the
        specified series.
        '''
        if not self.quiet:
            print('    enabling ppa %s' % self.ppa)
        ssh(target, '\'sudo apt-get -y install software-properties-common\'')
        ssh(target, '\'sudo add-apt-repository -y %s\'' % (self.ppa))

    # dist_upgrade
    #
    def dist_upgrade(self, target):
        '''
        Perform a update and dist-upgrade on a remote system.
        '''
        ssh(target, 'sudo apt-get update')
        ssh(target, 'sudo apt-get --yes dist-upgrade')

    # kernel_upgrade
    #
    def kernel_upgrade(self, target):
        '''
        Perform a update of the kernels on a remote system.
        '''
        ssh(target, 'sudo apt-get update')
        ssh(target, 'sudo apt-get --yes install linux-image-generic linux-headers-generic')

    # mainline_firmware_hack
    #
    def mainline_firmware_hack(self, target):
        '''
        Mainline kernels look for their firmware in /lib/firmware and might miss other required firmware.
        '''
        ssh(target, 'sudo ln -s /lib/firmware/\$\(uname -r\)/* /lib/firmware/', ignore_result=True)

    # wait_for_system
    #
    @classmethod
    def wait_for_system(cls, target, timeout=10):
        if not cls._dry_run:
            if not cls._quiet:
                print('Waiting for \'%s\' to come up.' % (target))

            start = datetime.utcnow()
            info('Starting waiting for \'%s\' at %s' % (target, start))
            while True:
                try:
                    result, output = sh('ssh -qf %s exit' % target, quiet=True, ignore_result=True)
                    if result == 0:
                        break

                except ShellError as e:

                    if 'port 22: Connection refused' in e.output:
                        # Just ignore this, we know that we can connect to the remote host
                        # otherwise we wouldn't have been able to reboot it.
                        #
                        print("** Encountered 'Connection refused'")
                        pass
                    else:
                        print("Something else bad happened")
                        raise

                now = datetime.utcnow()
                delta = now - start
                if delta.seconds > timeout * 60:
                    info('Timed out at: %s' % now)
                    raise ErrorExit('The specified timeout (%d) was reached while waiting for the target system (%s) to come back up.' % (timeout, target))

                sleep(60)
                info('Checking at: %s' % datetime.utcnow())

    # reboot
    #
    @classmethod
    def reboot(cls, target, wait=True, quiet=False):
        '''
        Reboot the target system and wait 5 minutes for it to come up.
        '''
        ssh(target, 'sudo reboot', quiet=quiet)
        if wait:
            cls.wait_for_system(target, timeout=10)

    # install_custom_debs
    #
    def install_custom_debs(self, target):
        '''
        On the SUT, download and install custome kernel debs for testing.
        '''
        if not self.quiet:
            print('Installing custom debs.')

        # Pull them down
        #
        ssh(target, 'wget -r -A .deb -e robots=off -nv -l1 --no-directories %s' % self.debs)

        # Install everything
        #
        ssh(target, 'sudo dpkg -i *_all.deb *_%s.deb' % self.arch, ignore_result=True) # best effort

    # install_hwe_kernel
    #
    def install_hwe_kernel(self, target):
        '''
        On the SUT, configure it to use a HWE kernel and then install the HWE
        kernel.
        '''
        if not self.quiet:
            print('Updating to the HWE kernel.')

        # We add the x-swat ppa so we can pick up the development HWE kernel
        # if we want.
        #
        if 'ppa' in HWE[self.hwe_series]:
            ssh(target, 'sudo apt-get install --yes python-software-properties')
            ssh(target, 'sudo apt-add-repository ppa:ubuntu-x-swat/q-lts-backport')

        hwe_package = HWE[self.hwe_series]['package']
        ssh(target, 'sudo apt-get update')
        ssh(target, 'sudo apt-get install --yes %s' % (hwe_package))

    # configure_passwordless_access
    #
    def configure_passwordless_access(self, target):
        result, out = sh('scp -r $HOME/.ssh %s:' % (target), ignore_result=True)
        if result > 0:
            error('****')
            error('**** Failed to scp .ssh to %s' % target)
            error(out)
            error('****')

# VirtualProvisioner
#
class VirtualProvisioner(Provisioner):

    # __init__
    #
    def __init__(self, virt_host, name, series, arch, hwe=False, debs=None, dry_run=False):
        Provisioner.__init__(self, name, series, arch, hwe, dry_run=dry_run)
        self.virt_host = virt_host

    # configure_orchestra
    #
    def configure_orchestra(self, target):
        '''
        Create the appropriate profiles and system configurations to the orchestra server
        for the system we are going to provision.
        '''
        if not self.quiet:
            print('Configure the Orchestra server')

        o_series = Orchestra['series'][self.series]
        o_arch   = Orchestra['arch'][self.arch]
        distro = '%s%s-%s' % (self.series, o_series['server distro decoration'], o_arch)
        kickstart = path.join(self.kickstarts_root, 'kt-virt-%s.preseed' % (o_series['preseed']))

        t = LabHW[target]
        server = t['provisioning']['server']
        if not self.quiet:
            print('    remove profile \'%s\'' % self.name)
        ssh('%s@%s' % ('kernel', server), 'sudo cobbler profile remove --name=%s' % (self.name))

        if not self.quiet:
            print('    adding profile \'%s\' with series: %s  arch: %s' % (self.name, self.series, self.arch))
        ssh('%s@%s' % ('kernel', server), 'sudo cobbler profile add --name=%s --distro=%s --kickstart=%s --ksmeta=hostname=%s --virt-file-size=20,100 --virt-ram=1000 --virt-disk=raw,raw --virt-path=/opt/%s-a,/opt/%s-b' % (self.name, distro, kickstart, self.name, self.name, self.name))

    # configure_host_for_virtual_guests
    #
    def configure_host_for_virtual_guests(self, target):
        '''
        '''
        ssh(target, r'sudo apt-get install -y qemu-kvm koan virt-manager')
        ssh(target, r"sudo sed -ie 's/^\(libvirtd.*\)/\1jenkins/' /etc/group")

        # The file structure on an Ubuntu CD uses the string amd64 instead of x86_64. To
        # use koan to install x86_64 VMs it is necessary (at least with cobbler on Oneiric)
        # to modify one file.
        #
        result, interfaces = ssh(target, r'sudo cat /etc/network/interfaces')
        for line in interfaces:
            line = line.strip()
            if 'inet dhcp' in line:
                (iface, interface, inet, dhcp) = line.split(' ')
        ssh(target, r'sudo sed -i -e \'/elif uri.count\(\"installer-amd64\"\):/ i \\ \\ \\ \\ \\ \\ \\ \\ elif uri.count\(\"x86_64\"\):\\n \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ self._treeArch = \"amd64\"\' /usr/share/pyshared/virtinst/OSDistro.py')
        ssh(target, r'/bin/echo -e \'\\n\\nauto br0\\niface br0 inet dhcp\\n     \ \ \ bridge_ports     %s\\n     \ \ \ bridge_stp         off\\n     \ \ \ bridge_fd            0\\n     \ \ \ bridge_maxwait 0\\n\' \| sudo tee -a /etc/network/interfaces' % interface)

        ssh(target, r'sudo ifup br0')

    # create_virtual_guest
    #
    def create_virtual_guest(self, target):
        ssh(target, 'sudo koan --virt --server=%s --profile=%s --virt-name=%s --virt-bridge=br0 --vm-poll' % (LabHW[target]['provisioning']['server'], self.name, self.name))

    # provision
    #
    def provision(self):
        target = self.name

        # If we are installing a HWE kernel, we want to install the correct series first.
        #
        if self.hwe:
            self.hwe_series = self.series
            self.series = HWE[self.series]['series']

        # We network boot/install the bare-metal hw to get our desired configuration on it.
        #
        self.configure_orchestra(self.virt_host)

        self.configure_host_for_virtual_guests(self.virt_host)
        self.create_virtual_guest(self.virt_host)

        # Once the initial installation has completed, we continue to install and update
        # packages so that we are testing the latest kernel, which is what we want.
        #
        self.wait_for_system(target, timeout=60) # Allow 30 minutes for network installation
        if not self.ubuntu.is_development_series(self.series):
            self.enable_proposed(target, self.series)
        if self.ppa is not None:
            self.enable_ppa(target, self.series)
        if self.ubuntu.is_development_series(self.series):
            self.kernel_upgrade(target)
        else:
            self.dist_upgrade(target)
        self.mainline_firmware_hack(target)

        if self.hwe:
            self.install_hwe_kernel(target)

        # We want to install to pick up any new kernel that we would have installed due
        # to either the dist-upgrade that was performed, or the install of the hwe
        # kernel.
        #
        self.reboot(target)

        self.configure_passwordless_access(target)

# MetalProvisioner
#
class MetalProvisioner(Provisioner):

    # __init__
    #
    def __init__(self, name, series, arch, hwe=False, debs=None, ppa=None, dry_run=False):
        Provisioner.__init__(self, name, series, arch, hwe, debs, ppa, dry_run)

    # configure_orchestra
    #
    def configure_orchestra(self, target):
        '''
        Create the appropriate profiles and system configurations to the orchestra server
        for the system we are going to provision.
        '''
        if not self.quiet:
            print('Configure the Orchestra server')

        o_series = Orchestra['series'][self.series]
        o_arch   = Orchestra['arch'][self.arch]
        distro = '%s%s-%s' % (self.series, o_series['server distro decoration'], o_arch)
        kickstart = path.join(self.kickstarts_root, 'kt-%s.preseed' % (o_series['preseed']))
        repos = "'%s-%s %s-%s-security'" % (self.series, o_arch, self.series, o_arch)

        t = LabHW[target]
        server = t['provisioning']['server']
        if not self.quiet:
            print('    remove profile \'%s\'' % self.name)
        ssh('%s@%s' % ('kernel', server), 'sudo cobbler profile remove --name=%s' % (self.name))

        if not self.quiet:
            print('    adding profile \'%s\' with series: %s  arch: %s' % (self.name, self.series, self.arch))
        ssh('%s@%s' % ('kernel', server), 'sudo cobbler profile add --name=%s --distro=%s --kickstart=%s --repos=%s' % (self.name, distro, kickstart, repos))

        if not self.quiet:
            print('    adding system \'%s\'' % (self.name))
        ssh('%s@%s' % ('kernel', server), 'sudo cobbler system add --name=%s --profile=%s --hostname=%s --mac=%s' % (self.name, self.name, self.name, t['mac address']))

    # cycle_power
    #
    def cycle_power(self, target):
        '''
        Has the smarts on how to go about turning the power off to a server
        remotely and then turning it back on. In some cases, multiple ports
        must be power cycled.
        '''
        if not self.quiet:
            print('Cycling the power on \'%s\'' % (target))

        t = LabHW[target]

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
                            if not self.quiet:
                                print('    Initial power cycle attempt failed, trying a second time.')
                            ssh('%s@%s' % ('kernel', server), 'fence_cdu -a %s -l kernel -p K3rn3! -n %s -o %s' % (psu['ip'], psu['port'], state), quiet=True)

                if state == 'off':
                    sleep(120) # Some of the systems want a little delay
                              # between being powered off and then back on.

    # target_verified
    #
    def target_verified(self, target, series, arch):
        '''
        Confirm that the target system has installed what was supposed to be installed. If we asked for
        one series but another is on the system, fail.
        '''
        retval = False

        result, codename = ssh(target, r'lsb_release --codename')
        for line in codename:
            line = line.strip()
            if line.startswith('Codename:'):
                if series not in line:
                    info("")
                    info("*** ERROR:")
                    info("    Was expecting the target to be (%s) but found it to be (%s) instead." % (series, line.replace('Codename:\t','')))
                    info("")
                else:
                    retval = True

        # Verify we installed the arch we intended to install
        #
        if retval:
            retval = False
            result, processor = ssh(target, r'uname -p')
            for line in processor:
                line = line.strip()

                if 'Warning: Permanently aded' in line: continue
                if line == '': continue

                if line == 'x86_64':
                    installed_arch = 'amd64'
                elif line == 'i686':
                    installed_arch = 'i386'
                else:
                    installed_arch = line

            if arch == installed_arch:
                retval = True
            else:
                info("")
                info("*** ERROR:")
                info("    Was expecting the target to be (%s) but found it to be (%s) instead." % (arch, installed_arch))
                info("")

        # Are we running the series correct kernel?
        #
        if retval:
            retval = False
            kv = None
            result, kernel = ssh(target, r'uname -vr')
            for line in kernel:
                line = line.strip()

                if 'Warning: Permanently aded' in line: continue
                if line == '': continue

                m = re.search('(\d+.\d+.\d+)-\d+-.* #(\d+)-Ubuntu.*', line)
                if m:
                    kv = m.group(1)

            if kv is not None:
                installed_series = self.ubuntu.lookup(kv)['name']

                if installed_series == series:
                    retval = True
                else:
                    info("")
                    info("*** ERROR:")
                    info("    Was expecting the target to be (%s) but found it to be (%s) instead." % (series, installed_series))
                    info("")
            else:
                info("")
                info("*** ERROR:")
                info("    Unable to find the kernel version in any line.")

        return retval

    # provision
    #
    def provision(self):
        target = self.name

        # Some systems we don't want to re-provision by accident.
        #
        if LabHW[target]['locked']:
            error('The system (%s) is locked and will not be provisioned.' % target)
            return False

        # If we are installing a HWE kernel, we want to install the correct series first.
        #
        if self.hwe:
            self.hwe_series = self.series
            self.series = HWE[self.series]['series']

        # We network boot/install the bare-metal hw to get our desired configuration on it.
        #
        provisioner = Configuration[Configuration['systems'][target]['provisioner']]
        if provisioner['type'] == 'cobbler':
            self.configure_orchestra(target)
            self.cycle_power(target)
        elif provisioner['type'] == 'maas':
            maas = MAAS(provisioner['profile'], provisioner['server'], provisioner['creds'])
            mt = maas.node(target)
            mt.stop_and_release()
            mt.series(self.series)
            mt.arch(self.arch)
            mt.acquire_and_start()
        else:
            error('Unrecognised provisioning type (%s)' % provisioner['type'])
            return False

        self.wait_for_system(target, timeout=60) # Allow 30 minutes for network installation

        # If we are installing via maas we are likely using the fastpath installer. That does
        # it's own reboot after installation. There is a window where we could think the system
        # is up but it's not really. Wait for a bit and then check for the system to be up
        # again.
        #
        if provisioner['type'] == 'maas':
            info("Giving it 5 more minutes")
            sleep(60 * 5) # Give it 5 minutes
            self.wait_for_system(target, timeout=60)

        if not self.target_verified(target, self.series, self.arch):
            info("Target verification failed.")
            return False

        # Once the initial installation has completed, we continue to install and update
        # packages so that we are testing the latest kernel, which is what we want.
        #
        if not self.ubuntu.is_development_series(self.series):
            self.enable_proposed(target, self.series)
        if self.ppa is not None:
            self.enable_ppa(target, self.series)
        if self.ubuntu.is_development_series(self.series):
            self.kernel_upgrade(target)
        else:
            self.dist_upgrade(target)
        self.mainline_firmware_hack(target)

        if self.hwe:
            self.install_hwe_kernel(target)

        if self.debs is not None:
            self.install_custom_debs(target)

        if provisioner['type'] == "cobbler":
            self.configure_passwordless_access(target)

        # We want to reboot to pick up any new kernel that we would have installed due
        # to either the dist-upgrade that was performed, or the install of the hwe
        # kernel.
        #
        self.reboot(target)
        return True

# vi:set ts=4 sw=4 expandtab syntax=python:
