<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="en-US">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <!-- <meta http-equiv="refresh" content="60" /> -->
        <title>Ubuntu - Kernel Team Server</title>
        <link rel="stylesheet" href="http://kernel.ubuntu.com/beta/media/kernel-style.css" type="text/css" media="screen" />
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
                            <a href="http://ubuntu.com" title="Home" rel="home"><img src="http://kernel.ubuntu.com/beta/media/ubuntu-logo.png" alt="Home" /></a>
                        </div>
                        <h1>Kernel Testing &amp; Benchmarks</h1>
                    </div> <!-- header -->

                    <br />

                    <h1>Testing</h1>
                    <div class="dash-section">
                        <table width="100%"> <!-- The section is one big table -->
                            <tr>
                                <td width="100%" valign="top">
                                    <table width="100%" style="font-size: 0.9em"> <!-- SRU Data -->
                                        % for ubuntu_series in sorted(data, reverse=True):
                                        <tr>
                                            <td style="background: #e9e7e5;">${ubuntu_series}</td>
                                        </tr>
                                        <tr>
                                            <td width="100%">
                                                <table id="" width="100%" border="0">
                                                    <tbody>
                                                        % for kernel_version in data[ubuntu_series]:
                                                        <tr>
                                                            <td>
                                                                <table width="100%">
                                                                    <tr>
                                                                        <td align="left" width="150">${ kernel_version } </td> <td> </td>
                                                                    </tr>
                                                                </table>
                                                            <td>
                                                        </tr>
                                                        <tr>
                                                            <td>
                                                                <table width="100%" border="0">
                                                                    <tbody>
                                                                    <tr>
                                                                        <th width="100">&nbsp;</th>
                                                                        <th align="left" width="100">&nbsp; Host &nbsp;</th>
                                                                        <th align="left" width="40">&nbsp; Arch &nbsp;</th>
                                                                        <th align="center" width="150">Date</th>

                                                                        <th align="center" width="40">Ran</th>
                                                                        <th align="center" width="40">Passed</th>
                                                                        <th align="center" width="40">Failed</th>

                                                                        <th align="center"><!--Benchmarks--></th>
                                                                    </tr>
                                                                        % for record in data[ubuntu_series][kernel_version]:
                                                                        <%
                                                                            total = 0
                                                                            passed = 0
                                                                            failed = 0
                                                                            for suite in record['results']['suites']:
                                                                                total += suite['tests run']
                                                                                passed += suite['tests run'] - suite['tests failed']
                                                                                failed += suite['tests failed']

                                                                            link = "http://kernel.ubuntu.com/beta/testing/test-results/%s.%s/results-index.html" % (record['attributes']['environ']['NODE_NAME'], record['attributes']['environ']['BUILD_ID'])
                                                                        %>
                                                                        <tr>
                                                                            <td>&nbsp;</td>
                                                                            <td><a href="test-results/${ record['attributes']['environ']['NODE_NAME'] }.html">${ record['attributes']['environ']['NODE_NAME'] }</a></td><td>${ record['attributes']['platform']['arch']['bits'] } </td> <td align="center">${ record['attributes']['timestamp'] }</td> <td align="center"><a href="${ link }">${ total }</a></td> <td align="center"><a href="${ link }">${ passed }</a></td> <td align="center"><a href="${ link }">${ failed }</a></td><td></td>
                                                                        </tr>
                                                                        % endfor
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                        % endfor
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        % endfor
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </div> <!-- dash-section -->

                    <h1>Benchmarks</h1>
                    <div class="dash-section">
                        <table width="100%">
                            <tr> <td style="background: #e9e7e5;">quantal</td> </tr>
                            <tr>
                                <td>
                                    <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                        <td width="5">&nbsp;</td>
                                        <td>
                                            <table border="0" cellpadding="0" cellspacing="0">
                                                <tr>
                                                    <th width="100">&nbsp;</th>
                                                    <th align="center" colspan="2" style="border-color: green; border-width: 0 0 1px 0; border-style: solid;"><a href="test-results/statler.html">statler</a></th>
                                                    <th width="10">&nbsp;</th>
                                                    <th align="center" colspan="2" style="border-color: green; border-width: 0 0 1px 0; border-style: solid;"><a href="test-results/waldorf.html">waldorf</a></th>
                                                </tr>
                                                <tr>
                                                    <td>bonnie</td>
                                                    <td align="center" width="100"><a href="benchmarks/statler-bonnie-3.4.0-all.html">all</a></td> <td align="center" width="100"><a href="benchmarks/statler-bonnie-3.4.0.html">block &amp; char i/o</a></td>
                                                    <td>&nbsp;</td>
                                                    <td align="center" width="100"><a href="benchmarks/waldorf-bonnie-3.4.0-all.html">all</a></td> <td align="center" width="100"><a href="benchmarks/waldorf-bonnie-3.4.0.html">block &amp; char i/o</a></td>
                                                </tr>
                                                <tr>
                                                    <td>compilebench</td>
                                                    <td align="center" colspan="2"><a href="benchmarks/statler-compilebench-3.4.0.html">results</a>
                                                    <td>&nbsp;</td>
                                                    <td align="center" colspan="2"><a href="benchmarks/waldorf-compilebench-3.4.0.html">results</a>
                                                </tr>
                                                <tr>
                                                    <td>dbench</td>
                                                    <td align="center" colspan="2"><a href="benchmarks/statler-bonnie-3.4.0.html">results</a></td>
                                                    <td>&nbsp;</td>
                                                    <td align="center" colspan="2"><a href="benchmarks/waldorf-bonnie-3.4.0.html">results</a></td>
                                                </tr>
                                            </table>
                                        </td>
                                    </table>
                                </td>
                            </tr>

                            <tr><td>&nbsp;</td></tr>

                            <tr> <td style="background: #e9e7e5;">precise</td> </tr>
                            <tr>
                                <td>
                                    <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                        <td width="5">&nbsp;</td>
                                        <td>
                                            <table border="0" cellpadding="0" cellspacing="0">
                                                <tr>
                                                    <th width="100">&nbsp;</th>
                                                    <th align="center" colspan="2" style="border-color: green; border-width: 0 0 1px 0; border-style: solid;"><a href="test-results/statler.html">statler</a></th>
                                                    <th width="10">&nbsp;</th>
                                                    <th align="center" colspan="2" style="border-color: green; border-width: 0 0 1px 0; border-style: solid;"><a href="test-results/waldorf.html">waldorf</a></th>
                                                </tr>
                                                <tr>
                                                    <td>bonnie</td>
                                                    <td align="center" width="100"><a href="benchmarks/statler-bonnie-3.2.0-all.html">all</a></td> <td align="center" width="100"><a href="benchmarks/statler-bonnie-3.2.0.html">block &amp; char i/o</a></td>
                                                    <td>&nbsp;</td>
                                                    <td align="center" width="100"><a href="benchmarks/waldorf-bonnie-3.2.0-all.html">all</a></td> <td align="center" width="100"><a href="benchmarks/waldorf-bonnie-3.2.0.html">block &amp; char i/o</a></td>
                                                </tr>
                                                <tr>
                                                    <td>compilebench</td>
                                                    <td align="center" colspan="2"><a href="benchmarks/statler-compilebench-3.2.0.html">results</a></td>
                                                    <td>&nbsp;</td>
                                                    <td align="center" colspan="2"><a href="benchmarks/waldorf-compilebench-3.2.0.html">results</a></td>
                                                </tr>
                                                <tr>
                                                    <td>dbench</td>
                                                    <td align="center" colspan="2"><a href="benchmarks/statler-bonnie-3.2.0.html">results</a></td>
                                                    <td>&nbsp;</td>
                                                    <td align="center" colspan="2"><a href="benchmarks/waldorf-bonnie-3.2.0.html">results</a></td>
                                                </tr>
                                            </table>
                                        </td>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </div>

                    <div class="index-bottom-section">
                        <table width="100%"> <!-- The section is one big table -->
                            <tr>
                                <td align="left" valign="bottom" colspan="5">
                                  <span style="font-size: 10px; color: #aea79f !important">(c) 2012 Canonical Ltd. Ubuntu and Canonical are registered trademarks of Canonical Ltd.</span>
                                </td>
                                <td align="right" valign="top">
                                    <a href="http://ubuntu.com"><img src="http://kernel.ubuntu.com/beta/media/ubuntu-footer-logo.png"></a>
                                </td>
                            </tr>
                        </table>
                    </div> <!-- dash-section -->

                </div>
            </div>
        </div>
    </body>

</html>
<!-- vi:set ts=4 sw=4 expandtab syntax=mako: -->

