# Copyright (C) 2015, 2016 Chris J Arges <chris.j.arges@canonical.com>
#

import sys
import urllib
from launchpadlib.launchpad             import Launchpad
from lib.log                            import cdebug, center, cleave, cinfo


# GetPublishedSourcesError
#
class GetPublishedSourcesError(Exception):
    """
    """
    def __init__(self, msg):
        self.message = msg


class KernelDebs:
    build = None

    def __init__(self, version, series, arch):
        center('KernelDebs.__init__')
        launchpad = Launchpad.login_anonymously('canonical-livepatch', 'production')
        ubuntu = launchpad.distributions["ubuntu"]

        self.main_archive = ubuntu.main_archive
        self.arch = arch
        self.version = version
        self.abi = version.split('-')[1].split('.')[0]
        cinfo('       arch: %s' % arch)
        cinfo('    version: %s' % version)
        cinfo('        abi: %s' % self.abi)
        cleave('KernelDebs.__init__')

    def get_binaries(self, source_version, filename_filter):
        center('KernelDebs.get_binaries')
        cinfo('     source_version: %s' % source_version)
        cinfo('    filename_filter: %s' % filename_filter)
        pub_sources = self.main_archive.getPublishedSources(source_name='linux', version=source_version, exact_match=True)
        if not pub_sources:
            raise GetPublishedSourcesError("PublishedSources: %s %s not found." % (source_version, self.arch))

        # Filter through URLs and create a flat list.
        ret = []
        for pub_source in pub_sources:
            urls = pub_source.binaryFileUrls()
            for x in urls:
                if filename_filter in x:
                    ret.append(x)

        # Just return the first element.
        cleave('KernelDebs.get_binaries')
        return ret

    def get_urls(self):
        center('KernelDebs.get_urls')
        appendage = '%s-%s-generic_%s_%s.deb' % (self.version.split('-')[0], self.abi, self.version, self.arch)
        filenames = [
            'linux-image-'       + appendage,
            'linux-image-extra-' + appendage
        ]

        urls = []
        url = ''
        try:
            for fid in filenames:
                url = self.get_binaries(self.version, fid)[0]

                # Verify that we can fetch the url
                #
                # urllib.request.urlopen(url).headers.getheader('Content-Length')

                cdebug('appending: "%s"' % url)
                urls.append(url)

        except GetPublishedSourcesError as e:
            cdebug(e.message)
            urls = None

        except urllib.error.HTTPError:
            cdebug('Failed to get the http headers for %s' % url)
            urls = None

        cleave('KernelDebs.get_urls')
        return urls

if __name__ == "__main__":
    VERSION = sys.argv[1]
    SERIES = sys.argv[2]
    ARCH = sys.argv[3]

    q = KernelDebs(VERSION, SERIES, ARCH)
    print(q.get_urls())

    exit(0)
