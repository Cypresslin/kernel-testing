<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<%
   sys_data = template_data
%>
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="en-US">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	    <title>${report_title}</title>

        <link title="light" rel="stylesheet" href="http://people.canonical.com/~kernel/reports/css/themes/blue/style.css" type="text/css" media="print, projection, screen" />
        <link title="light" rel="stylesheet" href="http://people.canonical.com/~kernel/reports/css/light.css" type="text/css" media="print, projection, screen" />

        <link href='http://fonts.googleapis.com/css?family=Cantarell&subset=latin'              rel='stylesheet' type='text/css'>
        <script type="text/javascript" src="http://people.canonical.com/~kernel/reports/js/jquery-latest.js"></script>
        <script type="text/javascript" src="http://people.canonical.com/~kernel/reports/js/jquery.tablesorter.js"></script>
        <script type="text/javascript" src="http://people.canonical.com/~bradf/media/high/js/highcharts.js"></script>
        <script type="text/javascript">
           $(function() {
                $("#boot-speed-results").tablesorter({
                    headers: { 0: {sorter: false}, 1: {sorter: false}, 2: {sorter: false}, 3: {sorter: false}, 4: {sorter: false}, 5: {sorter: false}, 6: {sorter: false}, 7: {sorter: false}, 8:{sorter: false} },
                    widgets: ['zebra']
                });
            });
        </script>
        <style>
            div.report-title {
                  font-weight: bold;
                    font-size: 20px;
                        color: #1d89c8;
                   text-align: center;
                      padding: 2px 0px 20px 0px;
            }

            div.section-heading {
                  font-weight: bold;
                    font-size: 16px;
                      padding: 20px 0px 2px 0px;
                border-bottom: 2px solid #1d89c8
            }

            div.column-wrapper {
                width: 100%;
                text-align: center;
            }

            div.column-1 {
                float: left;
                width: 50%;
            }

            div.column-2 {
                float: right;
                width: 50%;
            }

            div.boot-table {
                clear: both;
            }
        </style>
    </head>

    <body class="bugbody">
        <div class="outermost">
            <div class="report-title">
		    Ubuntu Boot Speed Tracking
            </div>

            <div id="bootchart" style="width: 1000px; height: 600px;"></div>

            <div>
                <p>&nbsp;</p>
            </div>

            <div class="boot-table">
                <table id="boot-speed-results" class="tablesorter" border="0" cellpadding="0" cellspacing="1" width="100%%">
                    <thead>
                        <tr>
                            <th width="120">Date</th>
                            <th width="100">Series</th>
                            <th width="70">Boot</th>
                            <th width="70">Kernel</th>
                            <th width="70">Plumbing</th>
                            <th width="70">X.org</th>
                            <th width="70">Desktop</th>
                            <th width="70">Kernel Init</th>
                            <th>Files</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for date in sorted(sys_data['dates'], reverse=True):
                        <%
                            boot       = '%0.2f' % sys_data['dates'][date]['timings']['boot']
                            kernel     = '%0.2f' % sys_data['dates'][date]['timings']['kernel']
                            plumbing   = '%0.2f' % sys_data['dates'][date]['timings']['plumbing']
                            xorg       = '%0.2f' % sys_data['dates'][date]['timings']['xorg']
                            desktop    = '%0.2f' % sys_data['dates'][date]['timings']['desktop']
                            kernelinit = '%0.2f' % sys_data['dates'][date]['timings']['kernelinit']

                            if sys_data['dates'][date]['tag'] == '':
                                label = sys_data['dates'][date]['datestamp']
                            else:
                                label = sys_data['dates'][date]['tag']
                        %>
                        <tr>
                            <td>${label}</td>
                            <td>${sys_data['dates'][date]['series']}</td>
                            <td>${boot}</td>
                            <td>${kernel}</td>
                            <td>${plumbing}</td>
                            <td>${xorg}</td>
                            <td>${desktop}</td>
                            <td>${kernelinit}</td>
                            <td>
                                <!--
                                <a href="${date}/bootchart.png">bootchart.png</a>
                                -->
                                <a href="${date}/bootchart.png">bootchart.png</a>
                                <a href="${date}/bootchart.svg">bootchart.svg</a>
                                <a href="${date}/bootchart.tgz">bootchart.tgz</a>
                                <a href="${date}/bootgraph.svg">bootgraph.svg</a>
                                <a href="${date}/lspci">lspci</a>
                                <a href="${date}/dmesg">dmesg</a>
                                <a href="${date}/times">times</a>
                            </td>
                        </tr>
                        % endfor
                    </tbody>
                </table>
            </div>
            <div>
                <br />
                <hr />
                <table width="100%%" cellspacing="0" cellpadding="0">
                    <tr>
                        <td>
                            ${timestamp}
                        </td>
                        <td align="right">
                            &nbsp;
                        </td>
                    </tr>
                </table>
                <br />
            </div>
        </div> <!-- Outermost -->
        <%
            chart_series = '                series: [\n                    {\n'
            x = 0
            for stage in ['desktop', 'xorg', 'plumbing', 'kernel', 'kernelinit']:
                if stage == 'boot': continue
                chart_series += '                        name: \'%s\',\n' % stage.title()

                t = []
                for i in reversed(range(0, len(sys_data['ct3'][stage]))):
                    t.append(sys_data['ct3'][stage][i])

                chart_series += '                        data: [%s]\n' % (', '.join(['%02f' % val[1] for val in t]))
                x += 1
                if x < 5:
                    chart_series += '                    }, {\n'
            chart_series += '                    }\n                ]\n'

            # Need some special handling so I can substitute non-date strings for some labels.
            #
            x1 = []
            for n in sys_data['ct3']['boot']:
                x1.append(n[0])

            x2 = []
            for n in sorted(x1, reverse=True):
                if sys_data['dates'][n]['tag'] == '':
                    x2.append(sys_data['dates'][n]['datestamp'])
                else:
                    x2.append(sys_data['dates'][n]['tag'])

            xaxis_categories = ', '.join(["'%s'" % n for n in x2])
            #xaxis_categories = ', '.join(sorted(["'%s'" % n[0] for n in sys_data['ct3']['boot']], reverse=True))
        %>
        <script type="text/javascript">
        $(function () {
            chart = new Highcharts.Chart({
                chart: {
                    renderTo: 'bootchart',
                    defaultSeriesType: 'bar'
                },
                title: {
                    text: '${report_title}'
                },
                legend: {
                    reversed: true
                },
                xAxis: {
                    categories: [${xaxis_categories}],
                    title: {
                        text: 'Date of Test'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Time (seconds)'
                    },
                    min: 0
                },
                plotOptions: {
                    series: {
                        stacking: 'normal'
                    }
                },
                tooltip: {
                    formatter: function() {
                        return '<b>' + this.series.name + '</b> : ' + this.y + ' seconds';
                    }
                },
${chart_series}
            });
        });
        </script>
    </body>

</html>
<!-- vi:set ts=4 sw=4 expandtab syntax=mako: -->
