<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<%
from datetime     import timedelta

test_results = data['results']
test_attributes = data['attributes']

title = "%s - %s - %s" % (test_attributes['environ']['JOB_NAME'], test_attributes['kernel'], test_attributes['timestamp'])
test_failures = False

%>
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="en-US">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <!-- <meta http-equiv="refresh" content="60" /> -->
        <title>${ title }</title>
        <link rel="stylesheet" href="http://kernel.ubuntu.com/media/kernel-style.css" type="text/css" media="screen" />
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
                            <a href="http://ubuntu.com" title="Home" rel="home"><img src="http:///kernel.ubuntu.com/media/ubuntu-logo.png" alt="Home" /></a>
                        </div>
                        <h1>Kernel Iozone Benchmarks</h1>
                    </div> <!-- header -->

                    <br />

                    <div class="dash-section">
                        <table width="100%" border="0" style="font-size: 0.9em">
                            <tr> <td width="100" align="right">timestamp :</td> <td width="2">&nbsp;</td> <td align="left">${ test_attributes['timestamp'] }</td> </tr>
                            <tr> <td width="100" align="right">kernel :</td> <td width="2">&nbsp;</td> <td align="left">${ test_attributes['kernel'] }</td> </tr>
                            <tr> <td width="100" align="right">job :</td> <td width="2">&nbsp;</td> <td align="left">${ test_attributes['environ']['JOB_NAME'] }</td> </tr>
                            <tr> <td width="100" align="right">results :</td> <td width="2">&nbsp;</td> <td align="left"><a href="iozone/html_out/index.html">charts</a></td> </tr>
                            <tr> <td width="100" align="right">console output :</td> <td width="2">&nbsp;</td> <td align="left"><a href="console_output.txt.html">log</a></td> </tr>
                        </table>
                    </div>

                    <div class="dash-section">
                        <table width="100%">
                            <%
                                failed = 0
                            %>
                            <tr>
                                <td width="100%" valign="top">
                                    <table width="100%" style="font-size: 0.9em">
                                        <tr>
                                            <td style="background: #e9e7e5;" colspan="6"><span style="font-weight: normal;font-size: 14px;">Test Suites</span></td>
                                        </tr>
                                        <tr>
                                            <th width="10">&nbsp;</th><th>Suite</th> <th>Duration</th> <th>Fail</th> <th>Skip</th> <th>Total</th>
                                        <tr>

                                        % for suite in test_results['suites']:
                                        <%
                                            name = suite['name'].replace('autotest.','')
                                            name_link = "%s-test-suite.html" % (name)

                                            hrs = suite['duration'] / 3600
                                            minutes = (suite['duration'] / 60) % 60

                                            if hrs > 0:
                                                duration = "%d hr %d min" % (hrs, minutes)
                                            else:
                                                duration = "%d min" % (minutes)

                                            failed = suite['tests failed']

                                            if failed:
                                                test_failures = True
                                        %>
                                        <tr>
                                            <td>&nbsp;</td><td><a href="${ name_link }">${ name }</a></td> <td>${ duration }</td> <td><a href="${ name_link }">${ suite['tests failed'] }</a></td> <td><a href="${ name_link }">${ suite['tests skipped'] }</a></td> <td><a href="${ name_link }">${ suite['tests run'] }</a></td>
                                        </tr>
                                        % endfor
                                    </table>
                                </td>
                            </tr>
                            % if test_failures:
                            <tr>
                                <td width="100%" valign="top">
                                    <table width="100%" style="font-size: 0.9em">
                                        <tr><td> &nbsp; </td></tr>
                                        <tr>
                                            <td style="background: #e9e7e5;" colspan="6"><span style="font-weight: normal;font-size: 14px;">Errors</span></td>
                                        </tr>
                                        <tr>
                                            <th width="10">&nbsp;</th><th>Name</th> <th width="100" align="center">Duration</th>
                                        </tr>
                                        % for suite in test_results['suites']:
                                            % for case in suite['cases']:
                                                % if 'errorDetails' in case:
                                                <%
                                                    name = suite['name'].replace('autotest.','')
                                                    hrs = case['duration'] / 3600
                                                    minutes = (case['duration'] / 60) % 60
                                                    seconds = case['duration'] % 60

                                                    if hrs > 0:
                                                        duration = "%d hr %d min" % (hrs, minutes)
                                                    elif minutes > 0:
                                                        duration = "%d min" % (minutes)
                                                    else:
                                                        duration = "%d sec" % (seconds)

                                                    error_link = "%s" % name
                                                    error_link += "/results/%s.%s/debug/%s.%s.DEBUG.html" % (name, case['name'], name, case['name'])
                                                %>
                                                <tr>
                                                    <td>&nbsp;</td><td><a href="${ error_link }">${ case['name'] }</a></td> <td align="right">${ duration }</td>
                                                </tr>
                                                % endif
                                            % endfor
                                        % endfor
                                    </table>
                                </td>
                            </tr>
                            % endif
                        </table>
                    </div> <!-- dash-section -->

                    <div class="index-bottom-section">
                        <table width="100%">
                            <tr>
                                <td align="left" valign="bottom" colspan="5">
                                  <span style="font-size: 10px; color: #aea79f !important">(c) 2012 Canonical Ltd. Ubuntu and Canonical are registered trademarks of Canonical Ltd.  (template: ingest-index.mako)</span>
                                </td>
                                <td align="right" valign="top">
                                    <a href="http://ubuntu.com"><img src="http://kernel.ubuntu.com/media/ubuntu-footer-logo.png"></a>
                                </td>
                            </tr>
                        </table>
                    </div>

                </div>
            </div>
        </div>
    </body>

</html>
<!-- vi:set ts=4 sw=4 expandtab syntax=mako: -->

