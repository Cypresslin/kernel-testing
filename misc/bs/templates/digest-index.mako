<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="en-US">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <!-- <meta http-equiv="refresh" content="60" /> -->
        <title>Ubuntu - Kernel Team Server</title>
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
                            <a href="http://ubuntu.com" title="Home" rel="home"><img src="http://kernel.ubuntu.com/media/ubuntu-logo.png" alt="Home" /></a>
                        </div>
                        <h1>Boot Speed Testing</h1>
                    </div> <!-- header -->

                    <br />

                    <div class="dash-section">
                        <table width="100%"> <!-- The section is one big table -->
                            <tr>
                                <td width="100%" valign="top">
                                    <table width="100%" style="font-size: 0.9em" border="0">
                                        % for mac in index['mac_address']:
                                        <tr>
                                            <%
                                                link = '%s.html' % mac.replace(':', '-')
                                                try:
                                                    section_heading = '%s &nbsp; (%s)' % (systems[mac], template_data[index['mac_address'][mac][0]]['properties']['whoami'])
                                                except KeyError:
                                                    section_heading = mac
                                            %>
                                            <td style="background: #e9e7e5;"><a href="${link}">${section_heading}</a></td>
                                        </tr>
                                        <tr>
                                            <td width="100%">
                                                <table width="100%" border="0">
                                                    <thead>
                                                        <tr>
                                                            <th colspan="5">&nbsp;</th>
                                                            <th align="center" colspan="6">Mean Times (sec.)</th>
                                                        </tr>
                                                        <tr>
                                                            <th align="left" width="120">Bootspeed Run</th>
                                                            <th align="left" width="100">Kernel</th>
                                                            <th align="left" width="100">Series</th>

                                                            <th align="left">&nbsp;</th> <!-- Column Separator -->

                                                            <th align="center" width="80">Boot</th>
                                                            <th align="center" width="80">Desktop</th>
                                                            <th align="center" width="80">Kernel</th>
                                                            <th align="center" width="80">Kernel Init</th>
                                                            <th align="center" width="80">Plumbing</th>
                                                            <th align="center" width="80">Xorg</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        % for k in index['mac_address'][mac]:
                                                            <%
                                                                props = template_data[k]['properties']
                                                                data  = template_data[k]['data']
                                                                url   = "%s__%s__%s/index.html" % (mac.replace(':', '.'), props['timestamp'], props['whoami'])
                                                            %>
                                                            <tr>
                                                                <td><%t = props['timestamp'].replace('_', ' ')%><a href="${url}">${t}</a></td>
                                                                <td>${props['kernel_version']}</td>
                                                                <td>${props['series_name']}</td>

                                                                <td align="left">&nbsp;</td> <!-- Column Separator -->

                                                                <td align="center"><% t = '%02.2f' % data['boot']['mean'] %>${t}</td>
                                                                <td align="center"><% t = '%02.2f' % data['desktop']['mean'] %>${t}</td>
                                                                <td align="center"><% t = '%02.2f' % data['kernel']['mean'] %>${t}</td>
                                                                <td align="center"><% t = '%02.2f' % data['kernelinit']['mean'] %>${t}</td>
                                                                <td align="center"><% t = '%02.2f' % data['plumbing']['mean'] %>${t}</td>
                                                                <td align="center"><% t = '%02.2f' % data['xorg']['mean'] %>${t}</td>
                                                            </tr>

                                                        % endfor
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr> <td>&nbsp;</td> </tr>
                                        % endfor
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
    </body>

</html>
<!-- vi:set ts=4 sw=4 expandtab syntax=mako: -->

