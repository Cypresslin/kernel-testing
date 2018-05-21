#!/usr/bin/env python
#

import re
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import yaml


def convert_v2_to_v1(data):
    data_v1 = {}
    for series_key, series in data.items():
        series_v1 = data_v1.setdefault(series_key, {})

        series_v1['series_version'] = series_key
        series_v1['name'] = series['codename']
        for key in ('development', 'supported'):
            series_v1[key] = series.get(key, False)
        for key in ('lts', 'esm'):
            if series.get(key, False):
                series_v1[key] = series[key]

        if 'sources' not in series or not series['sources']:
            continue

        for source_key, source in series['sources'].items():
            if 'versions' in source:
                series_v1['kernels'] = source['versions']
                series_v1['kernel'] = series_v1['kernels'][-1]
                break

        series_v1['derivative-packages'] = {}
        series_v1['packages'] = []
        series_v1['derivative-packages']['linux'] = []
        for source_key, source in series['sources'].items():
            if source.get('supported', False) and not source.get('copy-forward', False):
                if 'derived-from' in source:
                    (derived_series, derived_package) = source['derived-from']
                    if derived_series == series_key:
                        derivative_packages = series_v1['derivative-packages'].setdefault(derived_package, [])
                        derivative_packages.append(source_key)
                    else:
                        backport_packages = series_v1.setdefault('backport-packages', {})
                        backport_packages[source_key] = [ derived_package, derived_series ]

                else:
                    series_v1['derivative-packages'].setdefault(source_key, [])

            for package_key, package in source['packages'].items():
                if source.get('supported', False) and not source.get('copy-forward', False):
                    series_v1['packages'].append(package_key)

                if not package:
                    continue

                dependent_packages = series_v1.setdefault('dependent-packages', {})
                dependent_packages_package = dependent_packages.setdefault(source_key, {})

                if 'type' in package:
                    dependent_packages_package[package['type']] = package_key

            if 'snaps' in source:
                for snap_key, snap in source['snaps'].items():
                    if snap and 'primary' in snap:
                        dependent_snaps = series_v1.setdefault('dependent-snaps', {})
                        dependent_snaps_source = dependent_snaps.setdefault(source_key, snap)
                        dependent_snaps_source['snap'] = snap_key
                        del dependent_snaps_source['primary']
                        del dependent_snaps_source['repo']
                    else:
                        derivative_snaps = series_v1.setdefault('derivative-snaps', {})
                        derivative_snaps.setdefault(source_key, []).append(snap_key)

    return data_v1


#
# Warning - using the following dictionary to get the series name from the kernel version works for the linux package,
# but not for some others (some ARM packages are known to be wrong). This is because the ARM kernels used for some
# series are not the same as the main kernels
#

# UbuntuError
#
class UbuntuError(Exception):
    # __init__
    #
    def __init__(self, error):
        self.msg = error

# Ubuntu
#
class Ubuntu:

    # The series information data is now encoded in a yaml file in this same directory
    # and which is accessed via the URL you see below. If you make changes to the yaml
    # file you need to update the kteam-tools.kernel.ubuntu.com repo in the ~kernel-ppa
    # directory on kernel.ubuntu.com.
    #
    #url = 'https://git.launchpad.net/~canonical-kernel/+git/kteam-tools/plain/ktl/kernel-series-info.yaml'
    url = 'https://git.launchpad.net/~canonical-kernel/+git/kteam-tools/plain/info/kernel-series.yaml'
    # url = 'file:///home/apw/git2/kteam-tools/info/kernel-series.yaml'
    response = urlopen(url)
    content = response.read()
    if type(content) != str:
        content = content.decode('utf-8')
    data = yaml.load(content)

    db = convert_v2_to_v1(data)

    index_by_kernel_version = {}
    for v in db:
        if 'kernels' in db[v]:
            for version in db[v]['kernels']:
                index_by_kernel_version[version] = db[v]
            db[v]['kernel'] = db[v]['kernels'][-1]
        elif 'kernel' in db[v]:
            index_by_kernel_version[db[v]['kernel']] = db[v]

    index_by_series_name = {}
    for v in db:
        index_by_series_name[db[v]['name']] = db[v]

    kernel_source_packages = []
    for v in db:
        if 'packages' in db[v]:
            for p in db[v]['packages']:
                if p not in kernel_source_packages:
                    kernel_source_packages.append(p)

    # lookup
    #
    def lookup(self, key):
        """
        Using the given key, find the matching record in the db and return that record.
        Note, the key argument can be a series-name, series-version or a kernel-version.
        """
        if key in Ubuntu.db:
            record = Ubuntu.db[key]
        elif key in Ubuntu.index_by_kernel_version:
            record = Ubuntu.index_by_kernel_version[key]
        elif key in Ubuntu.index_by_series_name:
            record = Ubuntu.index_by_series_name[key]
        else:
            raise KeyError(key)

        return record

    # is_development_series
    #
    def is_development_series(self, series):
        '''
        Returns True if the series passed in is the current series under development.
        '''
        try:
            retval = self.index_by_series_name[series]['development']
        except KeyError:
            retval = False
        return retval

    # is_supported_series
    #
    def is_supported_series(self, series):
        """
        Lookup the given series and return whether it is still supported or not. Note, since
        this uses the 'lookup' method, the series argument can be a series-name, series-version
        or a kernel-version.
        """
        retval = False

        rec = self.lookup(series)
        retval = rec['supported']

        return retval

    # development_series
    #
    @property
    def development_series(self):
        """
        Assume there is one, and only one, development series.
        """
        retval = None
        for series in self.db:
            try:
                if self.db[series]['development']:
                    retval = self.db[series]['name']
                    break
            except KeyError:
                    pass

        return retval

    # development_series_version
    #
    @property
    def development_series_version(self):
        """
        Assume there is one, and only one, development series.
        """
        retval = None
        for series in self.db:
            try:
                if self.db[series]['development']:
                    retval = series
                    break
            except KeyError:
                    pass

        return retval

    # last_release
    #
    @property
    def last_release(self):
        """
        Return the series name for the last release, i.e. development_series - 1
        """
        devel_series = self.development_series
        devel_version = self.lookup(devel_series)['series_version']
        (y, m) = devel_version.split('.')
        if m == '10':
            m = '04'
        else:
            y = str(int(y) - 1)
            m = '10'
        release_version = "%s.%s" % (y, m)
        release_series = self.lookup(release_version)['name']

        return release_series

    # supported_series
    #
    @property
    def supported_series(self):
        """
        A list of all the currently supported series names.
        """
        retval = []
        for series in self.db:
            if self.db[series]['supported']:
                retval.append(self.db[series]['name'])

        return retval

    # supported_series_version
    #
    @property
    def supported_series_version(self):
        """
        A list of all the currently supported series names.
        """
        retval = []
        for series in self.db:
            if self.db[series]['supported']:
                retval.append(series)

        return retval

    # active_packages
    #
    @property
    def active_packages(self):
        """
        A list of all the packages for all the supported series.
        """
        retval = []
        for series in self.db:
            if self.db[series]['supported']:
                for pkg in self.db[series]['packages']:
                    if pkg not in retval:
                        retval.append(pkg)

        return retval

    # series where that package-version is found
    #
    def series_name(self, package, version):
        """
        Return the series name where that package-version is found
        """
        retval = None

        if package.startswith('linux-lts-') or package.startswith('linux-hwe'):
            for entry in self.db.values():
                # starting with trusty, the lts packages now include the series
                # version instead of the series name, e.g: 3.16.0-23.31~14.04.2
                # instead of 3.16.0-23.31~trusty1
                expected = '.*~(%s\.\d+|%s\d+)' % (entry['series_version'], entry['name'])
                if re.match(expected, version):
                    retval = entry['name']
        else:
            for entry in self.db.values():
                if 'kernels' in entry:
                    for kversion in entry['kernels']:
                        if version.startswith(kversion):
                            retval = entry['name']
                            series_version = entry['series_version']
                            break
                elif 'kernel' in entry:
                    if version.startswith(entry['kernel']):
                        retval = entry['name']
                        series_version = entry['series_version']

            # linux-azure is a backport that doesn't contain the 'upstream'
            # series number on the package name, so we need to look for it
            # first and then look for the target series.
            if package.startswith('linux-azure'):
                for entry in self.db.values():
                    try:
                        if len(set(['linux', series_version]) & set(entry['backport-packages'][package])) == 2:
                            retval = entry['name']
                    except KeyError:
                        pass

        return retval

if __name__ == '__main__':
    ubuntu = Ubuntu()
    db = ubuntu.db

    if db['16.04']['name'] != 'xenial':
        print('DB Name doesn\'t match xenial.')

    if ubuntu.index_by_kernel_version['4.4.0']['name'] != 'xenial':
        print('Looking up by kernel version failed')

    if ubuntu.index_by_series_name['xenial']['name'] != 'xenial':
        print('Looking up by series name failed')

    for p in ubuntu.ksp:
        if p not in ubuntu.kernel_source_packages:
            print('%s is not in ubuntu.kernel_source_packages' % p)
# vi:set ts=4 sw=4 expandtab:
