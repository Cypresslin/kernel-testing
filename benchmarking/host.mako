<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<%
from datetime     import timedelta
%>
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="en-US">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <!-- <meta http-equiv="refresh" content="60" /> -->
        <title>${ title }</title>
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
                            <a href="http://ubuntu.com" title="Home" rel="home"><img src="http:///kernel.ubuntu.com/beta/media/ubuntu-logo.png" alt="Home" /></a>
                        </div>
                        <h1>Kernel Testing &amp; Benchmarks</h1>
                    </div> <!-- header -->

                    <br />

                    <div class="dash-section">
                        <table width="100%" border="0" style="font-size: 1.0em">
                            % for k in data:
                            <tr> <td width="100" align="right">${ k }:</td> <td width="2">&nbsp;</td> <td align="left">${ data[k] }</td> </tr>
                            % endfor
                        </table>
                    </div>

                    <div class="index-bottom-section">
                        <table width="100%">
                            <tr>
                                <td align="left" valign="bottom" colspan="5">
                                  <span style="font-size: 10px; color: #aea79f !important">(c) 2012 Canonical Ltd. Ubuntu and Canonical are registered trademarks of Canonical Ltd.</span>
                                </td>
                                <td align="right" valign="top">
                                    <a href="http://ubuntu.com"><img src="http://kernel.ubuntu.com/beta/media/ubuntu-footer-logo.png"></a>
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

