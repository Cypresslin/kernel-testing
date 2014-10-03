#!/usr/bin/env python
#

from os                                 import getenv, path
from lib.argparse                       import ArgumentParser, RawDescriptionHelpFormatter
from logging                            import error, info, basicConfig, DEBUG, WARNING, INFO

from lib.log                            import cdebug, Clog, cerror
from lib.shell                          import ShellError, ShellTimeoutError, sh, ssh, Shell
from lib.provisioning                   import MetalProvisioner, VirtualProvisioner, Metal, PS
from lib.exceptions                     import ErrorExit
from lib.hwe                            import HWE
from lib.configuration                  import Configuration
from lib.ubuntu                         import Ubuntu

# ProvApp
#
class ProvApp(object):
    '''
    Handle all the tasks for getting a test system fully up and installed and ready for
    running the kernel tests.
    '''

    # __init__
    #
    def __init__(self):
        self.__hwdb = None

    def produce_error_results(self, workspace, msg):
        with open(path.join(workspace, 'kernel-results.xml'), 'w') as f:
            f.write('<testsuites>\n')
            f.write('    <testsuite tests="1" errors="1" name="Provisioning" timestamp="2012-01-01" hostname="hostname" time="0" failures="0">\n')
            f.write('        <properties/>\n')
            f.write('        <testcase classname="Provisioning.Initial-Provisioning" name="provisioning" time="0.0">\n')
            f.write('            <error message="Provisioning failed!" type="Logparse">\n')
            f.write(msg)
            f.write('\n')
            f.write('            </error>\n')
            f.write('        </testcase>\n')
            f.write('    </testsuite>\n')
            f.write('</testsuites>\n')

    # target_verified
    #
    def target_verified(self, target, series):
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

        return retval

    # validate_args
    #
    # Makes sure the command line options specified will actually work with the targetted system.
    #
    def validate_args(s, args):
        cdebug("    Enter ProvApp::validate_args")

        if args.sut == 'real':
            if args.sut_name not in Configuration['systems']:
                cdebug("        raising ErrorExit exception")
                raise ErrorExit('The name (%s) is not a recognized system. Valid systems are:\n    %s' % (args.sut_name, '\n    '.join(Configuration['systems'].keys())))

            # Some systems we don't want to re-provision by accident.
            #
            if Configuration['systems'][args.sut_name]['locked']:
                raise ErrorExit('The system (%s) is locked and will not be provisioned.' % args.sut_name)

            target = Configuration['systems'][args.sut_name]
            # Does the hw arch match that of what was specified on the command line?
            #
            if args.sut_arch not in target['arch']:
                raise ErrorExit('The arch (%s) is not valid for the system (%s). Valid arches for that system are:\n    %s' % (args.sut_arch, args.sut_name, '\n    '.join(target['arch'])))

            # NOTE: The following check is disabled while HWE continues to 'support' quantal and saucy.
            #
            ## Is the specified series a valid, supported series?
            ##
            #supported = []
            #for s in Ubuntu.index_by_series_name:
            #    try:
            #        if Ubuntu.index_by_series_name[s]['supported'] or Ubuntu.index_by_series_name[s]['development']:
            #            supported.append(s)
            #    except KeyError as e:
            #        pass

            #if args.sut_series not in supported:
            #    raise ErrorExit('The series (%s) is not a recognized, supported series. Valid series are:\n    %s' % (args.sut_series, '\n    '.join(supported)))

            if args.sut_hwe:
                if HWE[args.sut_series]['series'] is None:
                    raise ErrorExit('The series (%s) does not have a HWE version.' % (args.sut_series))

        if args.sut == 'virtual':
            if args.vh_name not in Configuration['systems']:
                cdebug("        raising ErrorExit exception")
                raise ErrorExit('The name (%s) is not a recognized system. Valid systems are:\n    %s' % (args.vh_name, '\n    '.join(Configuration['systems'].keys())))

            # Some systems we don't want to re-provision by accident.
            #
            if Configuration['systems'][args.sut_name]['locked']:
                raise ErrorExit('The system (%s) is locked and will not be provisioned.' % args.sut_name)

            # NOTE: The following check is disabled while HWE continues to 'support' quantal and saucy.
            #
            ## Is the specified series a valid, supported series?
            ##
            #supported = []
            #for s in Ubuntu.index_by_series_name:
            #    try:
            #        if Ubuntu.index_by_series_name[s]['supported'] or Ubuntu.index_by_series_name[s]['development']:
            #            supported.append(s)
            #    except KeyError as e:
            #        pass

            #if args.sut_series not in supported:
            #    raise ErrorExit('The series (%s) is not a recognized, supported series. Valid series are:\n    %s' % (args.sut_series, '\n    '.join(supported)))

            if args.vh_hwe:
                if HWE[args.vh_series]['series'] is None:
                    raise ErrorExit('The series (%s) does not have a HWE version.' % (args.vh_series))
        cdebug("    Leave ProvApp::validate_args")

    # neo
    #
    def neo(s, args):
        cdebug("Enter ProvApp::neo")
        retval = 1
        try:
            s.validate_args(args)
            metal = Metal(args.sut_name, args.sut_series, args.sut_arch, args.sut_hwe, args.sut_debs_url, ppa=args.ppa, dry_run=args.dry_run)
            metal.provision()
            result, output = metal.prossh('id')

        except ErrorExit as e:
            error(e.message)
            ws = getenv('WORKSPACE')
            if ws is not None:
                s.produce_error_results(ws, e.message)
            pass

        cdebug("Leave ProvApp::neo (%d)" % retval)
        return retval

    # main
    #
    def main(s, args):
        cdebug("Enter ProvApp::main")
        retval = 1
        try:
            metal = None
            if args.sut == 'real':
                metal = MetalProvisioner(args.sut_name, args.sut_series, args.sut_arch, args.sut_hwe, args.sut_debs_url, ppa=args.ppa, dry_run=args.dry_run)
                metal.provision()

                if args.sut_hwe:
                    targeted_series = HWE[args.sut_series]['series']
                else:
                    targeted_series = args.sut_series

                if s.target_verified(args.sut_name, targeted_series):
                    retval = 0
            else:
                info("=========================================================================")
                info("=")
                info("=                   V I R T U A L   H O S T")
                info("=")
                info("=========================================================================")
                metal = MetalProvisioner(args.vh_name, args.vh_series, args.vh_arch, args.vh_hwe, dry_run=args.dry_run)
                metal.provision()
                if s.target_verified(args.vh_name, args.vh_series):
                    info("=========================================================================")
                    info("=")
                    info("=                   V I R T U A L   C L I E N T")
                    info("=")
                    info("=========================================================================")
                    virt = VirtualProvisioner(args.vh_name, args.sut_name, args.sut_series, args.sut_arch, args.sut_hwe, dry_run=args.dry_run)
                    virt.provision()

                    if args.sut_hwe:
                        targeted_series = HWE[args.sut_series]['series']
                    else:
                        targeted_series = args.sut_series

                    if s.target_verified(args.sut_name, targeted_series):
                        retval = 0

        # Handle the user presses <ctrl-C>.
        #
        except KeyboardInterrupt:
            print("Aborting ...")

        except ShellTimeoutError as e:
            msg = 'The command (%s) timed out. (%d)' % (e.cmd, e.timeout)
            ws = getenv('WORKSPACE')
            if ws is not None:
                s.produce_error_results(ws, msg)
            error(msg)

        except ShellError as e:
            msg = 'The command (%s) returned a non-zero exit status (%d).\n' % (e.cmd, e.returncode)
            for line in e.output:
                msg += line.rstrip() + '\n'

            error('The command (%s) returned a non-zero exit status (%d).' % (e.cmd, e.returncode))
            for line in e.output:
                error(line.rstrip())

            ws = getenv('WORKSPACE')
            if ws is not None:
                s.produce_error_results(ws, msg)

        except ErrorExit as e:
            error(e.message)
            ws = getenv('WORKSPACE')
            if ws is not None:
                s.produce_error_results(ws, e.message)
            pass

        if retval > 0:
            error("")
            error("Due to the above error(s), this script is unable to continue and is terminating.")
            error("")

        cdebug("Leave ProvApp::main")
        return retval

if __name__ == '__main__':
    app_description = '''
    '''

    app_epilog = '''
examples:
    bare-metal
    ----------
        Install the latest kernel that is in -proposed:
          ./provision statler --sut=real --sut-series=quantal --sut-arch=amd64
          ./provision rizzo   --sut=real --sut-series=lucid   --sut-arch=amd64
          ./provision statler --sut=real --sut-series=quantal --sut-arch=amd64

        Install a custom kernel:
          ./provision waldorf --sut=real --sut-series=precise --sut-arch=i386 --sut-debs-url=http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.2.35-precise/

        Install packages from a ppa:
          ./provision waldorf --sut=real --sut-series=precise --sut-arch=i386 --ppa=ppa:canonical-kernel-team/ppa

    virtual client
    --------------
        Install the latest kernel that is in -proposed:
          ./provision statler --sut=virtual --vh-series=precise --vh-arch=amd64 --sut-series=quantal --sut-arch=amd64
          ./provision statler --sut=virtual --vh-series=precise --vh-arch=amd64 --sut-series=quantal --sut-arch=i386

    lts-hwe
    -------
        Install the latest HWE kernel that is in -proposed:
          ./provision rizzo   --sut=real --sut-series=quantal --sut-arch=amd64 --sut-hwe
          ./provision fozzie  --sut=real --sut-series=oneiric --sut-arch=amd64 --sut-hwe
    '''

    parser = ArgumentParser(description=app_description, epilog=app_epilog, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('--dry-run',  action='store_true', default=False, help='Don\'t do anything, just print out what would be done.')
    parser.add_argument('--quiet',  action='store_true', default=False, help='Do not print any progress information.')
    parser.add_argument('--debug', action='store_true', default=False, help='Print out lots of stuff.')

    parser.add_argument('--sut',          required=False,  default='real', choices=['real', 'virtual'], help='Kind of SUT to be created.')
    parser.add_argument('--sut-series',   required=True,  help='The series that is to be installed on the SUT. lts-hwe-<series> denotes that a lts-hwe kernel is to be run on the appropriate lts series.')
    parser.add_argument('--sut-arch',     required=False,  default='amd64', choices=['amd64', 'i386', 'arm64', 'ppc64el'], help='The architecture (amd64 or i386) that is to be installed on the SUT.')
    parser.add_argument('--sut-hwe',      required=False, action='store_true', default=False, help='The series is for a hwe or backport kernel series.')
    parser.add_argument('--sut-debs-url', required=False, default=None, help='A pointer to a set of kernel deb packages that are to be installed.')
    parser.add_argument('--ppa',          required=False, default=None, help='A ppa name to update packages from')

    parser.add_argument('--vh-series',    required=False, help='If the SUT is a virtual client, a virtual host is needed. This is the series of that virtual host.')
    parser.add_argument('--vh-arch',      required=False, help='If the SUT is a virtual client, a virtual host is needed. This is the arch of that virtual host.')
    parser.add_argument('--vh-hwe',       required=False, action='store_true', default=False, help='The series is for a hwe or backport kernel series.')

    parser.add_argument('target', metavar='TARGET', type=str, nargs=1, help='The name of the system to be provisioned.')

    args = parser.parse_args()

    if args.debug:
        level = DEBUG
        Clog.dbg = True
    else:
        level = WARNING
    basicConfig(filename=None, level=level, format="%(levelname)s - %(message)s")

    # If the sut-name was not specified on the command line, use the
    # HW name.
    #
    setattr(args, 'sut_name', args.target[0])
    if args.sut == 'virtual':
        args.sut_name = 'vm-%s' % args.target[0]
        setattr(args, 'vh_name', args.target[0])
    else:
        args.sut_name = args.target[0]

    cdebug('sut : %s' % args.sut)
    cdebug('sut-arch : %s' % args.sut_arch)

    app = ProvApp()
    exit(app.neo(args))

# vi:set ts=4 sw=4 expandtab syntax=python:
