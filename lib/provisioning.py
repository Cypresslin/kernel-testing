#!/usr/bin/env python
#
from sys                                import stdout, argv
from os                                 import path
from logging                            import error
from datetime                           import datetime
from time                               import sleep
from logging                            import getLogger, CRITICAL
import re
import yaml
import json

from lib.log                            import cdebug, cinfo, center, cleave
from lib3.shell                         import ShellError, Shell
from lib.ubuntu                         import Ubuntu
from lib.exceptions                     import ErrorExit
from lib.maas                           import MAAS
from lib.juju                           import JuJu
from .configuration                     import Configuration
from .kernel_debs                       import KernelDebs


def logging_off():
    logger = getLogger()
    level = logger.getEffectiveLevel()
    logger.setLevel(CRITICAL)
    return level

def logging_on(level):
    logger = getLogger()
    logger.setLevel(level)

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
            s.server = MAAS(s.server, s.creds, target, p['domain'], series, arch, flavour=sub_arch, api=s.api)
        elif s.type == "juju":
            domain = Configuration['systems'][target]['domain']
            cloud  = Configuration['systems'][target]['cloud']
            s.server = JuJu(cloud, target, series, domain=domain)
        else:
            s.server = None
        cleave("PS::__init__")

    # provision
    #
    def provision(s):
        level = logging_off()
        retval = s.server.provision()
        logging_on(level)
        return retval


# Base
#
class Base(object):
    # __init__
    #
    def __init__(s, target, series, arch, kernel=None, xen=False, debs=None, ppa=None, dry_run=False, lkp=False, lkp_snappy=False, pkg_name=None, required_kernel_version=None, flavour=None):
        center("Base::__init__")

        s.ps = PS(target, series, arch)

        sp = Configuration['systems'][target]['provisioner']
        p = Configuration[sp]
        if s.ps.type == "maas":
            s.target = '%s.%s' % (target, p['domain'])
        else:
            s.target = target
        s.raw_target = target

        s.series = series
        s.arch = arch
        s.xen = xen
        s.debs = debs
        s.ppa  = ppa
        s.lkp = lkp
        s.lkp_snappy = lkp_snappy
        s.kernel = kernel
        s.flavour = flavour
        s.pkg_name = pkg_name
        s.required_kernel_version = required_kernel_version
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
    def wait_for_target(s, progress=None, timeout=30):
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
                result, output = s.ssh('uname -vr', additional_ssh_options="-o BatchMode=yes")
                if result == 0 and len(output) > 0:
                    for l in output:
                        cdebug(l)
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
        s.ssh(r'sudo sed -i \'s/APT::Periodic::Update-Package-Lists "1"/APT::Periodic::Update-Package-Lists "0"/\' /etc/apt/apt.conf.d/10periodic')
        cleave('Base::disable_apt_periodic_updates')

    # install_kernel_flavour
    #
    def install_kernel_flavour(s):
        '''
        '''
        center("Base::install_kernel_flavour")
        s.progress('Installing %s Kernel Flavour' % s.flavour)

        extras = {}
        try:
            fid = path.join(path.dirname(argv[0]), 'flavour-extras')
            with open(fid, 'r') as stream:
                extras = yaml.safe_load(stream)
        except FileNotFoundError as e:
            print('Exception thrown and ignored. Did not find a flavour-extras file.')
            print(fid)
            pass # Ignore the error

        if s.flavour in extras:
            if 'key' in extras[s.flavour]['ppa']:
                for line in extras[s.flavour]['ppa']['key']:
                    cmd = '\'echo \"%s\" | sudo tee -a /tmp/%s.key\'' % (line, s.flavour)
                    s.ssh(cmd)
                cmd = 'sudo apt-key add /tmp/%s.key' % s.flavour
                s.ssh(cmd)

            if 'subscription' in extras[s.flavour]['ppa']:
                for line in extras[s.flavour]['ppa']['subscription']:
                    cmd = '\'echo \"%s\" | sudo tee -a /etc/apt/sources.list.d/%s.list\'' % (line, s.flavour)
                    s.ssh(cmd)

            s.ssh('sudo apt-get update', ignore_result=True)

            if 'packages' in extras[s.flavour]:
                for package in extras[s.flavour]['packages']:
                    p = package.replace('%v', '.'.join(s.required_kernel_version.split('.')[0:-1]))
                    cmd = 'sudo apt-get install --yes %s' % p
                    s.ssh(cmd)

        elif s.flavour in ['lowlatency', 'kvm']:
            cmd = 'sudo apt-get install --yes linux-%s' % s.flavour
            s.ssh(cmd)

        cleave("Base::install_kernel_flavour")

    # install_specific_kernel_version
    #
    def install_specific_kernel_version(s):
        '''
        '''
        center("Base::install_specific_kernel_version")
        s.progress('Installing Specific Kernel Version')

        kd = KernelDebs(s.kernel, s.series, s.arch, s.flavour)
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

        s.ssh('sudo touch /etc/apt/sources.list.d/canonical-livepatch.list')
        # FIXME: bjf - Need to use a kernel team config server for this
        #
        p = path.join(path.dirname(argv[0]), 'canonical-livepatch.list')
        with open(p, 'r') as f:
            for l in f.read().split('\n'):
                s.ssh('\'echo \"%s\" | sudo tee -a /etc/apt/sources.list.d/canonical-livepatch.list\'' % l)

        s.ssh('sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 74603F44')
        s.ssh('sudo apt-get update')
        s.ssh('sudo apt-get install canonical-livepatch')
        sleep(60) # Give the livepatch daemon a minute to calm down

        s.ssh(r'sudo sed -i \'s/1/48/\' /etc/default/canonical-livepatch')
        s.ssh('sudo canonical-livepatch update')

        cleave('Base::enable_live_kernel_patching')

    def customize_rc_local(s):
        center("Base::customize_rc_local")
        rc = [
            '#!/bin/sh -e',
            '#',
            '',
            'systemctl mask apt-daily.service',
            'systemctl mask apt-daily.timer',
            'systemctl mask apt-daily-upgrade.service',
            'systemctl mask apt-daily-upgrade.timer',
            'exit 0',
        ]

        s.ssh('sudo rm /etc/rc.local')
        s.ssh('sudo touch /etc/rc.local')
        for l in rc:
            s.ssh('\'echo \"%s\" | sudo tee -a /etc/rc.local\'' % l)
        s.ssh('sudo chmod 0755 /etc/rc.local')

        cleave("Base::customize_rc_local")

    def enable_snappy_client_live_kernel_patching(s):
        center("Base::enable_snappy_client_live_kernel_patching")
        s.progress('Enabling Live Kernel Snap Client Patching')

        # teach snapd about the proxys
        s.ssh('cp /etc/environment /tmp/environment.tmp')
        s.ssh('\'echo http_proxy=\"http://squid.internal:3128\" >> /tmp/environment.tmp\'')
        s.ssh('\'echo https_proxy=\"http://squid.internal:3128\" >> /tmp/environment.tmp\'')
        s.ssh('sudo cp /tmp/environment.tmp /etc/environment')
        s.ssh('sudo service snapd restart')

        # grab livepatch client from snap store
        (result, output) = s.ssh('sudo snap install --beta canonical-livepatch')
        if result != 0:
            raise ErrorExit("Failed to install canonical-livepatch snap")

        # Ensure all interfaces are connected
        s.ssh('sudo snap connect canonical-livepatch:kernel-module-control ubuntu-core:kernel-module-control')
        s.ssh('sudo snap connect canonical-livepatch:hardware-observe ubuntu-core:hardware-observe')
        s.ssh('sudo snap connect canonical-livepatch:system-observe ubuntu-core:system-observe')
        s.ssh('sudo snap connect canonical-livepatch:network-control ubuntu-core:network-control')
        s.ssh('sudo service snap.canonical-livepatch.canonical-livepatchd restart')

        # Get the auth key and enable it
        key = Configuration['systems'][s.raw_target]['livepatch key']
        (result, output) = s.ssh('sudo canonical-livepatch enable %s' % key)
        if result != 0:
            raise ErrorExit("Failed to enable canonical-livepatch key for %s" % s.raw_target)
        sleep(60)
        (result, output) = s.ssh('sudo canonical-livepatch status --verbose')
        (result, output) = s.ssh('lsmod')
        found_module = False
        for l in output:
            cdebug(l)
            if 'livepatch' in l:
                found_module = True
                break
        if found_module == False:
            raise ErrorExit("Could not find livepatch kernel module")

        cleave("Base::enable_snappy_client_live_kernel_patching")

    # install_required_pkgs
    #
    def install_required_pkgs(s):
        '''
        '''
        center("Base::install_required_pkgs")
        s.progress('Installing Required Packages')

        pkgs = [
            'python-yaml',
            'gdb',
        ]
        s.ssh('sudo apt-get install --yes %s' % ' '.join(pkgs))

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

        s.ssh('sudo apt-get update', ignore_result=True)
        s.ssh('sudo DEBIAN_FRONTEND=noninteractive UCF_FORCE_CONFFNEW=1 apt-get install --yes %s' % (s.pkg_name))

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
        sleep(30)                       # Got the "Connection to <host> close by remote host" but was able
                                        # to immediately get a valid "uname -vr" which shouldn't have happened.
        if wait:
            s.wait_for_target()
        cleave('Base::reboot')

    # fixup_hosts
    #
    def fixup_hosts(s):
        center('Base::fixup_hosts')
        s.progress('Fixup /etc/hosts')
        s.ssh('sudo sed -i -e \\\'/localhost/a 127.0.1.1 %s %s\\\' /etc/hosts' % (s.raw_target, s.target), quiet=False, ignore_result=False)
        cleave('Base::fixup_hosts')

    # remove_90curtin_aptproxy
    #
    def remove_90curtin_aptproxy(s):
        '''
        '''
        center('Base::remove_90curtin_aptproxy')
        s.progress('Remove /etc/apt/apt.conf.d/90curtin-aptproxy')

        # Don't use the proxy that MAAS sets up.
        #
        s.ssh('sudo rm -f /etc/apt/apt.conf.d/90curtin-aptproxy', quiet=False)

        s.ssh('sudo apt-get update', ignore_result=True)
        cleave('Base::remove_90curtin_aptproxy')

    # fixup_apt_sources
    #
    def fixup_apt_sources(s):
        '''
        '''
        center('Base::fixup_apt_sources')
        s.progress('Fixup /etc/apt/sources.list')

        # Don't use the proxy that MAAS sets up.
        #
        s.ssh('sudo rm -f /etc/apt/apt.conf.d/90curtin-aptproxy', quiet=False)

        # Make sure we are using the us archive, it should be faster
        #
        s.ssh('\'cat /etc/apt/sources.list | sed "s/\/archive\./\/us.archive./" | sudo tee /etc/apt/sources.list\'')

        s.ssh('sudo apt-get update', ignore_result=True)
        cleave('Base::fixup_apt_sources')

    # enable_src
    #
    def enable_src(s):
        '''
        On the target system, enable the src packages specified series.
        '''
        center('Base::enable_src')
        s.progress('Enabling Src')
        s.ssh('\'cat /etc/apt/sources.list | sed "s/^deb /deb-src /" | sudo tee -a /etc/apt/sources.list\'')
        s.ssh('sudo apt-get update', ignore_result=True)
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
        s.ssh('\'grep "%s main" /etc/apt/sources.list | sed s/\ %s\ /\ %s-proposed\ / | sudo tee -a /etc/apt/sources.list\'' % (s.series, s.series, s.series))
        s.ssh('sudo apt-get update', ignore_result=True)
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

        extras = {}
        try:
            fid = path.join(path.dirname(argv[0]), 'ppa-extras')
            with open(fid, 'r') as stream:
                extras = yaml.safe_load(stream)
        except FileNotFoundError as e:
            print('Exception thrown and ignored. Did not find a flavour-extras file.')
            print(fid)
            pass # Ignore the error

        if s.ppa in extras:
            if 'key' in extras[s.ppa]:
                cmd = "sudo touch /tmp/ppa.key"
                s.ssh(cmd)
                for line in extras[s.ppa]['key']:
                    cmd = '\'echo \"%s\" | sudo tee -a /tmp/ppa.key\'' % (line)
                    s.ssh(cmd)
                cmd = 'sudo apt-key add /tmp/ppa.key'
                s.ssh(cmd)

            if 'subscription' in extras[s.ppa]:
                for line in extras[s.ppa]['subscription']:
                    cmd = '\'echo \"%s\" | sudo tee -a /etc/apt/sources.list.d/%s.list\'' % (line, s.flavour)
                    s.ssh(cmd)
        else:
            s.ssh('\'sudo apt-get -y install software-properties-common\'')
            try:
                if s.ppa.startswith('ppa:'):
                    s.ssh('\'sudo add-apt-repository -y %s\'' % (s.ppa))
                else:
                    s.ssh('\'sudo add-apt-repository -y ppa:%s\'' % (s.ppa))
            except:
                raise ErrorExit('Failed to add the ppa.')
        s.ssh('sudo apt-get update', ignore_result=True)
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
        s.ssh('sudo apt-get -f install --yes --force-yes', ignore_result=True)
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
    def __init__(s, target, series, arch, kernel=None, xen=False, debs=None, ppa=None, dry_run=False, lkp=False, lkp_snappy=False, pkg_name=None, required_kernel_version=None, flavour='generic'):
        center("Metal::__init__")

        Base.__init__(s, target, series, arch, kernel=kernel, xen=xen, debs=debs, ppa=ppa, dry_run=dry_run, lkp=lkp, lkp_snappy=lkp_snappy, pkg_name=pkg_name, required_kernel_version=required_kernel_version, flavour=flavour)

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
        found = False
        result, codename = s.ssh(r'lsb_release --codename', quiet=False)
        for line in codename:
            line = line.strip()
            if line.startswith('Codename:'):
                found = True
                cdebug('lsb_release --codename : ' + line)
                print('         series: ' + line.replace('Codename:', '').strip())
                if s.series not in line:
                    error("")
                    error("*** ERROR:")
                    error("    Was expecting the target to be (%s) but found it to be (%s) instead." % (s.series, line.replace('Codename:\t', '')))
                    error("")
                else:
                    retval = True
        if not found:
            error("")
            error("*** ERROR:")
            error("    No output lines were found containing 'Codename:'")
            error("")


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
            # Specical case for s390x (s390x.zVM, s390x.zKVM)
            #
            elif s.arch.startswith(installed_arch) and installed_arch == 's390x':
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
            installed_kernel = None
            result, kernel = s.ssh(r'uname -vr')
            for line in kernel:
                line = line.strip()
                cdebug('uname -vr : ' + line)

                if 'Warning: Permanently aded' in line: continue
                if line == '': continue

                m = re.search('(\d+.\d+.\d+)-\d+-.* #(\d+[+~a-z\d.]*)-Ubuntu.*', line)
                if m:
                    kv = m.group(1)
                cdebug('kernel version : ' + kv)

                m = re.search('(\d+.\d+.\d+-\d+)-.* #(\d+[+~a-z\d.]*)-Ubuntu.*', line)
                if m:
                    installed_kernel = '%s.%s' % (m.group(1), m.group(2))
                cdebug('installed kernel version : ' + installed_kernel)

            if installed_kernel is not None:
                if s.required_kernel_version is not None:
                    if installed_kernel == s.required_kernel_version:
                        retval = True
                    else:
                        retval = False
                        error("")
                        error("*** ERROR:")
                        error("    Was expecting the target kernel version to be (%s) but found it to be (%s) instead." % (s.required_kernel_version, installed_kernel))
                        error("")
                else:
                    retval = True
                    cdebug("Didn't ask for a specific kernel, skipping the version check.")
            else:
                retval = False
                error("")
                error("*** ERROR:")
                error("    Unable to determine the installed kernel version.")
                error("")

        cleave('Metal::verify_target (%s)' % retval)
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

        dist_upgrade = None
        reboot = None
        retval = False

        # If the provisioning type is "manual" then the system has been setup by hand however,
        # go ahead and dist-upgrade it.
        #
        if s.ps.type == "manual":
            # s.dist_upgrade()
            s.reboot(progress="Rebooting for dist-upgrade")
            # As we don't run dist_upgrade() here, it's better to verify the kerenl version first
            if s.xen:
                if not s.verify_xen_target():
                    cinfo("Target verification failed.")
                else:
                    retval = True
            else:
                if not s.verify_target():
                    cinfo("Target verification failed.")
                else:
                    retval = True
            return retval

        s.progress('Provisioner setup')
        if not s.ps.provision():
            raise ErrorExit('Failed to provision the system')

        sleep(60 * 5)

        s.fixup_hosts()

        # The very first thing we need to do is make our changes to the apt sources and then dist-upgrade
        # the system. Once we do this the kernels that we install should be the right one.
        #
        # s.fixup_apt_sources() # This is breaking some systems
        # Do not remove 90curtin_aptproxy on hyper-maas, it will break the route to outer world
        if Configuration['systems'][s.raw_target]['provisioner'] != 'hyper-maas':
            s.remove_90curtin_aptproxy()
        s.enable_proposed()
        s.enable_src()
        if s.ppa is not None:
            s.enable_ppa()
            dist_upgrade = True

        s.customize_rc_local()
        s.reboot(progress="for the pure love of rebooting")

        # Disable APT from periodicly running and trying to update the systems.
        #
        s.disable_apt_periodic_updates()

        # If we want an HWE kernel installed on the bare metal then at this point the correct
        # LTS kernel has been installed and it's time to install the HWE kernel.
        #
        if s.required_kernel_version and '~' in s.required_kernel_version:
            s.install_hwe_kernel()
            reboot = 'Rebooting for HWE Kernel'

        if s.xen:
            s.install_xen()
            reboot = 'Rebooting for Xen Kernel'

        if s.debs is not None:
            s.install_custom_debs()
            reboot = 'Rebooting for custom debs'

        # We *always* enable proposed. However, for development series kernels
        # we only update the kernel packages.
        #
        if Ubuntu().is_development_series(s.series):
            s.kernel_upgrade()
            reboot = 'Rebooting for development series kernel'
        else:
            dist_upgrade = True

        s.mainline_firmware_hack()

        s.install_python_minimal()
        s.install_required_pkgs()

        if dist_upgrade:
            s.dist_upgrade()
            if not reboot:
                reboot = 'Rebooting for dist-upgrade'

        if s.flavour != 'generic':
            s.install_kernel_flavour()
            reboot = 'Rebooting for Kernel flavour %s' % s.flavour

        if s.kernel:
            s.install_specific_kernel_version()
            reboot = 'Rebooting for Kernel version %s' % s.kernel

        if reboot:
            s.reboot(progress=reboot)

        if s.lkp:
            s.enable_live_kernel_patching()
        elif s.lkp_snappy:
            s.enable_snappy_client_live_kernel_patching()

        s.progress('Verifying the running kernel version')
        if s.xen:
            if not s.verify_xen_target():
                cinfo("Target verification failed.")
            else:
                retval = True
        else:
            if not s.verify_target():
                cinfo("Target verification failed.")
            else:
                retval = True

        s.progress('That\'s All Folks!')

        cleave("Metal::provision (%s)" % (retval))
        return retval

# vi:set ts=4 sw=4 expandtab syntax=python:
