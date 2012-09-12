#!/usr/bin/env python
#
#
# This defines filter sets which are applied to the metadata in benchmark results in order to filter them for charting.
#

from json                               import dumps
from os                                 import path, listdir

from lib.utils                          import stdo, error, json_load
from lib.dbg                            import Dbg

# BenchCharts
#
class BenchCharts:

# Filter NOTES and TODO
#
# TODO: muted_metrics is not used and is ignored, needs implementation
# TODO: sort_by is not used and is ignored, data are sorted by test date and time

    filters = {
        'precise_statler_dbench' :
            {
            'environ.NODE_NAME' : 'statler',
            'metrics_testname' : 'dbench',
            'distro-release-name' : 'precise',
            },
        'quantal_statler_dbench' :
            {
            'environ.NODE_NAME' : 'statler',
            'metrics_testname' : 'dbench',
            'distro-release-name' : 'quantal',
            },
        'quantal_statler_bonnie' :
            {
            'environ.NODE_NAME' : 'statler',
            'metrics_testname' : 'bonnie',
            'distro-release-name' : 'quantal',
            },
        'power_filter' :
            {
            'environ.NODE_NAME' : 'master',
            # This is a hack because the test data files were generated using an older version of the tools.
            'environ.KERNEL_TEST_LIST' : 'power_consumption',
            #'metrics_testname' : 'bonnie',
            #'distro-release-name' : 'quantal',
            },
        }
    
    charts = {
        'dbench_precise_statler_chart' : {
            'filter' : 'precise_statler_dbench',
            'baseline_file' : 'statler-dbench-baseline.json',
            'chart_title' : 'Precise dbench Results',
            'y_label' : 'MB/S',
            'included_metrics' : 'all',
            'sort_by' : 'KERNEL_VERSION',
            },
        'dbench_quantal_statler_chart' : {
            'filter' : 'quantal_statler_dbench',
            'baseline_file' : 'quantal-dbench-baseline.json',
            'chart_title' : 'Quantal dbench Results',
            'y_label' : 'MB/S',
            'included_metrics' : 'all',
            'sort_by' : 'KERNEL_VERSION',
            },
        'bonnie_quantal_statler_block' : {
            'filter' : 'quantal_statler_bonnie',
            'baseline_file' : 'statler-bonnie-baseline.json',
            'chart_title' : 'Quantal Bonnie Block I/O Results',
            'y_label' : 'Operations per Second',
            'included_metrics' : 'seqin_perblk_ksec{perf},seqout_perblk_ksec{perf}',
            'sort_by' : 'KERNEL_VERSION',
            },
        'bonnie_quantal_statler_char' : {
            'filter' : 'quantal_statler_bonnie',
            'baseline_file' : 'statler-bonnie-baseline.json',
            'chart_title' : 'Quantal Bonnie Char I/O Results',
            'y_label' : 'Operations per Second',
            'included_metrics' : 'seqin_perchr_ksec{perf},seqout_perchr_ksec{perf}',
            'sort_by' : 'KERNEL_VERSION',
            },
        'bonnie_quantal_statler_all' : {
            'filter' : 'quantal_statler_bonnie',
            'baseline_file' : 'statler-bonnie-baseline.json',
            'chart_title' : 'Quantal Bonnie I/O Results (All)',
            'y_label' : 'Operations per Second',
            'included_metrics' : 'all',
            'muted_metrics' : 'size{perf}',
            'sort_by' : 'KERNEL_VERSION',
            },
        # Sample/test charts for power consumption using Colin's test data
        'power_dd' : {
            'filter' : 'power_filter',
            'baseline_file' : 'power-baseline.json',
            'chart_title' : 'Power Results: dd',
            'y_label' : 'milliAmps',
            'included_metrics' : 'dd_copy_current_drawn_mA_average{perf},dd_copy_current_drawn_mA_maximum{perf},dd_copy_current_drawn_mA_minimum{perf},dd_copy_current_drawn_mA_stddev{perf}',
            'muted_metrics' : '',
            'sort_by' : 'KERNEL_VERSION',
            },
        'power_idle' : {
            'filter' : 'power_filter',
            'baseline_file' : 'power-baseline.json',
            'chart_title' : 'Power Results: idle',
            'y_label' : 'milliAmps',
            'included_metrics' : 'idle_system_current_drawn_mA_average{perf},idle_system_current_drawn_mA_maximum{perf},idle_system_current_drawn_mA_minimum{perf},idle_system_current_drawn_mA_stddev{perf}',
            'muted_metrics' : '',
            'sort_by' : 'KERNEL_VERSION',
            },
        'power_stress_cpu' : {
            'filter' : 'power_filter',
            'baseline_file' : 'power-baseline.json',
            'chart_title' : 'Power Results: stress CPU',
            'y_label' : 'milliAmps',
            'included_metrics' : 'stress_CPU_current_drawn_mA_average{perf},stress_CPU_current_drawn_mA_maximum{perf},stress_CPU_current_drawn_mA_minimum{perf},stress_CPU_current_drawn_mA_stddev{perf}',
            'muted_metrics' : '',
            'sort_by' : 'KERNEL_VERSION',
            },
        'power_stress_io' : {
            'filter' : 'power_filter',
            'baseline_file' : 'power-baseline.json',
            'chart_title' : 'Power Results: stress I/O sync',
            'y_label' : 'milliAmps',
            'included_metrics' : 'stress_IO_Sync_current_drawn_mA_average{perf},stress_IO_Sync_current_drawn_mA_maximum{perf},stress_IO_Sync_current_drawn_mA_minimum{perf},stress_IO_Sync_current_drawn_mA_stddev{perf}',
            'muted_metrics' : '',
            'sort_by' : 'KERNEL_VERSION',
            },
        'power_stress_vm' : {
            'filter' : 'power_filter',
            'baseline_file' : 'power-baseline.json',
            'chart_title' : 'Power Results: stress VM',
            'y_label' : 'milliAmps',
            'included_metrics' : 'stress_VM_current_drawn_mA_average{perf},stress_VM_current_drawn_mA_maximum{perf},stress_VM_current_drawn_mA_minimum{perf},stress_VM_current_drawn_mA_stddev{perf}',
            'muted_metrics' : '',
            'sort_by' : 'KERNEL_VERSION',
            },
        'power_stress_all' : {
            'filter' : 'power_filter',
            'baseline_file' : 'power-baseline.json',
            'chart_title' : 'Power Results: stress all',
            'y_label' : 'milliAmps',
            'included_metrics' : 'stress_all_current_drawn_mA_average{perf},stress_all_current_drawn_mA_maximum{perf},stress_all_current_drawn_mA_minimum{perf},stress_all_current_drawn_mA_stddev{perf}',
            'muted_metrics' : '',
            'sort_by' : 'KERNEL_VERSION',
            },
        }

    result_sets = {
        'dbench-quantal' :
            {
            'name' : 'Dbench Results',
            'charts' : ['dbench_quantal_statler_chart'],
            },
        'dbench-precise' :
            {
            'name' : 'Dbench Results',
            'charts' : ['dbench_precise_statler_chart', 'dbench_quantal_statler_chart'],
            },
        'bonnie' :
            {
            'name' : 'Bonnie Results',
            'charts' : ['bonnie_quantal_statler_block', 'bonnie_quantal_statler_char', 'bonnie_quantal_statler_all'],
            },
        'power' :
            {
            'name' : 'Power Consumption Results',
            'charts' : ['power_dd', 'power_idle', 'power_stress_cpu', 'power_stress_io', 'power_stress_vm', 'power_stress_all'],
            },
        }

    # lookup
    #
    def ismatch(self, chartname, metadata):
        """
        Using the given chart name, see whether the json data loaded
        from a file meets the criteria to match the definition in the db
        """
        try:
            cd = self.charts[chartname]
        except:
            raise KeyError("Can't find a chart definition named: %s" % chartname)

        filtername = cd['filter']

        try:
            fd = self.filters[filtername]
        except:
            raise KeyError("Can't find a benchmark filter named: %s" % filtername)

        # All filter items must pass
        for key, filterVal in fd.items():
            fparts = key.split(".")
            mptr = metadata
            # Walk into the metadata dictionary using the dot-delimited string in the filter
            #print "    Filtername: %s, filterval: %s " % (key, filterVal)
            try:
                for part in fparts[:-1]:
                    mptr = mptr[part]
                mdValue = mptr[fparts[-1]]
            except KeyError:
                #print "Couldn't find a match in the test metadata for filter variable <%s>, failing match" % key
                return False
            if mdValue != filterVal:
                return False

        return True

    def getsetinfo(self, resultsetname):
        """
        Using the given result set name, find the matching record in the db. return the title
        and names of the charts in that result set.
        """
        try:
            sd = result_sets[resultsetname]
        except:
            raise KeyError("Can't find a results set named: %s" % resultsetname)

        return (result_sets[resultsetname]['name'], result_sets[resultsetname]['charts'])

    def dumpsets(self):
        """
        Dump all set information
        """
        for setname, setinfo in self.result_sets.items():
            print 'Set Name: [%s]' % setname
            for chartname in setinfo['charts']:
                print '    Chart Name: [%s]' % chartname
                chinfo = self.charts[chartname]
                print '        Filter Name: [%s]' % chinfo['filter']
                print '        Filter Definition:'
                for key, val in self.filters[chinfo['filter']].items():
                    print '            [%s] == [%s]' % (key, val)
                print '        Baseline File: [%s]' % chinfo['baseline_file']
                print '        Chart Title: [%s]' % chinfo['chart_title']
                print '        Included Metrics: [%s]' % chinfo['included_metrics']
                print '        Sort By: [%s]' % chinfo['sort_by']
        return

    #
    # filtered_data
    def filtered_data(self, chartname, path_to_data, normalize):
        """
        read all data files in the path location and return a dictionary containing data that meets the filter.
        Only include metrics in the chart definition
        If data is to be normalized, do that using the baseline file in the chart definition
        """
        chartdef = self.charts[chartname]
        filterdata = self.filters[chartdef['filter']]
        included_metrics = chartdef['included_metrics'].split(',')

        if normalize:
            # If we're normalizing the data we take all the included metrics from the
            # baseline file, then find the highest value one, and scale everything to that.
            # This is done to obscure real values in public reports
            baseline_fn = path.join(path_to_data, 'baselines', chartdef['baseline_file'])
            if not path.isfile(baseline_fn):
                raise ValueError("Baseline File <%s> does not exist" % baseline_fn)
            baseline = json_load(baseline_fn)
            basekeys = baseline['metrics'].keys()
            if chartdef['included_metrics'] != 'all':
                # remove any metrics that we don't use
                for metric in basekeys:
                    if 'all' not in included_metrics:
                        if metric not in included_metrics:
                            del baseline['metrics'][metric]

            # Now, find the highest value among all the request metrics so we can scale to that
            norm_val = None
            # get these again, we may have deleted some
            basekeys = baseline['metrics'].keys()
            for metric in basekeys:
                #print('%s : %s' % (metric, baseline['metrics'][metric]))
                if norm_val is None:
                    norm_val =  float(baseline['metrics'][metric])
                elif  (float(baseline['metrics'][metric]) > norm_val):
                    norm_val =  float(baseline['metrics'][metric])

        # Now we open each file, check filters, and process it
        dfl = listdir(path_to_data)
        tests = {}
        for fname in dfl:
            if not fname.endswith('.json'):
                continue

            data = json_load(path.join(path_to_data, fname))
            #print 'testing filters for <%s>' % fname
            if not self.ismatch(chartname, data['meta']):
                #print 'file <%s> did not match filters' % fname
                continue

            print 'file <%s> passes filters, processing' % fname
            if len(data['metrics']) == 0:
                # this can apparently happen when tests are aborted
                print 'Data file contains no metrics, skipping'
                continue

            # filter metrics as requested
            mkeys = data['metrics'].keys()
            for metric in mkeys:
                if 'all' not in included_metrics:
                    if metric not in included_metrics:
                        del data['metrics'][metric]

            if len(data['metrics']) == 0:
                raise ValueError('No metrics left in data file after filtering')

            # if we're scaling to a baseline, do it
            if normalize:
                # get these agin, we may have deleted some
                mkeys = data['metrics'].keys()
                for metric in mkeys:
                    mval = float(data['metrics'][metric])/norm_val
                    data['metrics'][metric] = '%s' % mval

            data['meta']['chart-title'] = chartdef['chart_title']
            if normalize:
                data['meta']['y-label'] = chartdef['y_label'] + ' (normalized)'
            else:
                data['meta']['y-label'] = chartdef['y_label']

            # Save this test, as the BUILD_ID string, which can be sorted chronologically
            #print data['meta']
            buildid = data['meta']['environ']['BUILD_ID']
            tests[buildid] = data

        if len(tests) == 0:
            raise ValueError("There are no data records to write to the output file, perhaps none passed the filters")

        return tests

if __name__ == '__main__':
    benchcharts = BenchCharts()
    db = benchcharts.db

    #for record in db:
    #    print db[record]

    print(ubuntu.lookup('dbench_statler'))

# vi:set ts=4 sw=4 expandtab:
