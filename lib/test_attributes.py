#!/usr/bin/env python
#

from sys                                import argv
from os                                 import environ, path
import platform
import re
from  subprocess                        import Popen, PIPE
from datetime                           import datetime

from lib.dbg                            import Dbg
from lib.utils                          import date_to_string
from lib.shell                          import sh, ShellError

# TestAttributes
#
class TestAttributes():
    """
    """

    # __init__
    #
    def __init__(self, cfg):
        Dbg.enter("TestAttributes.__init__")

        self.cfg    = cfg

        Dbg.leave("TestAttributes.__init__")

    def kernel_version(self):
        m = re.match('^(\d+\.\d+\.\d+[\.-][\drc]+)-?(.*)$', platform.release())
        version = m.group(1)
        flavour = m.group(2)

        m = re.match('^#(\d+.*?)(-Ubuntu)* .*$', platform.version())
        upload = m.group(1)

        retval = "%s.%s" % (version, upload)
        return retval, flavour

    def distro_release(self):
        p = Popen(['lsb_release', '-sir'], stdout=PIPE, stderr=PIPE, close_fds=True)
        retval = p.communicate()[0].strip().replace('\n', ' ')
        return retval

    def distro_release_name(self):
        p = Popen(['lsb_release', '-c'], stdout=PIPE, stderr=PIPE, close_fds=True)
        retval = p.communicate()[0].strip().split()[-1]
        return retval

    def kind_of_hardware(self):
        retval = 'real'
        with open('/proc/cpuinfo', 'r') as f:
            line = f.readline()
            while line:
                if 'model name' in line:
                    if 'QEMU Virtual CPU' in line:
                        retval = 'virtual'
                    break
                line = f.readline()
        return retval

    def virt_host_kernel_version(self, vhost):
        retval = ''
        p = Popen(['ssh', vhost, 'uname', '-vr'], stdout=PIPE, stderr=PIPE, close_fds=True)
        results = p.communicate()[0].strip().replace('\n', ' ')
        if results is not None:
            m = re.search('(\d+.\d+.\d+-\d+-).* #(\d+)-Ubuntu.*', results)
            if m:
                retval = '%s%s' % (m.group(1), m.group(2))
        return retval

    def livepatch_package_version(self):

        retval = '0.0'
        try:
            import yaml

            result, output = sh('sudo canonical-livepatch status', quiet=True)
            status = yaml.safe_load(''.join(output))
            for k in status:
                if k['livepatch']['installed'] is True:
                    retval = k['livepatch']['version']
        except ShellError:
            # For whatever reason it failed (probably not present) just ignore the failure.
            #
            pass

        except ImportError:
            # The ADT tests do not have a dependency on yaml and so the import will fail.
            # Since we are not doing livepatch package testing as part of ADT we will just
            # ignore the issue and continue.
            #
            pass

        return retval

    # gather
    #
    def gather(self):
        Dbg.enter("TestAttributes.main")

        data = {}

        # Timestamp
        #
        # Obtaining the timestamp from the system that was just provisioned is not reliable. The
        # true timestamp is obtained on the jenkins system and passed in as the _TS_ env variable.
        #
        if '_TS_' in environ:
            data['timestamp'] = environ['_TS_']
        else:
            data['timestamp'] = 'unknown'

        # TestAttributes the environment variables.
        #
        data['environ'] = {}
        for e in environ:
            data['environ'][e] = environ[e]

        # TestAttributes platform data.
        #
        data['platform'] = {}
        data['platform']['arch'] = {}
        (data['platform']['arch']['bits'], data['platform']['arch']['linkage']) = platform.architecture()

        data['platform']['libc'] = {}
        (data['platform']['libc']['lib'], data['platform']['libc']['version']) = platform.libc_ver()


        data['platform']['machine']  = platform.machine()
        data['platform']['proc']     = platform.processor()
        data['platform']['hostname'] = platform.node()

        data['platform']['hardware'] = self.kind_of_hardware()
        #if data['platform']['hardware'] == 'virtual':
        #    if self.cfg.vh_name != '':
        #        data['virt host'] = {
        #            'kernel version' : self.virt_host_kernel_version(self.cfg.vh_name),
        #            'name' : self.cfg.vh_name,
        #        }

        data['kernel'], data['kernel-flavour'] = self.kernel_version()
        data['distro-release'] = self.distro_release()
        data['distro-release-name'] = self.distro_release_name()

        data['livepatch-package-version'] = self.livepatch_package_version()

        Dbg.leave("TestAttributes.main")
        return data

# vi:set ts=4 sw=4 expandtab:

