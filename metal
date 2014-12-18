#!/usr/bin/env python
#

from os                                 import getenv, path
from lib.argparse                       import ArgumentParser, RawDescriptionHelpFormatter
from logging                            import error, info, basicConfig, DEBUG, WARNING, INFO

try:
    from lib.configuration                  import Configuration
except ImportError as e:
    print("")
    print("*** Error: Failed to import lib.configuration. Do you need to create the symlink from your")
    print("           local configuration-<mine>.py file to lib/configuration.py?")
    print("")
    exit(-1)

from lib.log                            import cdebug, Clog, cerror
from lib.shell                          import ShellError, ShellTimeoutError, sh, ssh, Shell
from lib.provisioning                   import MetalProvisioner, VirtualProvisioner, Metal, PS
from lib.exceptions                     import ErrorExit
from lib.hwe                            import HWE

from lib.ubuntu                         import Ubuntu

# MetalApp
#
class MetalApp(object):
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

    # validate_args
    #
    # Makes sure the command line options specified will actually work with the targetted system.
    #
    def validate_args(s, args):
        cdebug("    Enter MetalApp::validate_args")

        if args.name not in Configuration['systems']:
            cdebug("        raising ErrorExit exception")
            raise ErrorExit('The name (%s) is not a recognized system. Valid systems are:\n    %s' % (args.name, '\n    '.join(Configuration['systems'].keys())))

        # Some systems we don't want to re-provision by accident.
        #
        if Configuration['systems'][args.name]['locked']:
            raise ErrorExit('The system (%s) is locked and will not be provisioned.' % args.name)

        target = Configuration['systems'][args.name]
        # Does the hw arch match that of what was specified on the command line?
        #
        if args.arch not in target['arch']:
            raise ErrorExit('The arch (%s) is not valid for the system (%s). Valid arches for that system are:\n    %s' % (args.arch, args.name, '\n    '.join(target['arch'])))

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

        #if args.series not in supported:
        #    raise ErrorExit('The series (%s) is not a recognized, supported series. Valid series are:\n    %s' % (args.series, '\n    '.join(supported)))

        if args.hwe:
            if HWE[args.series]['series'] is None:
                raise ErrorExit('The series (%s) does not have a HWE version.' % (args.series))

        cdebug("    Leave MetalApp::validate_args")

    # main
    #
    def main(s, args):
        cdebug("Enter MetalApp::main")
        retval = 1
        try:
            s.validate_args(args)
            metal = Metal(args.name, args.series, args.arch, hwe=args.hwe, xen=args.xen, debs=args.debs_url, ppa=args.ppa, dry_run=args.dry_run)
            if metal.provision():
                retval = 0

        except ErrorExit as e:
            error(e.message)
            ws = getenv('WORKSPACE')
            if ws is not None:
                s.produce_error_results(ws, e.message)
            pass

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

        cdebug("Leave MetalApp::main")
        return retval

if __name__ == '__main__':
    app_description = '''
    '''

    app_epilog = '''
examples:
    bare-metal
    ----------
        Install the latest kernel that is in -proposed:
          metal nuc1 --series=trusty
          metal nuc2 --series=utopic --arch=amd64

        Install a custom kernel:
          metal nuc1 --series=precise --arch=i386 --debs-url=http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.2.35-precise/

        Install packages from a ppa:
          metal nuc1 --sut=real --sut-series=precise --sut-arch=i386 --ppa=ppa:canonical-kernel-team/ppa

    lts-hwe
    -------
        Install the latest HWE kernel that is in -proposed:
          metal nuc1  --series=trusty --arch=amd64 --hwe
    '''

    parser = ArgumentParser(description=app_description, epilog=app_epilog, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('--dry-run',  action='store_true', default=False, help='Don\'t do anything, just print out what would be done.')
    parser.add_argument('--quiet',  action='store_true', default=False, help='Do not print any progress information.')
    parser.add_argument('--debug', action='store_true', default=False, help='Print out lots of stuff.')

    parser.add_argument('--series',   required=True,  help='The series that is to be installed on the SUT. lts-hwe-<series> denotes that a lts-hwe kernel is to be run on the appropriate lts series.')
    parser.add_argument('--arch',     required=False, default='amd64', choices=['amd64', 'i386', 'arm64', 'ppc64el'], help='The architecture (amd64, i386, arm64 or ppc64el) that is to be installed on the SUT. (amd64 is the default)')
    parser.add_argument('--debs-url', required=False, default=None, help='A pointer to a set of kernel deb packages that are to be installed.')
    parser.add_argument('--ppa',      required=False, default=None, help='A ppa name to update packages from')
    parser.add_argument('--hwe',      required=False, action='store_true', default=False, help='The series is for a hwe or backport kernel series.')
    parser.add_argument('--xen',      required=False, action='store_true', default=False, help='The bare-metal should be a Xen host.')

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
    setattr(args, 'name', args.target[0])

    app = MetalApp()
    exit(app.main(args))

# vi:set ts=4 sw=4 expandtab syntax=python:
