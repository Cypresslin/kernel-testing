#!/usr/bin/env python
#
from sys                                import stdout
from os                                 import path
from logging                            import error
from datetime                           import datetime
from time                               import sleep
import re

#from lib.infrastructure                 import Orchestra, LabHW, MAASConfig
from lib.log                            import cdebug, cinfo
from lib.hwe                            import HWE
from lib.shell                          import sh, ShellError, ssh, Shell
from lib.ubuntu                         import Ubuntu
from lib.exceptions                     import ErrorExit
from lib.maas                           import MAAS, MAASCore
from lib.cobbler                        import Cobbler
from configuration                      import Configuration

# PS
#
# Provisioning Server
#
class PS(object):
    # __init__
    #
    def __init__(s, target, series, arch):
        cdebug("    Enter PS::__init__")
        sp = Configuration['systems'][target]['provisioner']
        p = Configuration[sp]
        for k in p:
            cdebug("        %16s : %s" % (k, p[k]))
            setattr(s, k, p[k])

        if s.type == "cobbler":
            s.server = Cobbler(target, series, arch)
        elif s.type == "maas":
            s.server = MAAS(s.profile, s.server, s.creds, target, series, arch)
        else:
            s.server = None
        cdebug("    Leave PS::__init__")

    # provision
    #
    def provision(s):
        return s.server.provision()

# Base
#
class Base(object):
    # __init__
    #
    def __init__(s, target, series, arch, hwe=False, debs=None, ppa=None, dry_run=False):
        cdebug("Enter Base::__init__")

        # If we are installing a HWE kernel, we want to install the correct series first.
        #
        if hwe:
            s.hwe_series = series
            series = HWE[series]['series']

        s.ps = PS(target, series, arch)
        s.target = target
        s.series = series
        s.arch = arch
        s.hwe = hwe
        s.debs = debs
        s.ppa  = ppa
        s.dry_run = dry_run
        s.progress_dots = 0
        s.progress_msg = ''
        cdebug("Leave Base::__init__")

    # progress
    #
    def progress(s, msg):
        dots = '.'
        s.progress_dots += 1
        prev_msg = s.progress_msg
        s.progress_msg = dots + ' ' + msg
        stdout.write(' ' + s.progress_msg + '\n')
        stdout.flush()

    # ssh
    #
    # This ssh method uses the lower-level ssh function for actuall remote shell to
    # the target system. This helper automatically provides the 'target' and 'user'
    # options to every ssh call.
    #
    def ssh(s, cmd, additional_ssh_options='', quiet=True, ignore_result=False):
        cdebug("Enter Base::ssh")
        result, output = Shell.ssh(s.target, cmd, user=s.ps.sut_user, additional_ssh_options=additional_ssh_options, quiet=quiet, ignore_result=ignore_result)
        cdebug("Leave Base::ssh")
        return result, output

    # prossh
    #
    # Helper for ssh'ing to the provisioning server.
    #
    def prossh(s, cmd, quiet=True, ignore_result=False, additional_ssh_options=''):
        cdebug("Enter Base::prossh")
        result, output = Shell.ssh(s.ps.server, cmd, additional_ssh_options=additional_ssh_options, user=s.ps.user, quiet=quiet, ignore_result=ignore_result)
        cdebug("Leave Base::prossh")
        return result, output

    # wait_for_target
    #
    def wait_for_target(s, timeout=10):
        cdebug('        Enter Base::wait_for_system_ex')

        start = datetime.utcnow()
        cinfo('Starting waiting for \'%s\' at %s' % (s.target, start))

        # Keep spinning until we either timeout or we get back some output from 'uname -vr'
        #
        while True:
            try:
                result, output = s.ssh('uname -vr')
                if result == 0 and len(output) > 0:
                    cdebug("             exit result is 0")
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
                    cdebug('        Leave Base::wait_for_system')
                    raise

            now = datetime.utcnow()
            delta = now - start
            if delta.seconds > timeout * 60:
                cinfo('Timed out at: %s' % now)
                raise ErrorExit('The specified timeout (%d) was reached while waiting for the target system (%s) to come back up.' % (timeout, s.target))

            sleep(60)
            cinfo('Checking at: %s' % datetime.utcnow())

        cdebug('        Leave Base::wait_for_system_ex')

    # install_hwe_kernel
    #
    def install_hwe_kernel(s):
        cdebug("        Enter Base::install_hwe_kernel")
        '''
        On the SUT, configure it to use a HWE kernel and then install the HWE
        kernel.
        '''
        # We add the x-swat ppa so we can pick up the development HWE kernel
        # if we want.
        #
        if 'ppa' in HWE[s.hwe_series]:
            s.ssh('sudo apt-get install --yes python-software-properties')
            s.ssh('sudo apt-add-repository ppa:ubuntu-x-swat/q-lts-backport')

        hwe_package = HWE[s.hwe_series]['package']
        s.ssh('sudo apt-get update')
        s.ssh('sudo DEBIAN_FRONTEND=noninteractive UCF_FORCE_CONFFNEW=1 apt-get install --yes %s' % (hwe_package))
        cdebug("        Leave Base::install_hwe_kernel")

    # reboot
    #
    def reboot(s, wait=True, quiet=True):
        '''
        Reboot the target system and wait 5 minutes for it to come up.
        '''
        cdebug('        Enter Base::reboot')
        s.ssh('sudo reboot', quiet=quiet)
        if wait:
            s.wait_for_target()
        cdebug('        Leave Base::reboot')

    # enable_proposed
    #
    def enable_proposed(s):
        '''
        On the target system, enable the -proposed archive pocket for the
        specified series.
        '''
        cdebug('        Enter Base::enable_proposed')
        s.ssh('\'echo deb http://us.archive.ubuntu.com/ubuntu/ %s-proposed restricted main multiverse universe | sudo tee -a /etc/apt/sources.list\'' % (s.series))
        cdebug('        Leave Base::enable_proposed')

    # enable_ppa
    #
    def enable_ppa(s):
        '''
        On the target system, enable the -proposed archive pocket for the
        specified series.
        '''
        cdebug('        Enter Base::enable_ppa')
        s.ssh('\'sudo apt-get -y install software-properties-common\'')
        s.ssh('\'sudo add-apt-repository -y %s\'' % (s.ppa))
        cdebug('        Leave Base::enable_ppa')

    # dist_upgrade
    #
    def dist_upgrade(s):
        '''
        Perform a update and dist-upgrade on a remote system.
        '''
        cdebug('        Enter Base::dist_upgrade')
        s.ssh('sudo apt-get update')
        s.ssh('sudo DEBIAN_FRONTEND=noninteractive UCF_FORCE_CONFFNEW=1 apt-get --yes dist-upgrade')
        cdebug('        Leave Base::dist_upgrade')

    # kernel_upgrade
    #
    def kernel_upgrade(s):
        '''
        Perform a update of the kernels on a remote system.
        '''
        cdebug('        Enter Base::kernel_upgrade')
        s.ssh('sudo apt-get update')
        s.ssh('sudo apt-get --yes install linux-image-generic linux-headers-generic')
        cdebug('        Leave Base::kernel_upgrade')

    # install_custom_debs
    #
    def install_custom_debs(s):
        '''
        On the SUT, download and install custome kernel debs for testing.
        '''
        cdebug('        Enter Base::install_custom_debs')
        # Pull them down
        #
        s.ssh('wget -r -A .deb -e robots=off -nv -l1 --no-directories %s' % s.debs)

        # Install everything
        #
        s.ssh('sudo dpkg -i *_all.deb *_%s.deb' % s.arch, ignore_result=True) # best effort
        cdebug('        Leave Base::install_custom_debs')

    # configure_passwordless_access
    #
    def configure_passwordless_access(s):
        result, out = sh('scp -r $HOME/.ssh %s:' % (s.target), ignore_result=True)
        if result > 0:
            error('****')
            error('**** Failed to scp .ssh to %s' % s.target)
            error(out)
            error('****')

    # mainline_firmware_hack
    #
    def mainline_firmware_hack(s):
        '''
        Mainline kernels look for their firmware in /lib/firmware and might miss other required firmware.
        '''
        cdebug('        Enter Metal::mainline_firmware_hack')
        s.ssh('sudo ln -s /lib/firmware/\$\(uname -r\)/* /lib/firmware/', ignore_result=True)
        cdebug('        Leave Metal::mainline_firmware_hack')

# Metal
#
# Every SUT has a 'bare-metal' component. Most of the time that _is_ the SUT and there
# is no other component. Sometimes the SUT is a VM which runs on 'bare-metal'.
#
class Metal(Base):
    # __init__
    #
    def __init__(s, target, series, arch, hwe=False, debs=None, ppa=None, dry_run=False):
        cdebug("Enter Metal::__init__")

        Base.__init__(s, target, series, arch, hwe=hwe, debs=debs, ppa=ppa, dry_run=dry_run)

        cdebug("Leave Metal::__init__")

    # verify_target
    #
    def verify_target(s):
        '''
        Confirm that the target system has installed what was supposed to be installed. If we asked for
        one series but another is on the system, fail.
        '''
        cdebug('        Enter Metal::verify_target')
        retval = False

        cdebug('            Verifying series:')
        result, codename = s.ssh(r'lsb_release --codename')
        for line in codename:
            line = line.strip()
            if line.startswith('Codename:'):
                cdebug('                lsb_release --codename : ' + line)
                if s.series not in line:
                    cinfo("")
                    cinfo("*** ERROR:")
                    cinfo("    Was expecting the target to be (%s) but found it to be (%s) instead." % (s.series, line.replace('Codename:\t','')))
                    cinfo("")
                else:
                    retval = True

        # Verify we installed the arch we intended to install
        #
        cdebug('            Verifying arch:')
        if retval:
            retval = False
            result, processor = s.ssh(r'uname -p')
            for line in processor:
                line = line.strip()
                cdebug('                uname -p : ' + line)

                if 'Warning: Permanently aded' in line: continue
                if line == '': continue

                if line == 'x86_64':
                    installed_arch = 'amd64'
                elif line == 'i686':
                    installed_arch = 'i386'
                else:
                    installed_arch = line

            if s.arch == installed_arch:
                retval = True
            else:
                cinfo("")
                cinfo("*** ERROR:")
                cinfo("    Was expecting the target to be (%s) but found it to be (%s) instead." % (s.arch, installed_arch))
                cinfo("")

        # Are we running the series correct kernel?
        #
        cdebug('            Verifying kernel:')
        if retval:
            retval = False
            kv = None
            result, kernel = s.ssh(r'uname -vr')
            for line in kernel:
                line = line.strip()
                cdebug('                uname -vr : ' + line)

                if 'Warning: Permanently aded' in line: continue
                if line == '': continue

                m = re.search('(\d+.\d+.\d+)-\d+-.* #(\d+)-Ubuntu.*', line)
                if m:
                    kv = m.group(1)
                cdebug('                kernel version : ' + kv)

            if kv is not None:
                installed_series = Ubuntu().lookup(kv)['name']

                if installed_series == s.series:
                    retval = True
                else:
                    cinfo("")
                    cinfo("*** ERROR:")
                    cinfo("    Was expecting the target to be (%s) but found it to be (%s) instead." % (s.series, installed_series))
                    cinfo("")
            else:
                cinfo("")
                cinfo("*** ERROR:")
                cinfo("    Unable to find the kernel version in any line.")

        cdebug('        Leave Metal::verify_target (%s)' % retval)
        return retval

    # verify_target
    #
    def verify_hwe_target(s):
        cdebug('        Enter Metal::verify_hwe_target')
        retval = True
        # Are we running the series correct kernel?
        #
        cdebug('            Verifying hwe kernel:')
        if retval:
            retval = False
            kv = None
            result, kernel = s.ssh(r'uname -vr')
            for line in kernel:
                line = line.strip()
                cdebug('                uname -vr : ' + line)

                if 'Warning: Permanently aded' in line: continue
                if line == '': continue

                m = re.search('(\d+.\d+.\d+)-\d+-.* #(\d+)\~\S+-Ubuntu.*', line)
                if m:
                    kv = m.group(1)
                cdebug('                kernel version : ' + kv)

            if kv is not None:
                installed_series = Ubuntu().lookup(kv)['name']

                if installed_series == s.hwe_series:
                    retval = True
                else:
                    cinfo("")
                    cinfo("*** ERROR:")
                    cinfo("    Was expecting the target to be (%s) but found it to be (%s) instead." % (s.series, installed_series))
                    cinfo("")
            else:
                cinfo("")
                cinfo("*** ERROR:")
                cinfo("    Unable to find the kernel version in any line.")
        cdebug('        Leave Metal::verify_hwe_target (%s)' % retval)
        return retval

    # provision
    #
    def provision(s):
        cdebug("Enter Metal::provision")

        s.progress('Provisioner setup')
        s.ps.provision()
        s.progress('Installing')
        s.wait_for_target(timeout=60) # Allow 30 minutes for network installation

        # If we are installing via maas we are likely using the fastpath installer. That does
        # it's own reboot after installation. There is a window where we could think the system
        # is up but it's not really. Wait for a bit and then check for the system to be up
        # again.
        #
        if s.ps.type == 'maas':
            cinfo("Giving it 5 more minutes")
            sleep(60 * 5) # Give it 5 minutes
            s.progress('Coming up')
            s.wait_for_target(timeout=60)
        cdebug("Leave Metal::provision")

        s.progress('Verifying base install')
        if not s.verify_target():
            cinfo("Target verification failed.")
            cdebug('Leave MetalProvisioner::provision')
            return False

        # If we want an HWE kernel installed on the bare metal then at this point the correct
        # LTS kernel has been installed and it's time to install the HWE kernel.
        #
        if s.hwe:
            s.progress('Installing HWE Kernel')
            s.install_hwe_kernel()
            s.progress('Rebooting for HWE Kernel')
            s.reboot()
            s.progress('Verifying HWE install')
            if not s.verify_hwe_target():
                cinfo("Target verification failed.")
                cdebug('Leave MetalProvisioner::provision')
                return False

        # Once the initial installation has completed, we continue to install and update
        # packages so that we are testing the latest kernel, which is what we want.
        #
        if not Ubuntu().is_development_series(s.series):
            s.progress('Enabling Proposed')
            s.enable_proposed()
        if s.ppa is not None:
            s.progress('Enabling PPA')
            s.enable_ppa()
        if Ubuntu().is_development_series(s.series):
            s.progress('Kernel Upgrade')
            s.kernel_upgrade()
        else:
            s.progress('Dist Upgrade')
            s.dist_upgrade()
        s.mainline_firmware_hack()

        if s.debs is not None:
            s.progress('Install custom debs')
            s.install_custom_debs()

        if s.ps.type == "cobbler":
            s.progress('Configure passwordless access')
            s.configure_passwordless_access()

        # We want to reboot to pick up any new kernel that we would have installed due
        # to either the dist-upgrade that was performed, or the install of the hwe
        # kernel.
        #
        s.reboot(s.target)
        s.progress('That\'s All Folks!')

        cdebug("Leave Metal::provision")

# SUT
#
class SUT(object):
    # __init__
    #
    def __init__(s):
        pass

# Provisioner
#
class Provisioner():

    _dry_run = False
    _quiet = False

    # __init__
    #
    def __init__(self, name, series, arch, hwe=False, debs=None, ppa=None, dry_run=False):
        cdebug('Enter Provisioner::__init__')
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

        self.target = name
        self.ps = PS(self.target)

        cdebug('Leave Provisioner::__init__')

    # enable_proposed
    #
    def enable_proposed(self, target, series):
        '''
        On the target system, enable the -proposed archive pocket for the
        specified series.
        '''
        cdebug('Enter Provisioner::enable_proposed')
        if not self.quiet:
            print('    enabling proposed')

        ssh(target, '\'echo deb http://us.archive.ubuntu.com/ubuntu/ %s-proposed restricted main multiverse universe | sudo tee -a /etc/apt/sources.list\'' % (series))
        cdebug('Leave Provisioner::enable_proposed')

    # enable_ppa
    #
    def enable_ppa(self, target, series):
        '''
        On the target system, enable the -proposed archive pocket for the
        specified series.
        '''
        cdebug('Enter Provisioner::enable_ppa')
        if not self.quiet:
            print('    enabling ppa %s' % self.ppa)
        ssh(target, '\'sudo apt-get -y install software-properties-common\'')
        ssh(target, '\'sudo add-apt-repository -y %s\'' % (self.ppa))
        cdebug('Leave Provisioner::enable_ppa')

    # dist_upgrade
    #
    def dist_upgrade(self, target):
        '''
        Perform a update and dist-upgrade on a remote system.
        '''
        cdebug('Enter Provisioner::dist_upgrade')
        ssh(target, 'sudo apt-get update')
        ssh(target, 'sudo apt-get --yes dist-upgrade')
        cdebug('Leave Provisioner::dist_upgrade')

    # kernel_upgrade
    #
    def kernel_upgrade(self, target):
        '''
        Perform a update of the kernels on a remote system.
        '''
        cdebug('Enter Provisioner::kernel_upgrade')
        ssh(target, 'sudo apt-get update')
        ssh(target, 'sudo apt-get --yes install linux-image-generic linux-headers-generic')
        cdebug('Leave Provisioner::kernel_upgrade')

    # mainline_firmware_hack
    #
    def mainline_firmware_hack(self, target):
        '''
        Mainline kernels look for their firmware in /lib/firmware and might miss other required firmware.
        '''
        cdebug('Enter Provisioner::mainline_firmware_hack')
        ssh(target, 'sudo ln -s /lib/firmware/\$\(uname -r\)/* /lib/firmware/', ignore_result=True)
        cdebug('Leave Provisioner::mainline_firmware_hack')

    # wait_for_system
    #
    @classmethod
    def wait_for_system(cls, target, user, timeout=10):
        cdebug('Enter Provisioner::wait_for_system')
        if not cls._dry_run:
            if not cls._quiet:
                print('Waiting for \'%s\' to come up.' % (target))

            start = datetime.utcnow()
            cinfo('Starting waiting for \'%s\' at %s' % (target, start))
            while True:
                try:
                    ssh_options = '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=quiet -qf'
                    result, output = sh('ssh %s %s@%s exit' % (ssh_options, user, target), quiet=True, ignore_result=True)
                    #result, output = ssh(target, '-qf exit', quiet=True, ignore_result=True)
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
                    cinfo('Timed out at: %s' % now)
                    raise ErrorExit('The specified timeout (%d) was reached while waiting for the target system (%s) to come back up.' % (timeout, target))

                sleep(60)
                cinfo('Checking at: %s' % datetime.utcnow())
        cdebug('Leave Provisioner::wait_for_system')

    # reboot
    #
    @classmethod
    def reboot(cls, target, user, wait=True, quiet=False):
        '''
        Reboot the target system and wait 5 minutes for it to come up.
        '''
        cdebug('Enter Provisioner::reboot')
        ssh(target, 'sudo reboot', quiet=quiet)
        if wait:
            cls.wait_for_system(target, user, timeout=10)
        cdebug('Leave Provisioner::reboot')

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

        o = Configuration['systems'][target]['provisioner']
        o_series = o['series'][self.series]
        o_arch   = o['arch'][self.arch]
        distro = '%s%s-%s' % (self.series, o_series['server distro decoration'], o_arch)
        kickstart = path.join(self.kickstarts_root, 'kt-virt-%s.preseed' % (o_series['preseed']))

        server = o['server']
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
        cdebug('Enter VirtualProvisioner::create_virtual_guest')
        p = Configuration['systems'][target]['provisioner']
        cdebug('    provisioner: %s' % p)
        pServer = Configuration[p]['system']
        cdebug('    pServer: %s' % pServer)
        ssh(target, 'sudo koan --virt --server=%s --profile=%s --virt-name=%s --virt-bridge=br0 --vm-poll' % (pServer, self.name, self.name))
        cdebug('Leave VirtualProvisioner::create_virtual_guest')

    # provision
    #
    def provision(self):
        target = self.name
        # If we are installing a HWE kernel, we want to install the correct series first.
        #
        if self.hwe:
            self.hwe_series = self.series
            self.series = HWE[self.series]['series']

        p = Configuration['systems'][target]['provisioner']
        user = Configuration[p]['sut-user']

        # We network boot/install the bare-metal hw to get our desired configuration on it.
        #
        self.configure_orchestra(self.virt_host)

        self.configure_host_for_virtual_guests(self.virt_host)
        self.create_virtual_guest(self.virt_host)

        # Once the initial installation has completed, we continue to install and update
        # packages so that we are testing the latest kernel, which is what we want.
        #
        self.wait_for_system(target, user, timeout=60) # Allow 30 minutes for network installation
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
        self.reboot(target, user)

        self.configure_passwordless_access(target, user)

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
        cdebug('Enter MetalProvisioner::configure_orchestra')
        cdebug('    target : %s' % target)
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
        cdebug('Leave MetalProvisioner::configure_orchestra')

    # cycle_power
    #
    def cycle_power(self, target):
        '''
        Has the smarts on how to go about turning the power off to a server
        remotely and then turning it back on. In some cases, multiple ports
        must be power cycled.
        '''
        cdebug('Enter MetalProvisioner::cycle_power')
        cdebug('    target : %s' % target)
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
        cdebug('Leave MetalProvisioner::cycle_power')

    # target_verified
    #
    def target_verified(self, target, user, series, arch):
        '''
        Confirm that the target system has installed what was supposed to be installed. If we asked for
        one series but another is on the system, fail.
        '''
        cdebug('Enter MetalProvisioner::target_verified')
        cdebug('    target : %s' % target)
        cdebug('    series : %s' % series)
        cdebug('      arch : %s' % arch)
        retval = False

        result, codename = ssh(target, r'lsb_release --codename', user=user)
        for line in codename:
            line = line.strip()
            if line.startswith('Codename:'):
                if series not in line:
                    cinfo("")
                    cinfo("*** ERROR:")
                    cinfo("    Was expecting the target to be (%s) but found it to be (%s) instead." % (series, line.replace('Codename:\t','')))
                    cinfo("")
                else:
                    retval = True

        # Verify we installed the arch we intended to install
        #
        if retval:
            retval = False
            result, processor = ssh(target, r'uname -p', user=user)
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
                cinfo("")
                cinfo("*** ERROR:")
                cinfo("    Was expecting the target to be (%s) but found it to be (%s) instead." % (arch, installed_arch))
                cinfo("")

        # Are we running the series correct kernel?
        #
        if retval:
            retval = False
            kv = None
            result, kernel = ssh(target, r'uname -vr', user=user)
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
                    cinfo("")
                    cinfo("*** ERROR:")
                    cinfo("    Was expecting the target to be (%s) but found it to be (%s) instead." % (series, installed_series))
                    cinfo("")
            else:
                cinfo("")
                cinfo("*** ERROR:")
                cinfo("    Unable to find the kernel version in any line.")

        cdebug('Leave MetalProvisioner::target_verified')
        return retval

    # provision
    #
    def provision(self):
        cdebug('Enter MetalProvisioner::provision')
        target = self.name

        # Some systems we don't want to re-provision by accident.
        #
        if Configuration['systems'][target]['locked']:
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
        user = provisioner['sut-user']
        if provisioner['type'] == 'cobbler':
            self.configure_orchestra(target)
            self.cycle_power(target)
        elif provisioner['type'] == 'maas':
            maas = MAASCore(provisioner['profile'], provisioner['server'], provisioner['creds'])
            mt = maas.node(target)
            mt.stop_and_release()
            mt.series(self.series)
            mt.arch(self.arch)
            mt.acquire_and_start()
        else:
            error('Unrecognised provisioning type (%s)' % provisioner['type'])
            return False

        self.wait_for_system(target, user, timeout=60) # Allow 30 minutes for network installation

        # If we are installing via maas we are likely using the fastpath installer. That does
        # it's own reboot after installation. There is a window where we could think the system
        # is up but it's not really. Wait for a bit and then check for the system to be up
        # again.
        #
        if provisioner['type'] == 'maas':
            cinfo("Giving it 5 more minutes")
            sleep(60 * 5) # Give it 5 minutes
            self.wait_for_system(target, user, timeout=60)

        if not self.target_verified(target, user, self.series, self.arch):
            cinfo("Target verification failed.")
            cdebug('Leave MetalProvisioner::provision')
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
        cdebug('Leave MetalProvisioner::provision')
        return True

# vi:set ts=4 sw=4 expandtab syntax=python:
