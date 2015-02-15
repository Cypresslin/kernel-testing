#!/usr/bin/env python
#
from sys                                import stdout
from os                                 import path
from logging                            import error
from datetime                           import datetime
from time                               import sleep
import re

#from lib.infrastructure                 import Orchestra, LabHW, MAASConfig
from lib.log                            import cdebug, cinfo, center, cleave
from lib.hwe                            import HWE
from lib.shell                          import sh, ShellError, ssh, Shell
from lib.ubuntu                         import Ubuntu
from lib.exceptions                     import ErrorExit
from lib.maas                           import MAAS
from configuration                      import Configuration

# PS
#
# Provisioning Server
#
class PS(object):
    # __init__
    #
    def __init__(s, target, series, arch):
        center("PS::__init__")
        sp = Configuration['systems'][target]['provisioner']
        p = Configuration[sp]
        for k in p:
            cdebug("%16s : %s" % (k, p[k]))
            setattr(s, k, p[k])

        if s.type == "maas":
            s.server = MAAS(s.profile, s.server, s.creds, target, series, arch)
        else:
            s.server = None
        cleave("PS::__init__")

    # provision
    #
    def provision(s):
        return s.server.provision()

# Base
#
class Base(object):
    # __init__
    #
    def __init__(s, target, series, arch, hwe=False, xen=False, debs=None, ppa=None, dry_run=False):
        center("Base::__init__")

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
        s.xen = xen
        s.debs = debs
        s.ppa  = ppa
        s.dry_run = dry_run
        s.progress_dots = 0
        s.progress_msg = ''

        cleave("Base::__init__")

    # progress
    #
    def progress(s, msg):
        '''
        Simple 'progress' messages sent to stdout to give the user some feeling that something
        is happening.
        '''
        dots = '.'
        s.progress_dots += 1
        prev_msg = s.progress_msg
        s.progress_msg = dots + ' ' + msg
        stdout.write(' ' + s.progress_msg + '\n')
        stdout.flush()

    # ssh
    #
    def ssh(s, cmd, additional_ssh_options='', quiet=True, ignore_result=False):
        '''
        This ssh method uses the lower-level ssh function for actuall remote shell to
        the target system. This helper automatically provides the 'target' and 'user'
        options to every ssh call.
        '''
        center("Base::ssh")
        result, output = Shell.ssh(s.target, cmd, user=s.ps.sut_user, additional_ssh_options=additional_ssh_options, quiet=quiet, ignore_result=ignore_result)
        cleave("Base::ssh")
        return result, output

    # prossh
    #
    #
    def prossh(s, cmd, quiet=True, ignore_result=False, additional_ssh_options=''):
        '''
        Helper for ssh'ing to the provisioning server. This is done a lot with the
        same options over and over.
        '''
        center("Base::prossh")
        result, output = Shell.ssh(s.ps.server, cmd, additional_ssh_options=additional_ssh_options, user=s.ps.user, quiet=quiet, ignore_result=ignore_result)
        cleave("Base::prossh (%d)" % result)
        return result, output

    # wait_for_target
    #
    def wait_for_target(s, timeout=10):
        '''
        Wait for the remote system to come up far enough that we can start talking
        (ssh) to it.
        '''
        center('Base::wait_for_system_ex')

        start = datetime.utcnow()
        cinfo('Starting waiting for \'%s\' at %s' % (s.target, start))

        # Keep spinning until we either timeout or we get back some output from 'uname -vr'
        #
        while True:
            try:
                result, output = s.ssh('uname -vr')
                if result == 0 and len(output) > 0:
                    cdebug("exit result is 0")
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
                    cleave('Base::wait_for_system')
                    raise

            now = datetime.utcnow()
            delta = now - start
            if delta.seconds > timeout * 60:
                cinfo('Timed out at: %s' % now)
                raise ErrorExit('The specified timeout (%d) was reached while waiting for the target system (%s) to come back up.' % (timeout, s.target))

            sleep(60)
            cinfo('Checking at: %s' % datetime.utcnow())

        cleave('Base::wait_for_system_ex')

    # install_hwe_kernel
    #
    def install_hwe_kernel(s):
        '''
        On the SUT, configure it to use a HWE kernel and then install the HWE
        kernel.
        '''
        center("Base::install_hwe_kernel")
        # We add the x-swat ppa so we can pick up the development HWE kernel
        # if we want.
        #
        if 'ppa' in HWE[s.hwe_series]:
            s.ssh('sudo apt-get install --yes python-software-properties')
            s.ssh('sudo apt-add-repository ppa:ubuntu-x-swat/q-lts-backport')

        hwe_package = HWE[s.hwe_series]['package']
        s.ssh('sudo apt-get update', ignore_result=True)
        s.ssh('sudo DEBIAN_FRONTEND=noninteractive UCF_FORCE_CONFFNEW=1 apt-get install --yes %s' % (hwe_package))
        cleave("Base::install_hwe_kernel")

    # install_xen
    #
    def install_xen(s):
        '''
        Configure the remote system as a xen host.
        '''
        center("        Enter Base::install_xen")
        if s.series == 'lucid':
            cdebug("Can't do lucid")
        elif s.series == 'precise':
            cdebug("Doing it the hard way")
            # Do it the hard way
            #
            s.ssh('sudo apt-get update', ignore_result=True)
            s.ssh('sudo apt-get install --yes xen-hypervisor', ignore_result=True)
            s.ssh(r'sudo sed -i \'s/GRUB_DEFAULT=.*\\+/GRUB_DEFAULT=\"Xen 4.1-amd64\"/\' /etc/default/grub')
            s.ssh(r'sudo sed -i \'s/GRUB_CMDLINE_LINUX=.*\\+/GRUB_CMDLINE_LINUX=\"apparmor=0\"/\' /etc/default/grub')
            s.ssh(r'sudo sed -i \'s/GRUB_CMDLINE_LINUX_DEFAULT=\"\"/GRUB_CMDLINE_LINUX_DEFAULT=\"\"\\nGRUB_CMDLINE_XEN=\""dom0_mem=1G,max:1G dom0_max_vcpus=1\""/\' /etc/default/grub')
            s.ssh('sudo update-grub')
        else:
            cdebug("Doing it the easy way")
            s.ssh('sudo apt-get update', ignore_result=True)
            s.ssh('sudo apt-get install --yes xen-hypervisor-amd64', ignore_result=True)
        cleave("        Leave Base::install_xen")

    # reboot
    #
    def reboot(s, wait=True, quiet=True):
        '''
        Reboot the target system and wait 5 minutes for it to come up.
        '''
        center('Base::reboot')
        s.ssh('sudo reboot', quiet=quiet)
        if wait:
            s.wait_for_target()
        cleave('Base::reboot')

    # enable_src
    #
    def enable_src(s):
        '''
        On the target system, enable the src packages specified series.
        '''
        center('Base::enable_proposed')
        s.progress('Enabling Src')
        if s.arch == 'ppc64el': # This really should be a generic 'if s.arch in s.ports:'
            s.ssh('\'echo deb-src http://ports.ubuntu.com/ubuntu-ports/ %s restricted main multiverse universe | sudo tee -a /etc/apt/sources.list\'' % (s.series))
            s.ssh('\'echo deb-src http://ports.ubuntu.com/ubuntu-ports/ %s-updates restricted main multiverse universe | sudo tee -a /etc/apt/sources.list\'' % (s.series))
            s.ssh('\'echo deb-src http://ports.ubuntu.com/ubuntu-ports/ %s-security restricted main multiverse universe | sudo tee -a /etc/apt/sources.list\'' % (s.series))
        else:
            s.ssh('\'echo deb-src http://us.archive.ubuntu.com/ubuntu/ %s restricted main multiverse universe | sudo tee -a /etc/apt/sources.list\'' % (s.series))
            s.ssh('\'echo deb-src http://us.archive.ubuntu.com/ubuntu/ %s-updates restricted main multiverse universe | sudo tee -a /etc/apt/sources.list\'' % (s.series))
            s.ssh('\'echo deb-src http://us.archive.ubuntu.com/ubuntu/ %s-security restricted main multiverse universe | sudo tee -a /etc/apt/sources.list\'' % (s.series))
        cleave('Base::enable_proposed')

    # enable_proposed
    #
    def enable_proposed(s):
        '''
        On the target system, enable the -proposed archive pocket for the
        specified series.
        '''
        center('Base::enable_proposed')
        if s.arch == 'ppc64el': # This really should be a generic 'if s.arch in s.ports:'
            s.ssh('\'echo deb http://ports.ubuntu.com/ubuntu-ports/ %s-proposed restricted main multiverse universe | sudo tee -a /etc/apt/sources.list\'' % (s.series))
        else:
            s.ssh('\'echo deb http://us.archive.ubuntu.com/ubuntu/ %s-proposed restricted main multiverse universe | sudo tee -a /etc/apt/sources.list\'' % (s.series))
        cleave('Base::enable_proposed')

    # enable_ppa
    #
    def enable_ppa(s):
        '''
        On the target system, enable the -proposed archive pocket for the
        specified series.
        '''
        center('Base::enable_ppa')
        s.ssh('\'sudo apt-get -y install software-properties-common\'')
        s.ssh('\'sudo add-apt-repository -y %s\'' % (s.ppa))
        cleave('Base::enable_ppa')

    # dist_upgrade
    #
    def dist_upgrade(s):
        '''
        Perform a update and dist-upgrade on a remote system.
        '''
        center('Base::dist_upgrade')
        s.ssh('sudo apt-get update', ignore_result=True)
        s.ssh('sudo DEBIAN_FRONTEND=noninteractive UCF_FORCE_CONFFNEW=1 apt-get --yes dist-upgrade')
        cleave('Base::dist_upgrade')

    # kernel_upgrade
    #
    def kernel_upgrade(s):
        '''
        Perform a update of the kernels on a remote system.
        '''
        center('Base::kernel_upgrade')
        s.ssh('sudo apt-get update', ignore_result=True)
        s.ssh('sudo apt-get --yes install linux-image-generic linux-headers-generic')
        cleave('Base::kernel_upgrade')

    # install_custom_debs
    #
    def install_custom_debs(s):
        '''
        On the SUT, download and install custome kernel debs for testing.
        '''
        center('Base::install_custom_debs')
        # Pull them down
        #
        s.ssh('wget -r -A .deb -e robots=off -nv -l1 --no-directories %s' % s.debs)

        # Install everything
        #
        s.ssh('sudo dpkg -i *_all.deb *_%s.deb' % s.arch, ignore_result=True) # best effort
        cleave('Base::install_custom_debs')

    # mainline_firmware_hack
    #
    def mainline_firmware_hack(s):
        '''
        Mainline kernels look for their firmware in /lib/firmware and might miss other required firmware.
        '''
        center('Base::mainline_firmware_hack')
        s.ssh('sudo ln -s /lib/firmware/\$\(uname -r\)/* /lib/firmware/', ignore_result=True)
        cleave('Base::mainline_firmware_hack')

# Metal
#
# Every SUT has a 'bare-metal' component. Most of the time that _is_ the SUT and there
# is no other component. Sometimes the SUT is a VM which runs on 'bare-metal'.
#
class Metal(Base):
    # __init__
    #
    def __init__(s, target, series, arch, hwe=False, xen=False, debs=None, ppa=None, dry_run=False):
        center("Metal::__init__")

        Base.__init__(s, target, series, arch, hwe=hwe, xen=xen, debs=debs, ppa=ppa, dry_run=dry_run)

        cleave("Metal::__init__")

    # verify_target
    #
    def verify_target(s):
        '''
        Confirm that the target system has installed what was supposed to be installed. If we asked for
        one series but another is on the system, fail.
        '''
        center('Metal::verify_target')
        retval = False

        cdebug('Verifying series:')
        result, codename = s.ssh(r'lsb_release --codename')
        for line in codename:
            line = line.strip()
            if line.startswith('Codename:'):
                cdebug('lsb_release --codename : ' + line)
                print('         series: ' + line.replace('Codename:','').strip())
                if s.series not in line:
                    error("")
                    error("*** ERROR:")
                    error("    Was expecting the target to be (%s) but found it to be (%s) instead." % (s.series, line.replace('Codename:\t','')))
                    error("")
                else:
                    retval = True

        # Verify we installed the arch we intended to install
        #
        cdebug('Verifying arch:')
        if retval:
            retval = False
            result, processor = s.ssh(r'uname -p')
            for line in processor:
                line = line.strip()
                cdebug('uname -p : ' + line)

                if 'Warning: Permanently aded' in line: continue
                if line == '': continue

                if line == 'x86_64':
                    installed_arch = 'amd64'
                elif line == 'i686':
                    installed_arch = 'i386'
                elif line == 'athlon':
                    installed_arch = 'i386'
                else:
                    installed_arch = line

            print('         arch: ' + installed_arch)
            if s.arch == installed_arch:
                retval = True
            # Special case for Power8 (ppc64el)
            #
            elif s.arch == 'ppc64el' and installed_arch == 'ppc64le':
                retval = True
            else:
                error("")
                error("*** ERROR:")
                error("    Was expecting the target to be (%s) but found it to be (%s) instead." % (s.arch, installed_arch))
                error("")

        # Are we running the series correct kernel?
        #
        cdebug('Verifying kernel:')
        if retval:
            retval = False
            kv = None
            result, kernel = s.ssh(r'uname -vr')
            for line in kernel:
                line = line.strip()
                cdebug('uname -vr : ' + line)

                if 'Warning: Permanently aded' in line: continue
                if line == '': continue

                m = re.search('(\d+.\d+.\d+)-\d+-.* #(\d+)-Ubuntu.*', line)
                if m:
                    kv = m.group(1)
                cdebug('kernel version : ' + kv)

            print('         kernel: ' + kv)
            retval = True
            #if kv is not None:
            #    installed_series = Ubuntu().lookup(kv)['name']

            #    if installed_series == s.series:
            #        retval = True
            #    else:
            #        error("")
            #        error("*** ERROR:")
            #        error("    Was expecting the target to be (%s) but found it to be (%s) instead." % (s.series, installed_series))
            #        error("")
            #else:
            #    error("")
            #    error("*** ERROR:")
            #    error("    Unable to find the kernel version in any line.")
            #    error("")

        cleave('Metal::verify_target (%s)' % retval)
        return retval

    # verify_hwe_target
    #
    def verify_hwe_target(s):
        center('Metal::verify_hwe_target')
        retval = True
        # Are we running the series correct kernel?
        #
        cdebug('Verifying hwe kernel:')
        if retval:
            retval = False
            kv = None
            result, kernel = s.ssh(r'uname -vr')
            for line in kernel:
                line = line.strip()
                cdebug('uname -vr : ' + line)

                if 'Warning: Permanently aded' in line: continue
                if line == '': continue

                m = re.search('(\d+.\d+.\d+)-\d+-.* #(\d+)\~\S+-Ubuntu.*', line)
                if m:
                    kv = m.group(1)
                    cdebug('kernel version : ' + kv)

            if kv is not None:
                installed_series = Ubuntu().lookup(kv)['name']

                if installed_series == s.hwe_series:
                    retval = True
                else:
                    error("")
                    error("*** ERROR:")
                    error("    Was expecting the target to be (%s) but found it to be (%s) instead." % (s.series, installed_series))
                    error("")
            else:
                error("")
                error("*** ERROR:")
                error("    Unable to find the kernel version in any line.")
                error("")
                for line in kernel:
                    line = line.strip()
                    error("    line: %s" % line)

        cleave('Metal::verify_hwe_target (%s)' % retval)
        return retval

    # verify_xen_target
    #
    def verify_xen_target(s):
        center('Metal::verify_xen_target')
        retval = False

        if s.series == 'lucid':
            cdebug("Can't do lucid")
        elif s.series == 'precise':
            result, output = s.ssh('sudo xm list')
            for line in output:
                line = line.strip()
                if 'Domain-0' in line:
                    retval = True
                    break
        else:
            result, output = s.ssh('sudo xl list')
            for line in output:
                line = line.strip()
                if 'Domain-0' in line:
                    retval = True
                    break
        if not retval:
            error("")
            error("Failed to find the Domain-0 domain.")
            error("")

        cleave('Metal::verify_xen_target (%s)' % retval)
        return retval

    # provision
    #
    def provision(s):
        center("Enter Metal::provision")

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
            sleep(60 * 3) # Give it 5 minutes
            s.progress('Coming up')
            s.wait_for_target(timeout=60)

        s.progress('Verifying base install')
        if not s.verify_target():
            cinfo("Target verification failed.")
            cleave('Metal::provision')
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
            #if not s.verify_hwe_target():
            #    cinfo("Target verification failed.")
            #    cdebug('Leave Metal::provision')
            #    return False

        if s.xen:
            s.progress('Installing Xen Kernel')
            s.install_xen()
            s.progress('Rebooting for Xen Kernel')
            s.reboot()
            s.progress('Verifying Xen install')
            if not s.verify_xen_target():
                cinfo("Target verification failed.")
                cleave('Metal::provision')
                return False

        # Once the initial installation has completed, we continue to install and update
        # packages so that we are testing the latest kernel, which is what we want.
        #
        s.enable_src()
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

        # We want to reboot to pick up any new kernel that we would have installed due
        # to either the dist-upgrade that was performed, or the install of the hwe
        # kernel.
        #
        s.reboot(s.target)
        s.progress('That\'s All Folks!')

        cleave("Metal::provision")
        return True

# vi:set ts=4 sw=4 expandtab syntax=python:
