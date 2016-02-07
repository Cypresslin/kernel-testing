#!/usr/bin/env python
#
# Copyright (C) 2015, 2016 Chris J Arges <chris.j.arges@canonical.com>
#

import sys
import urllib2
from launchpadlib.launchpad             import Launchpad
from lib.log                            import cdebug


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
        launchpad = Launchpad.login_anonymously('canonical-livepatch', 'production')
        ubuntu = launchpad.distributions["ubuntu"]

        self.main_archive = ubuntu.main_archive
        self.arch = arch
        self.version = version
        self.abi = '.'.join(version.split('.')[0:3])

    def get_binaries(self, source_version, filename_filter):
        pub_sources = self.main_archive.getPublishedSources(source_name='linux', version=source_version, exact_match=True)
        if not pub_sources:
            raise GetPublishedSourcesError("PublishedSources: %s %s not found." % (source_version, self.arch))

        # Filter through URLs and create a flat list.
        ret = []
        for pub_source in pub_sources:
            urls = pub_source.binaryFileUrls()
            ret = ret + filter(lambda k: filename_filter in k, urls)

        # Just return the first element.
        return ret

    def get_urls(self):
        appendage = '%s-generic_%s_%s.deb' % (self.abi, self.version, self.arch)
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
                urllib2.urlopen(url).headers.getheader('Content-Length')

                cdebug('appending: "%s"' % url)
                urls.append(url)

        except GetPublishedSourcesError as e:
            cdebug(e.message)
            urls = None

        except urllib2.HTTPError:
            cdebug('Failed to get the http headers for %s' % url)
            urls = None

        return urls

if __name__ == "__main__":
    VERSION = sys.argv[1]
    SERIES = sys.argv[2]
    ARCH = sys.argv[3]

    q = KernelDebs(VERSION, SERIES, ARCH)
    print(q.get_urls())

    exit(0)
