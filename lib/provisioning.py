#!/usr/bin/env python
#
from sys                                import stdout
from logging                            import error
from datetime                           import datetime
from time                               import sleep
import re

from lib.log                            import cdebug, cinfo, center, cleave
from lib.hwe                            import HWE
from lib.shell                          import ShellError, Shell
from lib.ubuntu                         import Ubuntu
from lib.exceptions                     import ErrorExit
from lib.maas                           import MAAS
from configuration                      import Configuration
from .kernel_debs                       import KernelDebs


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
            cdebug("++ %16s : %s" % (k, p[k]))
            setattr(s, k, p[k])

        if s.type == "maas":
            # Some systems/arches require a non-'generic' sub-arch. That information is specified
            # in the configuration information.
            #
            sub_arch = Configuration['systems'][target].get('sub-arch', 'generic')
            s.server = MAAS(s.profile, s.server, s.user, s.creds, target, series, arch, sub_arch)
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
    def __init__(s, target, series, arch, kernel=None, hwe=False, xen=False, debs=None, ppa=None, dry_run=False, lkp=False):
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
        s.lkp = lkp
        s.kernel = kernel
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
    def wait_for_target(s, progress=None, timeout=10):
        '''
        Wait for the remote system to come up far enough that we can start talking
        (ssh) to it.
        '''
        center('Base::wait_for_system_ex')

        if progress:
            s.progress(progress)

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

    # disable_apt_periodic_updates
    #
    def disable_apt_periodic_updates(s):
        center("Base::disable_apt_periodic_updates")
        s.progress('Disabling Periodic APT Updates')
        s.ssh(r'sudo sed -i \'s/s/APT::Periodic::Update-Package-Lists "1"/APT::Periodic::Update-Package-Lists "0"/\' /etc/apt/apt.conf.d/10periodic')
        cleave('Base::disable_apt_periodic_updates')

    # install_specific_kernel_version
    #
    def install_specific_kernel_version(s):
        '''
        '''
        center("Base::install_specific_kernel_version")
        s.progress('Installing Specific Kernel Version')

        kd = KernelDebs(s.kernel, s.series, s.arch)
        urls = kd.get_urls()
        if urls:
            for url in urls:
                cdebug(url, 'magenta')

                # Pull them down
                #
                s.ssh('wget -r -A .deb -e robots=off -nv -l1 --no-directories %s' % url, quiet=True)

            # Install them
            #
            s.ssh('sudo dpkg -i *.deb', ignore_result=True)

            # Remove all other kernels
            #
            purge_list = []
            m = re.search('(\d+.\d+.\d+-\d+).*', s.kernel)
            target = m.group(1)
            cdebug('target: %s' % target, 'cyan')
            result, output = s.ssh('dpkg -l \\\'linux-*\\\'', quiet=True)
            for l in output:
                if l.startswith('ii'):
                    if 'linux-headers' in l or 'linux-image' in l:  # Only interested in kernel packages
                        if target not in l:                         # Ignore lines that contain the kernel version we are specifically targeting
                            info = l.split()
                            package = info[1]
                            if any(char.isdigit() for char in package):
                                purge_list.append(package)

            cdebug('Kernel packages to be purged:')
            for p in purge_list:
                cdebug('    %s' % p)

            for p in purge_list:
                s.ssh('sudo apt-get purge --yes %s' % p, quiet=True)

            s.ssh('sudo update-grub', quiet=True)
        else:
            raise ErrorExit('Failed to get the urls for the spcified kernel version (%s)' % s.kernel)

        cleave("Base::install_specific_kernel_version")

    # enable_live_kernel_patching
    #
    def enable_live_kernel_patching(s):
        center("Base::enable_live_kernel_patching")
        s.progress('Enabling Live Kernel Patching')
        cleave('Base::enable_live_kernel_patching')

    # install_required_pkgs
    #
    def install_required_pkgs(s):
        '''
        '''
        center("Base::install_required_pkgs")
        s.progress('Installing Required Packages')

        s.ssh('sudo apt-get install --yes python-yaml')

        cleave("Base::install_required_pkgs")

    # install_hwe_kernel
    #
    def install_hwe_kernel(s):
        '''
        On the SUT, configure it to use a HWE kernel and then install the HWE
        kernel.
        '''
        center("Base::install_hwe_kernel")
        s.progress('Installing HWE Kernel')

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
        s.progress('Installing Xen Kernel')
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
    def reboot(s, progress=None, wait=True, quiet=True):
        '''
        Reboot the target system and wait 5 minutes for it to come up.
        '''
        center('Base::reboot')
        if progress:
            s.progress(progress)

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
        center('Base::enable_src')
        s.progress('Enabling Src')
        s.ssh('\'cat /etc/apt/sources.list | sed "s/^deb /deb-src /" | sudo tee -a /etc/apt/sources.list\'')
        cleave('Base::enable_src')

    # enable_proposed
    #
    def enable_proposed(s):
        '''
        On the target system, enable the -proposed archive pocket for the
        specified series.
        '''
        center('Base::enable_proposed')
        s.progress('Enabling Proposed')
        s.ssh('\'grep %s /etc/apt/sources.list | sed s/%s/%s-proposed/ | sudo tee -a /etc/apt/sources.list\'' % (s.series, s.series, s.series))
        cleave('Base::enable_proposed')

    # enable_ppa
    #
    def enable_ppa(s):
        '''
        On the target system, enable the -proposed archive pocket for the
        specified series.
        '''
        center('Base::enable_ppa')
        s.progress('Enabling PPA')
        s.ssh('\'sudo apt-get -y install software-properties-common\'')
        if s.ppa.startswith('ppa:'):
            s.ssh('\'sudo add-apt-repository -y %s\'' % (s.ppa))
        else:
            s.ssh('\'sudo add-apt-repository -y ppa:%s\'' % (s.ppa))
        cleave('Base::enable_ppa')

    # dist_upgrade
    #
    def dist_upgrade(s):
        '''
        Perform a update and dist-upgrade on a remote system.
        '''
        center('Base::dist_upgrade')
        s.progress('Dist Upgrade')
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
        s.progress('Kernel Upgrade')
        s.ssh('sudo apt-get update', ignore_result=True)
        s.ssh('sudo apt-get --yes install linux-image-generic linux-headers-generic')
        cleave('Base::kernel_upgrade')

    # install_python_minimal
    #
    def install_python_minimal(s):
        '''
        From Wily onward, python 2 is no longer installed.
        '''
        center('Base::install_python_minimal')
        s.progress('Installing python-minimal')
        s.ssh('sudo apt-get --yes install python-minimal', ignore_result=True)
        cleave('Base::install_python_minimal')

    # install_custom_debs
    #
    def install_custom_debs(s):
        '''
        On the SUT, download and install custome kernel debs for testing.
        '''
        center('Base::install_custom_debs')
        s.progress('Install custom debs')
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
    def __init__(s, target, series, arch, kernel=None, hwe=False, xen=False, debs=None, ppa=None, dry_run=False, lkp=False):
        center("Metal::__init__")

        Base.__init__(s, target, series, arch, kernel=kernel, hwe=hwe, xen=xen, debs=debs, ppa=ppa, dry_run=dry_run, lkp=lkp)

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
        s.progress('Verifying base install')

        cdebug('Verifying series:')
        result, codename = s.ssh(r'lsb_release --codename')
        for line in codename:
            line = line.strip()
            if line.startswith('Codename:'):
                cdebug('lsb_release --codename : ' + line)
                print('         series: ' + line.replace('Codename:', '').strip())
                if s.series not in line:
                    error("")
                    error("*** ERROR:")
                    error("    Was expecting the target to be (%s) but found it to be (%s) instead." % (s.series, line.replace('Codename:\t', '')))
                    error("")
                else:
                    retval = True

        # Verify we installed the arch we intended to install
        #
        cdebug('Verifying arch:')
        if retval:
            retval = False
            installed_arch = 'unknown'
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
                elif line == 'aarch64':
                    installed_arch = 'arm64'
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

                m = re.search('(\d+.\d+.\d+-\d+)-.* #(\d+)-Ubuntu.*', line)
                if m:
                    installed_kernel = '%s.%s' % (m.group(1), m.group(2))
                cdebug('installed kernel version : ' + installed_kernel)

            print('         kernel: ' + installed_kernel)
            retval = True
            if kv is not None:
                installed_series = Ubuntu().lookup(kv)['name']

                if installed_series == s.series:
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

            if s.kernel is not None:
                if installed_kernel == s.kernel:
                    retval = True
                else:
                    retval = False
                    error("")
                    error("*** ERROR:")
                    error("    Was expecting the target kernel version to be (%s) but found it to be (%s) instead." % (s.kernel, installed_kernel))
                    error("")

        cleave('Metal::verify_target (%s)' % retval)
        return retval

    # verify_hwe_target
    #
    def verify_hwe_target(s):
        center('Metal::verify_hwe_target')
        retval = True
        s.progress('Verifying HWE install')
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
        s.progress('Verifying Xen install')

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
        s.wait_for_target(progress='Installing', timeout=60)  # Allow 30 minutes for network installation

        # If we are installing via maas we are likely using the fastpath installer. That does
        # it's own reboot after installation. There is a window where we could think the system
        # is up but it's not really. Wait for a bit and then check for the system to be up
        # again.
        #
        if s.ps.type == 'maas':
            cinfo("Giving it 5 more minutes")
            sleep(60 * 3)  # Give it 3 minutes
            s.wait_for_target(progress='Coming up', timeout=60)

        # The very first thing we need to do is make our changes to the apt sources and then dist-upgrade
        # the system. Once we do this the kernels that we install should be the right one.
        #
        s.enable_proposed()
        s.enable_src()
        if s.ppa is not None:
            s.enable_ppa()
        s.dist_upgrade()

        # Disable APT from periodicly running and trying to update the systems.
        #
        s.disable_apt_periodic_updates()

        # If we want an HWE kernel installed on the bare metal then at this point the correct
        # LTS kernel has been installed and it's time to install the HWE kernel.
        #
        if s.hwe:
            s.install_hwe_kernel()
            s.reboot(progress='Rebooting for HWE Kernel')                    # reboot
            if not s.verify_hwe_target():
                cinfo("Target verification failed.")
                cdebug('Leave Metal::provision')
                return False

        if s.xen:
            s.install_xen()
            s.reboot(progress='Rebooting for Xen Kernel')                    # reboot
            if not s.verify_xen_target():
                cinfo("Target verification failed.")
                cleave('Metal::provision')
                return False

        if s.debs is not None:
            s.install_custom_debs()
            s.reboot(progress='Rebooting for custom dbes')                   # reboot

        if s.kernel:
            s.install_specific_kernel_version()
            s.reboot(progress='Rebooting for Kernel version %s' % s.kernel)  # reboot

        if Ubuntu().is_development_series(s.series):
            s.kernel_upgrade()
            s.reboot(progress='Rebooting for development series kernel')     # reboot
        s.mainline_firmware_hack()

        s.progress('Verifying the running kernel version')
        if not s.verify_target():
            cinfo("Target verification failed.")
            cleave('Metal::provision')
            return False

        if s.lkp:
            s.enable_live_kernel_patching()

        s.install_python_minimal()
        s.install_required_pkgs()

        # We want to reboot to pick up any new kernel that we would have installed due
        # to either the dist-upgrade that was performed, or the install of the hwe
        # kernel.
        #
        s.reboot(s.target)
        s.progress('That\'s All Folks!')

        cleave("Metal::provision")
        return True

# vi:set ts=4 sw=4 expandtab syntax=python:
