#!/usr/bin/env python
#
from sys                                import stdout, argv
from os                                 import path
from logging                            import error
from datetime                           import datetime
from time                               import sleep
import re
import yaml

from lib.log                            import cdebug, cinfo, center, cleave
from lib.hwe                            import HWE
from lib3.shell                         import ShellError, Shell
from lib.ubuntu                         import Ubuntu
from lib.exceptions                     import ErrorExit

# Base
#
class Base(object):
    # __init__
    #
    def __init__(s, target, series, arch, kernel=None, hwe=False, debs=None, ppa=None, dry_run=False, lkp=False, lkp_snappy=False, required_kernel_version=None, flavour=None, ssh_options=None, ssh_user='ubuntu'):
        center("Base::__init__")

        # If we are installing a HWE kernel, we want to install the correct series first.
        #
        if hwe:
            s.hwe_series = series
            series = HWE[series]['series']

        s.target = target
        s.raw_target = target

        s.series = series
        s.arch = arch
        s.hwe = hwe
        s.debs = debs
        s.ppa  = ppa
        s.lkp = lkp
        s.kernel = kernel
        s.lkp_snappy = lkp_snappy
        s.flavour = flavour
        s.required_kernel_version = required_kernel_version
        s.dry_run = dry_run
        s.progress_dots = 0
        s.progress_msg = ''
        s.ssh_options = ssh_options
        s.ssh_user = ssh_user

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
        if s.ssh_options is not None:
            additional_ssh_options += ' ' + s.ssh_options
        result, output = Shell.ssh(s.target, cmd, user=s.ssh_user, additional_ssh_options=additional_ssh_options, quiet=quiet, ignore_result=ignore_result)
        cleave("Base::ssh")
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
                result, output = s.ssh('uname -vr', additional_ssh_options="-o BatchMode=yes -o LogLevel=quiet")
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
        s.ssh(r'sudo sed -i \'s/APT::Periodic::Update-Package-Lists "1"/APT::Periodic::Update-Package-Lists "0"/\' /etc/apt/apt.conf.d/10periodic')
        cleave('Base::disable_apt_periodic_updates')

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

        hwe_package = HWE[s.hwe_series]['package']
        s.ssh('sudo apt-get update', ignore_result=True)
        s.ssh('sudo DEBIAN_FRONTEND=noninteractive UCF_FORCE_CONFFNEW=1 apt-get install --yes %s' % (hwe_package))

        cleave("Base::install_hwe_kernel")

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
        except FileNotFoundError:
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

        else: # s.flavour in ['lowlatency', 'aws', 'azure', 'gke']:
            cmd = 'sudo apt-get install --yes linux-%s' % s.flavour
            s.ssh(cmd)

        cleave("Base::install_kernel_flavour")

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

    # fixup_hosts
    #
    def fixup_hosts(s):
        center('Base::fixup_hosts')
        s.progress('Fixup /etc/hosts')
        s.ssh('sudo sed -i -e \\\'/localhost/a 127.0.1.1 %s %s\\\' /etc/hosts' % (s.raw_target, s.target), quiet=False, ignore_result=False)
        cleave('Base::fixup_hosts')

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
        s.ssh('\'grep "%s universe" /etc/apt/sources.list | sed s/\ %s\ /\ %s-proposed\ / | sudo tee -a /etc/apt/sources.list\'' % (s.series, s.series, s.series))
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
        s.ssh('\'sudo apt-get -y install software-properties-common\'')
        if s.ppa.startswith('ppa:'):
            s.ssh('\'sudo add-apt-repository -y %s\'' % (s.ppa))
        else:
            s.ssh('\'sudo add-apt-repository -y ppa:%s\'' % (s.ppa))
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
        s.ssh('sudo DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::="--force-confnew" --assume-yes -fuy dist-upgrade')

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
        s.ssh('sudo apt-get -f install --yes --assume-yes', ignore_result=True)
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


# Target
#
# Every SUT has a 'bare-metal' component. Most of the time that _is_ the SUT and there
# is no other component. Sometimes the SUT is a VM which runs on 'bare-metal'.
#
class Target(Base):
    # __init__
    #
    def __init__(s, target, series, arch, kernel=None, hwe=False, debs=None, ppa=None, dry_run=False, lkp=False, lkp_snappy=False, required_kernel_version=None, flavour='generic', ssh_options=None, ssh_user='ubuntu'):
        center("Target::__init__")

        Base.__init__(s, target, series, arch, kernel=kernel, hwe=hwe, debs=debs, ppa=ppa, dry_run=dry_run, lkp=lkp, lkp_snappy=lkp_snappy, required_kernel_version=required_kernel_version, flavour=flavour, ssh_options=ssh_options, ssh_user=ssh_user)

        cleave("Target::__init__")

    # verify_target
    #
    def verify_target(s):
        '''
        Confirm that the target system has installed what was supposed to be installed. If we asked for
        one series but another is on the system, fail.
        '''
        center('Target::verify_target')
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
            result, kernel = s.ssh(r'uname -vr', additional_ssh_options="-o LogLevel=quiet")
            for line in kernel:
                line = line.strip()
                print('uname -vr : ' + line)

                if 'Warning: Permanently added' in line: continue
                if line == '': continue

                m = re.search('(\d+.\d+.\d+)-\d+-.* #(\d+[~a-z\d.]*)-Ubuntu.*', line)
                if m:
                    kv = m.group(1)
                cdebug('kernel version : ' + kv)

                m = re.search('(\d+.\d+.\d+-\d+)-.* #(\d+[~a-z\d.]*)-Ubuntu.*', line)
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
                error("")
                error("*** ERROR:")
                error("    Required kernel version is None")
                error("")

        cleave('Target::verify_target (%s)' % retval)
        return retval

    # verify_hwe_target
    #
    def verify_hwe_target(s):
        center('Target::verify_hwe_target')
        retval = True
        s.progress('Verifying HWE install')
        # Are we running the series correct kernel?
        #
        cdebug('Verifying hwe kernel:')
        if retval:
            retval = False
            kv = None
            result, kernel = s.ssh(r'uname -vr', additional_ssh_options="-o LogLevel=quiet")
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

        cleave('Target::verify_hwe_target (%s)' % retval)
        return retval

    # provision
    #
    def provision(s):
        center("Target::provision")

        reboot = None
        retval = False

        s.fixup_hosts()

        # The very first thing we need to do is make our changes to the apt sources and then dist-upgrade
        # the system. Once we do this the kernels that we install should be the right one.
        #
        s.fixup_apt_sources()
        s.enable_proposed()
        # s.enable_src()
        if s.ppa is not None:
            s.enable_ppa()

        # Disable APT from periodicly running and trying to update the systems.
        #
        s.disable_apt_periodic_updates()

        # If we want an HWE kernel installed on the bare metal then at this point the correct
        # LTS kernel has been installed and it's time to install the HWE kernel.
        #
        if s.hwe:
            s.install_hwe_kernel()
            reboot = 'Rebooting for HWE Kernel'

        if s.debs is not None:
            s.install_custom_debs()
            reboot = 'Rebooting for custom debs'

        if s.flavour == 'generic':
            s.kernel_upgrade()
            reboot = 'Reboot for kenel update'
        if s.flavour != 'generic':
            s.install_kernel_flavour()
            reboot = 'Rebooting for Kernel flavour %s' % s.flavour

        s.mainline_firmware_hack()

        s.install_python_minimal()
        s.install_required_pkgs()

        if reboot:
            s.reboot(progress=reboot)

        if s.lkp:
            s.enable_live_kernel_patching()

        s.progress('Verifying the running kernel version')
        if not s.verify_target():
            cinfo("Target verification failed.")
        else:
            retval = True

        s.progress('That\'s All Folks!')

        cleave("Target::provision (%s)" % (retval))
        return retval

# vi:set ts=4 sw=4 expandtab syntax=python:
