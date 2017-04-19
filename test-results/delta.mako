<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="en-US">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <!-- <meta http-equiv="refresh" content="60" /> -->
        <title>Ubuntu - Kernel Team Server</title>
        <link rel="stylesheet" href="http://kernel.ubuntu.com/media/kernel-style.css" type="text/css" media="screen" />
        <style type="text/css">
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
                        <h1>Kernel Testing</h1>
                    </div> <!-- header -->

                    <br />

                    <!-- series | flavour | kernel | 'suites-results' | arch | suite -->

                    <div class="dash-section">
                        <table width="100%"> <!-- The section is one big table -->
                            <tr>
                                <td width="100%" valign="top">
                                    <table width="100%" style="font-size: 0.9em"> <!-- SRU Data -->
                                        % for ubuntu_series in sorted(data, reverse=True):
                                        <tr>
                                            <td style="background: #ffff99;"><strong>${ubuntu_series}</strong></td>
                                        </tr>
                                        <tr>
                                            <td width="100%">

                                                % for flavour in sorted(data[ubuntu_series], reverse=True):

                                                    <table id="" width="100%" border="0">
                                                        <tbody>
                                                            % for kernel_version in sorted(data[ubuntu_series][flavour], reverse=True):
                                                            <tr>
                                                                <td align="left" width="150" colspan="7">${ kernel_version }</td> <td> </td>
                                                            </tr>
                                                                % for arch in sorted(data[ubuntu_series][flavour][kernel_version]['suites-results']):
                                                                    <tr>
                                                                        <th width="100">&nbsp;</th>
                                                                        <td align="center" colspan="7" style="background: #e9e7e5;">${ arch } </td>
                                                                    </tr>
                                                                    % if len(data[ubuntu_series][flavour][kernel_version]['suites-results'][arch]) == 1:
                                                                        <tr>
                                                                            <th width="100">&nbsp;</th>
                                                                            <th align="center" width="140">Suite</th>
                                                                            <th align="center" width="50">Passed</th>
                                                                            <th align="center" width="50">Failed</th>
                                                                            <th width="50">&nbsp;</th>
                                                                            <th align="center" width="140"></th>
                                                                            <th align="center" width="50"></th>
                                                                            <th align="center" width="50"></th>
                                                                        </tr>
                                                                    % else:
                                                                        <tr>
                                                                            <th width="100">&nbsp;</th>
                                                                            <th align="center" width="140">Suite</th>
                                                                            <th align="center" width="50">Passed</th>
                                                                            <th align="center" width="50">Failed</th>
                                                                            <th width="50">&nbsp;</th>
                                                                            <th align="center" width="140">Suite</th>
                                                                            <th align="center" width="50">Passed</th>
                                                                            <th align="center" width="50">Failed</th>
                                                                        </tr>
                                                                    % endif
                                                                    <tr>
                                                                        <td width="100">&nbsp;</td>
                                                                        <% suite_row = 0 %>
                                                                        % for suite in sorted(data[ubuntu_series][flavour][kernel_version]['suites-results'][arch]):
                                                                                <%
                                                                                    suite_row += 1
                                                                                    passed = data[ubuntu_series][flavour][kernel_version]['suites-results'][arch][suite]['passed']
                                                                                    pdelta = data[ubuntu_series][flavour][kernel_version]['suites-results'][arch][suite]['pdelta']
                                                                                    if pdelta > 0:
                                                                                        pdelta = '(+%d)' % pdelta
                                                                                    elif pdelta == 0:
                                                                                        pdelta = '(nc)'
                                                                                    else:
                                                                                        pdelta = '(%d)' % pdelta
                                                                                    failed = data[ubuntu_series][flavour][kernel_version]['suites-results'][arch][suite]['failed']
                                                                                    fdelta = data[ubuntu_series][flavour][kernel_version]['suites-results'][arch][suite]['fdelta']
                                                                                    if fdelta > 0:
                                                                                        fdelta = '(+%d)' % fdelta
                                                                                    elif fdelta == 0:
                                                                                        fdelta = '(nc)'
                                                                                    else:
                                                                                        fdelta = '(%d)' % fdelta
                                                                                    link = 'https://null.com/'
                                                                                    # (passed, failed) = data[ubuntu_series][flavour][kernel_version]['suites-results'][arch][suite]['totals']
                                                                                    # link =             data[ubuntu_series][flavour][kernel_version]['suites-results'][arch][suite]['link']
                                                                                    link = data[ubuntu_series][flavour][kernel_version]['suites-results'][arch][suite]['link']
                                                                                %>
                                                                            <td align="left"  ><a href="${ link }">${ suite }</a></td>
                                                                            <td align="center"><a href="${ link }">${ passed } ${pdelta}</a></td>
                                                                            <td align="center"><a href="${ link }">${ failed } ${fdelta}</a></td>
                                                                            % if suite_row == 2:
                                                                                <% suite_row = 0 %>
                                                                    </tr>
                                                                    <tr>
                                                                        <td width="100">&nbsp;</td>
                                                                            % else:
                                                                        <td width="50">&nbsp;</td>
                                                                            % endif
                                                                        % endfor
                                                                        % if suite_row == 1:
                                                                    <tr>
                                                                        <td>&nbsp;</td>
                                                                    </tr>
                                                                        % endif
                                                                        </tr>
                                                                    </tr>
                                                                % endfor
                                                            % endfor
                                                        </tbody>
                                                    </table>

                                                % endfor

                                            </td>
                                        </tr>
                                        % endfor
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </div> <!-- dash-section -->

                    <div class="index-bottom-section">
                        <table width="100%">
                            <tr>
                                <td align="left" colspan="5">
                                    ${ timestamp }
                                </td>
                            </tr>
                            <tr>
                                <td align="left" valign="bottom" colspan="5">
                                  <span style="font-size: 10px; color: #aea79f !important">(c) 2012 Canonical Ltd. Ubuntu and Canonical are registered trademarks of Canonical Ltd.</span>
                                </td>
                                <td align="right" valign="top">
                                    <a href="http://ubuntu.com"><img src="http://kernel.ubuntu.com/media/ubuntu-footer-logo.png" alt="Home" /></a>
                                </td>
                            </tr>
                        </table>
                    </div> <!-- index-bottom-section -->

                </div>
            </div>
        </div>
    </body>

</html>
<!-- vi:set ts=4 sw=4 expandtab syntax=mako: -->

