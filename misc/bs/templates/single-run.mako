<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="en-US">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <!-- <meta http-equiv="refresh" content="60" /> -->
        <title>Ubuntu - Kernel Team Server</title>
        <link rel="stylesheet" href="http://kernel.ubuntu.com/media/kernel-style.css" type="text/css" media="screen" />
        <script type="text/javascript" src="http://people.canonical.com/~kernel/reports/js/jquery-latest.js"></script>
        <script type="text/javascript" src="http://people.canonical.com/~bradf/media/high/js/highcharts.js"></script>
        <style>
            div.index-bottom-section {
                 border-radius: 0px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.3);
                    background: #f7f5f6;
                       padding: 20px;
                 margin-top: -16px;
                       /*
                 margin-bottom: 20px;
                 */

                     font-size: 11px;
                   line-height: 16px;
                         color: #333;
            }

            a {
                         color: #0000cc;
            }

            a:hover {
               text-decoration: underline;
            }

            a:active a:link, a:visited {
               text-decoration: none;
            }

        </style>
    </head>


    <body class="dash-body">
        <div class="dash-center-wrap">
            <div class="dash-center">
                <div class="dash-center-content">

                    <div id="dash-header">
                        <div id="dash-timestamp">
                            <a href="http://ubuntu.com" title="Home" rel="home"><img src="http://kernel.ubuntu.com/media/ubuntu-logo.png" alt="Home" /></a>
                        </div>
                        <h1>Boot Speed Testing</h1>
                    </div> <!-- header -->

                    <br />

                    <!-- System Information
                    -->
                    <div class="dash-section" align="center">
                        <table width="100%" border="0" style="font-size: 1.0em">
                            <tr>
                                <td width="100" align="right">platform:</td>    <td width="2">&nbsp;</td> <td width="350" align="left">${systems[template_data['properties']['mac_address']]}</td>
                                <td width="100" align="right">mac address:</td> <td width="2">&nbsp;</td> <td width="350" align="left">${template_data['properties']['mac_address']}</td>
                                <td>&nbsp;</td>
                            </tr>
                            <tr>
                                <td width="100" align="right">kernel:</td>      <td width="2">&nbsp;</td> <td width="350" align="left">${template_data['properties']['kernel_version']}</td>
                                <td width="100" align="right">series:</td>      <td width="2">&nbsp;</td> <td width="350" align="left">${template_data['properties']['series_name']}</td>
                                <td>&nbsp;</td>
                            </tr>
                        </table>
                    </div>

                    <!-- Boot chart section
                    -->
                    <div class="dash-section" align="center">
                        <table width="100%"> <!-- The section is one big table -->
                            <tr>
                                <td><div id="kernelinit" style="width: 300px; height: 300px;"></div></td>
                                <td><div id="kernel" style="width: 300px; height: 300px;"></div></td>
                                <td><div id="xorg" style="width: 300px; height: 300px;"></div></td>
                            </tr>
                            <tr>
                                <td><div id="desktop" style="width: 300px; height: 300px;"></div></td>
                                <td><div id="plumbing" style="width: 300px; height: 300px;"></div></td>
                            </tr>
                        </table>
                    </div> <!-- dash-section -->

                    <!-- Results table section
                    -->
                    <div class="dash-section">
                        <table width="100%"> <!-- The section is one big table -->
                            <tr>
                                <td width="100%" valign="top">
                                    <table width="100%" style="font-size: 0.9em" border="0">
                                        <thead>
                                                <tr>
                                                    <th align="center" colspan="6">Times (sec.)</th>
                                                    <th>&nbsp;</th>
                                                </tr>
                                            <tr>
                                                <th align="center" width="80">Run</th>
                                                <th align="center" width="80">Desktop</th>
                                                <th align="center" width="80">Kernel</th>
                                                <th align="center" width="80">Kernel Init</th>
                                                <th align="center" width="80">Plumbing</th>
                                                <th align="center" width="80">Xorg</th>
                                                <th align="center" colspan="8">Files</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            % for run in range(0, len(template_data['data']['boot']['raw'])):
                                                <tr>
                                                    <td align="center"><%r = run + 1%>${r}</td>
                                                    <td align="center"><% t = '%02.2f' % template_data['data']['desktop']['raw'][run] %>${t}</td>
                                                    <td align="center"><% t = '%02.2f' % template_data['data']['kernel']['raw'][run] %>${t}</td>
                                                    <td align="center"><% t = '%02.2f' % template_data['data']['kernelinit']['raw'][run] %>${t}</td>
                                                    <td align="center"><% t = '%02.2f' % template_data['data']['plumbing']['raw'][run] %>${t}</td>
                                                    <td align="center"><% t = '%02.2f' % template_data['data']['xorg']['raw'][run] %>${t}</td>

                                                    <td><a href="${r}/bootchart.png">bootchart.png</a></td>
                                                    <td><a href="${r}/bootchart.svg">bootchart.svg</a></td>
                                                    <td><a href="${r}/bootchart.tgz">bootchart.tgz</a></td>
                                                    <td><a href="${r}/installer.tgz">installer.tgz</a></td>
                                                    <td><a href="${r}/lspci">lspci</a></td>
                                                    <td><a href="${r}/dmesg">dmesg</a></td>
                                                    <td><a href="${r}/dmesg">syslog</a></td>
                                                    <td><a href="${r}/times">times</a></td>

                                                </tr>

                                            % endfor
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </div> <!-- dash-section -->

                    <div class="index-bottom-section">
                        <table width="100%"> <!-- The section is one big table -->
                            <tr>
                                <td align="left" valign="bottom" colspan="5">
                                  <span style="font-size: 10px; color: #aea79f !important">(c) 2012 Canonical Ltd. Ubuntu and Canonical are registered trademarks of Canonical Ltd.</span>
                                </td>
                                <td align="right" valign="top">
                                    <a href="http://ubuntu.com"><img src="http://kernel.ubuntu.com/media/ubuntu-footer-logo.png"></a>
                                </td>
                            </tr>
                        </table>
                    </div> <!-- dash-section -->

                </div>
            </div>
        </div>
        <%
            chart = {}

            for stage in ['desktop', 'xorg', 'plumbing', 'kernel', 'kernelinit']:
                chart[stage] = {}
                runs = []
                for run in range(0, len(template_data['data']['boot']['raw'])):
                    runs.append('%d' % (run + 1))
                chart[stage]['xaxis'] = ', '.join(["'%s'" % n for n in runs])

                chart[stage]['series'] = '                series: [\n                    {\n'
                chart[stage]['series'] += '                        color: colors[5],\n'
                chart[stage]['series'] += '                        name: \'run\',\n'
                chart[stage]['series'] += '                        data: [%s]\n' % (', '.join(['%02.02f' % val for val in template_data['data'][stage]['raw']]))
                chart[stage]['series'] += '                    }\n                ]\n'

            charts = "            var colors = Highcharts.getOptions().colors;"
            for stage in ['desktop', 'xorg', 'plumbing', 'kernel', 'kernelinit']:
                charts += "            kernelinit = new Highcharts.Chart({\n"
                charts += "                chart: {\n"
                charts += "                    renderTo: '%s',\n" % stage
                charts += "                    defaultSeriesType: 'column'\n"
                charts += "                },\n"
                charts += "                title: {\n"
                charts += "                    text: '%s'\n" % stage
                charts += "                },\n"
                charts += "                legend: {\n"
                charts += "                    enabled: false,\n"
                charts += "                    reversed: true\n"
                charts += "                },\n"
                charts += "                xAxis: {\n"
                charts += "                    categories: [%s],\n" % chart[stage]['xaxis']
                charts += "                    title: {\n"
                charts += "                        text: null\n"
                charts += "                    }\n"
                charts += "                },\n"
                charts += "                yAxis: {\n"
                charts += "                    title: {\n"
                charts += "                        text: 'Time (seconds)'\n"
                charts += "                    },\n"
                charts += "                    min: 0\n"
                charts += "                },\n"
                charts += "                tooltip: {\n"
                charts += "                    formatter: function() {\n"
                charts += "                        return '<b> pass #' + this.x + '</b> : ' + this.y + '(s)';\n"
                charts += "                    }\n"
                charts += "                },\n"
                charts += "%s\n" % chart[stage]['series']
                charts += "            });\n"
        %>
        <script type="text/javascript">
        $(function () {
${charts}
        });
        </script>
    </body>

</html>
<!-- vi:set ts=4 sw=4 expandtab syntax=mako: -->

