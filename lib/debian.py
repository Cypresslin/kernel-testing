#!/usr/bin/env python
#

# Note: It would be nice to not tie the debian class to the git class but
#       be able to handle projects that are under bzr as well. But for
#       now, we need to be practical for now.

from ktl.git                            import Git, GitError
from ktl.utils                          import debug, dump
from ktl.kernel                         import Kernel
from re                                 import compile
from os                                 import path, listdir

# DebianError
#
class DebianError(Exception):
    # __init__
    #
    def __init__(self, error):
        self.msg = error

# Note: Think about cacheing the decoded, changelog dictionary.
#

class Debian:
    verbose = False
    debug = False
    version_line_rc = compile("^(linux[-\S]*) \(([0-9]+\.[0-9]+\.[0-9]+[-\.][0-9]+\.[0-9]+[~\S]*)\) (\S+); urgency=\S+$")
    version_rc      = compile("^([0-9]+\.[0-9]+\.[0-9]+)[-\.]([0-9]+)\.([0-9]+)([~\S]*)$")

    package_rc = compile("^(linux[-\S])*.*$")
    ver_rc     = compile("^linux[-\S]* \(([0-9]+\.[0-9]+\.[0-9]+[-\.][0-9]+\.[0-9]+[~a-z0-9]*)\).*$")

    # debian_directories
    #
    @classmethod
    def debian_directories(cls):
        retval = []

        # Find the correct debian directory for this branch of this repository.
        #
        current_branch = Git.current_branch()

        # If we have a debian/debian.env then open and extract the DEBIAN=...
        # location.
        debug("Checking debian/debian.env", cls.debug)
        debdirs = []
        try:
            debian_env = Git.show("debian/debian.env", branch=current_branch)
            for line in debian_env:
                (var, val) = line.split('=', 1)
                val = val.rstrip()

                if var == 'DEBIAN':
                    debdirs.append(val)
            debug("SUCCEEDED\n", cls.debug, False)
        except GitError:
            debug("FAILED\n", cls.debug, False)
            debdirs += [ 'debian', 'meta-source/debian' ]

        return debdirs

    # master_changelog
    #
    @classmethod
    def master_changelog(cls):
        '''
        The 'changelog' method returns the changelog related to the current branch. This
        method always returns the changelog from the debian.master directory.
        '''
        fid = 'debian.master/changelog'
        if path.exists(fid):
            with open(fid, 'r') as f:
                changelog_contents = f.read()

            retval = cls.changelog_as_list(changelog_contents.split('\n'))
        else:
            raise DebianError('Failed to find the master changelog.')
        return retval

    # raw_changelog
    #
    @classmethod
    def raw_changelog(cls):
        retval = []

        # Find the correct changelog for this branch of this repository.
        #
        current_branch = Git.current_branch()

        # Check each possible directory for a changelog
        debian_dirs = cls.debian_directories()
        for debdir in debian_dirs:
            chglog = debdir + '/changelog'
            debug("Trying '%s': " % chglog, cls.debug)
            try:
                retval = Git.show(chglog, branch=current_branch)
                return retval, chglog
            except GitError:
                debug("FAILED\n", cls.debug, False)

        # Not there anywhere, barf
        raise DebianError('Failed to find the changelog.')

    # changelog
    #
    @classmethod
    def changelog(cls):
        changelog_contents, changelog_path = cls.raw_changelog()
        return cls.changelog_as_list(changelog_contents)

    # changelog_as_list
    #
    @classmethod
    def changelog_as_list(cls, changelog_contents):
        retval = []

        # The first line of the changelog should always be a version line.
        #
        m = cls.version_line_rc.match(changelog_contents[0])
        if m == None:
            if cls.debug:
                m = cls.package_rc.match(changelog_contents[0])
                if m == None:
                    debug('The package does not appear to be in a recognized format.\n', cls.debug)

                m = cls.ver_rc.match(changelog_contents[0])
                if m == None:
                    debug('The version does not appear to be in a recognized format.\n', cls.debug)

            raise DebianError("The first line in the changelog is not a version line.")

        content = []
        for line in changelog_contents:
            m = cls.version_line_rc.match(line)
            if m != None:
                version = ""
                release = ""
                pocket  = ""
                package = m.group(1)
                version = m.group(2)
                rp = m.group(3)
                if '-' in rp:
                    release, pocket = rp.split('-')
                else:
                    release = rp

                section = {}
                section['version'] = version
                section['release'] = release
                section['series']  = release
                section['pocket']  = pocket
                section['content'] = content
                section['package'] = package

                m = cls.version_rc.match(version)
                if m != None:
                    section['linux-version'] = m.group(1)
                    section['ABI']           = m.group(2)
                    section['upload-number'] = m.group(3)
                else:
                    debug('The version (%s) failed to match the regular expression.\n' % version, cls.debug)

                retval.append(section)
                content = []
            else:
                content.append(line)

        return retval

    # abi
    #
    @classmethod
    def abi(cls):

        # Check each possible directory for an abi file
        debian_dirs = cls.debian_directories()
        retvals = []
        for debdir in debian_dirs:
            abidir = debdir + '/abi'
            debug("Trying '%s': \n" % abidir, cls.debug)
            if path.isdir(abidir):
                debug("  '%s' is a directory\n" % abidir, cls.debug)
                contents = listdir(abidir)
                for item in contents:
                    debug("  Contains: '%s'\n" % item, cls.debug)
                    if path.isdir(abidir + '/' + item):
                        retvals.append(item)
                return retvals

        # Not there anywhere, barf
        raise DebianError('Failed to find the abi files.')

# vi:set ts=4 sw=4 expandtab:
