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

                    <div class="dash-section">
                        <table width="100%"> <!-- The section is one big table -->
                            <tr>
                                <td width="100%" valign="top">
                                    <table width="100%" style="font-size: 0.9em" border="0"> <!-- SRU Data -->
                                        <tr>
                                            <td style="background: #e9e7e5;" width="33%" align="left"><strong>${data['suite']}</strong></td>
                                            <td style="background: #e9e7e5;" width="33%" align="center"><strong>${data['kernel']} </strong></td>
                                            <td style="background: #e9e7e5;" width="33%" align="right"><strong>${data['arch']} </strong></td>
                                        </tr>
                                        <tr>
                                            <td width="100%" colspan="3">
                                                <table id="" width="100%" border="0">
                                                    <tbody>
                                                        <tr>
                                                            <th align="left" width="100">&nbsp; Host &nbsp;</th>
                                                            <th align="center" width="150">Date</th>

                                                            <th align="center" width="45">Ran</th>
                                                            <th align="center" width="45">Passed</th>
                                                            <th align="center" width="45">Failed</th>
                                                            <th>&nbsp;</th>
                                                        </tr>
                                                        % for i in range(0, len(data['jobs'])):
                                                            <%
                                                            (jname, host, passed, failed) = data['jobs'][i]
                                                            try:
                                                                timestamp = data['timestamp']
                                                                ran = passed + failed
                                                                link = '%s/%s-test-suite.html' % (jname, data['suite'])
                                                            except ValueError:
                                                                continue
                                                            %>
                                                            <tr>
                                                                <td>${ host }</td>
                                                                <td align="center">${timestamp}</a></td>
                                                                <td align="center"><a href="${link}">${ran}</a></td>
                                                                <td align="center"><a href="${link}">${passed}</a></td>
                                                                <td align="center"><a href="${link}">${failed}</a></td>
                                                                <td>&nbsp;</td>
                                                            </tr>
                                                        % endfor
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </div> <!-- dash-section -->

                    <div class="index-bottom-section">
                        <table width="100%">
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

