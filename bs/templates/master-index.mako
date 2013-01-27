<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<%
   sys_data = template_data
%>
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="en-US">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	    <title>${report_title}</title>

        <link title="light" rel="stylesheet" href="http://people.canonical.com/~kernel/reports/css/themes/blue/style.css" type="text/css" media="print, projection, screen" />
        <link title="light" rel="stylesheet" href="http://people.canonical.com/~kernel/reports/css/light-style.css" type="text/css" media="print, projection, screen" />

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

            <div>
                <p>&nbsp;</p>
            </div>

            <div class="boot-table">
                <table id="boot-speed-results" class="tablesorter" border="0" cellpadding="0" cellspacing="1" width="100%%">
                    <thead>
                        <tr>
                            <th width="120">Timestamp</th>
                            <th width="100">Series</th>
                            <th width="100">Mac Address</th>
                            <th width="100">User</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for k in sys_data:
                            <%
                                props = sys_data[k]['properties']
                                data  = sys_data[k]['data']
                            %>
                            <tr>
                                <td>${props['timestamp']}</td>
                                <td>${props['series_name']}</td>
                                <td>${props['mac_address']}</td>
                                <td>${props['whoami']}</td>
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
    </body>

</html>
<!-- vi:set ts=4 sw=4 expandtab syntax=mako: -->
