#!/usr/bin/env python
#

from lib.log                            import cdebug, center, cleave

from lib.grinder                        import Exit, TestResultsRepository, TestResultsRepositoryError
from lib.utils                          import error, string_to_date

from lib.ubuntu                         import Ubuntu
from lib.debian                         import Debian

# TestResults
#
class TestResults():
    '''
    '''

    # __init__
    #
    def __init__(s):
        '''
        '''
        center(s.__class__.__name__ + '.__init__')
        try:
            s.trr = TestResultsRepository(rc='test-results.rc')
            s.ubuntu = Ubuntu()

        except TestResultsRepositoryError as e:
            error(e.msg)
            cdebug("Leave Digest.initialize")
            cleave(s.__class__.__name__ + '.__init__')
            raise Exit()
        cleave(s.__class__.__name__ + '.__init__')

    # series
    #
    def series(s, results):
        center(s.__class__.__name__ + '.series')

        retval = "unknown"
        try:
            # First see if the series is in the results. This might have been done by hand
            # to add a series where this algorithm doesn't work.
            #
            retval = results['attributes']['series']
        except KeyError:
            kv = ''
            try:
                kv = results['attributes']['kernel']
                m = Debian.version_rc.match(kv)
                if m:
                    for series in Ubuntu.index_by_series_name:
                        if series in kv:
                            cdebug("            is backport kernel", 'blue')
                            # If the series is in the kernel version string, it is most likely
                            # a "backport" kernel and we should use the series in the version
                            #
                            retval = series
                            break

                    if retval == 'unknown':
                        # Starting with Utopic we are adding the series version to the kernel version and not
                        # the series name.
                        #
                        for k in Ubuntu.db:
                            if '~%s' % k in kv:
                                cdebug("            is backport kernel", 'blue')
                                # If the series is in the kernel version string, it is most likely
                                # a "backport" kernel and we should use the series in the version
                                #
                                retval = Ubuntu.db[k]['name']
                                break

                    if retval == 'unknown':
                        # What a hack ...
                        if '2.6' == m.group(1):
                            version = '2.6.32'
                        else:
                            version = '%s.0' % (m.group(1)) # Only want major and minor for determining the series
                        retval = s.ubuntu.lookup(version)['name']
                else:
                    print(" ** WARNING: The kernel version string found in the results data did not match the regex.")
            except KeyError:
                print(" ** WARNING: The kernel version (%s) did not match up with any Ubuntu series." % (results['attributes']['kernel']))

        cleave(s.__class__.__name__ + '.series')
        return retval

    # arch_from_proc
    #
    def arch_from_proc(s, proc):
        if proc == 'x86_64':
            arch = 'amd64'
        elif proc == 'i686':
            arch = 'i386'
        elif proc == 'athlon':
            arch = 'i386'
        elif proc == 'aarch64':
            arch = 'arm64'
        else:
            arch = proc
        return arch

    def per_suite_results(s, data, who='sru'):
        # Take the cumulative results dictionary and build a test-suite focused dictionary from
        # it.
        #
        center(s.__class__.__name__ + '.per_suite_results')
        cdebug('--------------------------------------------------')
        retval = {} # suite results
        cdebug('Building test-suite focused dictionary')
        try:
            for series in data[who]:
                cdebug('    series: %s' % series)
                if series not in retval:
                    retval[series] = {}

                for kver in data[who][series]:
                    cdebug('        kver: %s' % kver)
                    for flavour in data[who][series][kver]:
                        cdebug('            flavour: %s' % flavour)
                        if kver not in retval[series]:
                            retval[series][kver] = {}

                        if flavour not in retval[series][kver]:
                            retval[series][kver][flavour] = {}

                        for test_run in data[who][series][kver][flavour]:
                            attributes = test_run['attributes']

                            # decode the arch
                            #
                            arch = s.arch_from_proc(attributes['platform']['proc'])
                            cdebug('                arch: %s' % arch)

                            if arch not in retval[series][kver][flavour]:
                                retval[series][kver][flavour][arch] = {}

                            results = test_run['results']
                            for k in results['suites']:
                                suite = k['name'].replace('autotest.', '')

                                if who == 'sru':
                                    link = '%s-%s/%s-%s-%s-index.html' % (kver, flavour, suite, kver, arch)
                                else:
                                    link = '%s-%s/%s-%s-%s-%s-index.html' % (kver, flavour, who, suite, kver, arch)

                                if suite not in retval[series][kver][flavour][arch]:
                                    if suite == 'qrt_apparmor':
                                        cdebug("            %s : new (%s); ran: %d; failed: %d" % (suite, arch, k['tests run'], k['tests failed']), 'green')
                                    retval[series][kver][flavour][arch][suite] = {}
                                    retval[series][kver][flavour][arch][suite]['link'] = link
                                    retval[series][kver][flavour][arch][suite]['failed']  = k['tests failed']
                                    retval[series][kver][flavour][arch][suite]['run']     = k['tests run']
                                    retval[series][kver][flavour][arch][suite]['skipped'] = k['tests skipped']
                                else:
                                    if suite == 'qrt_apparmor':
                                        cdebug("            %s : adding (%s); ran: %d; failed: %d" % (suite, arch, k['tests run'], k['tests failed']), 'green')
                                    retval[series][kver][flavour][arch][suite]['failed']  += k['tests failed']
                                    retval[series][kver][flavour][arch][suite]['run']     += k['tests run']
                                    retval[series][kver][flavour][arch][suite]['skipped'] += k['tests skipped']
        except KeyError:
            pass
        cleave(s.__class__.__name__ + '.per_suite_results')
        return retval

    # collect_results
    #
    def collect_results(s):
        '''
        Build a dictionary of all of the test results.

        dict:
            who:
                series:
                    kernel-version:
                        test results
        '''
        center(s.__class__.__name__ + '.collect_results')
        data = {}
        for tr in s.trr.test_runs:
            try:
                cdebug('tr: %s' % tr)
                results = s.trr.results(tr)
            except TestResultsRepositoryError as e:
                error(e.msg)
                continue

            cdebug("Processing: %s" % (tr), 'green')

            kernel_version = results['attributes']['kernel']
            try:
                flavour = results['attributes']['kernel-flavour']
            except KeyError:
                cdebug("no kernel-flavour", 'cyan')
                flavour = 'generic'
            series = s.series(results)

            cdebug("    kernel: %s" % (kernel_version))
            if flavour == 'lowlatency':
                cdebug("   falvour: %s     --------------------------------------------------------------------------------------" % (flavour))
            else:
                cdebug("   falvour: %s" % (flavour))
            cdebug("    series: %s" % (series))

            # If the kernel used was a "custom" kernel, one that someone on the kernel
            # team built themselves or a mainline build kernel, we want that information
            #
            job = results['attributes']['environ']['JOB_NAME']
            who = None
            if '_for_' in job:
                (junk, who) = job.split('_for_')
                cdebug("       who: %s" % (who))
            else:
                who = 'sru' # 'sru' is just a general 'catch all' this lumps everything
                # that wasn't done by someone specifically into a single
                # bucket.

            if who == 'kernel':
                who = 'sru'

            results['attributes']['series'] = series

            # "Fixup" the timestamp to be what we want it to look like on the web page
            #
            ts = string_to_date(results['attributes']['timestamp'])
            results['attributes']['timestamp'] = ts.strftime("%Y-%m-%d %H:%M")

            # The primary key is who.
            #
            if who not in data:
                data[who] = {}
                cdebug('                                                                                       who first seen (%s)' % who, 'white')

            # The second key is the series.
            #
            if series not in data[who]:
                data[who][series] = {}
                cdebug('                                                                                       series first seen (%s)' % series, 'white')

            # The third key for 'data' is the kernel version.
            #
            if kernel_version not in data[who][series]:
                data[who][series][kernel_version] = {}
                cdebug('                                                                                       version (%s) first seen (%s %s)' % (kernel_version, who, series), 'white')

            # The fourth key for 'data' is the flavour
            #
            if flavour not in data[who][series][kernel_version]:
                data[who][series][kernel_version][flavour] = []
                cdebug('                                                                                       flavour first seen (%s)' % flavour, 'white')

            data[who][series][kernel_version][flavour].append(results)

        cleave(s.__class__.__name__ + '.collect_results')
        return data

# vi:set ts=4 sw=4 expandtab:
