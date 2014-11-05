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
                        <h1>Kernel Benchmarks</h1>
                    </div> <!-- header -->

                    <br />

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
                                                        <tr>
                                                            <th width="100">Kernel</th>
                                                            <th align="left" width="100">&nbsp; Host &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; Arch &nbsp;</th>
                                                            <th align="center" width="40">&nbsp; HW &nbsp;</th>
                                                            <th align="center" width="150">Date</th>

                                                            <th align="center" width="45">Ran</th>
                                                            <th align="center" width="45">Passed</th>
                                                            <th align="center" width="45">Failed</th>

                                                            <th align="left">Notes</th>
                                                        </tr>
                                                        % for kernel_version in data[ubuntu_series]:
                                                        <tr>
                                                            <td align="left" width="150" colspan="8">${ kernel_version } </td> <td> </td>
                                                        </tr>
                                                            % for record in data[ubuntu_series][kernel_version]:
                                                            <%
                                                                from datetime import datetime
                                                                notes = ''
                                                                total = 0
                                                                passed = 0
                                                                failed = 0
                                                                for suite in record['results']['suites']:
                                                                    total += suite['tests run']
                                                                    passed += suite['tests run'] - suite['tests failed']
                                                                    failed += suite['tests failed']

                                                                dt = datetime.strptime(record['attributes']['timestamp'], '%Y-%m-%d %H:%M')
                                                                ts = dt.strftime('%Y-%m-%d_%H-%M-%S')
                                                                link = "http://kernel.ubuntu.com/benchmarking/stluser/iozone-nolazy/%s__%s__%s/results-index.html" % (record['attributes']['platform']['hostname'], record['attributes']['kernel'], ts)

                                                                hardware = 'real'
                                                                if 'hardware' in record['attributes']['platform']:
                                                                    hardware = record['attributes']['platform']['hardware']
                                                                    if hardware == 'virtual' and 'virt host' in record['attributes']:
                                                                        notes += '(virt. host: %s)' % record['attributes']['virt host']['kernel version']

                                                                # Trim the 'bits' off
                                                                arch = record['attributes']['platform']['arch']['bits'].replace('bit', '')
                                                            %>
                                                            <tr>
                                                                <td>&nbsp;</td>
                                                                <td><a href="${ record['attributes']['platform']['hostname'] }.html">${ record['attributes']['platform']['hostname'] }</a></td>
                                                                <td align="center">${ arch } </td>
                                                                <td align="center">${hardware}</td>
                                                                <td align="center">${ record['attributes']['timestamp'] }</td>
                                                                <td align="center"><a href="${ link }">${ total }</a></td>
                                                                <td align="center"><a href="${ link }">${ passed }</a></td>
                                                                <td align="center"><a href="${ link }">${ failed }</a></td>
                                                                <td>${ notes }</td>
                                                            </tr>
                                                            % endfor
                                                        % endfor
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        % endfor
					<!-- SERIES ------------------------------------------------------------ -->
                                    <table width="100%" style="font-size: 0.9em"> <!-- inter-release results -->
                                      <tr>
                                        <td style="background: #e9e7e5;">Series To Series Comparisons</td>
                                      </tr>
                                        <tr>
                                            <td width="100%">
                                                <table id="" width="100%" border="0">
                                                    <tbody>
                                                        <tr>
                                                            <th width="100">Baseline</th>
                                                            <th align="left" width="100">&nbsp; Comparison &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; ext4 &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; ext4-nolazy &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; ext3 &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; ext2 &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; xfs &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; btrfs &nbsp;</th>
                                                        </tr>

                                                        % for scomp in seriespairs:
                                                        <%
							   from os import path
							   baseline   = '%s (%s)' % (scomp['first']['attributes']['distro-release-name'], scomp['first']['attributes']['kernel'])
							   comparison = '%s (%s)' % (scomp['second']['attributes']['distro-release-name'], scomp['second']['attributes']['kernel'])

							   lbase =  ""
							   ext4link = path.join(lbase, path.basename(scomp['path']), 'ext4/index.html')
							   ext4nolazylink = path.join(lbase, path.basename(scomp['path']), 'ext4-nolazy/index.html')
							   ext3link = path.join(lbase, path.basename(scomp['path']), 'ext3/index.html')
							   ext2link = path.join(lbase, path.basename(scomp['path']), 'ext2/index.html')
							   xfslink = path.join(lbase, path.basename(scomp['path']), 'xfs/index.html')
							   btrfslink = path.join(lbase, path.basename(scomp['path']), 'btrfs/index.html')
                                                         %>
                                                        <tr>
                                                          <td align="left">${ baseline }</td>
                                                          <td align="left">${ comparison }</td>
                                                          <td align="left"><a href="${ ext4link }">&nbsp; ext4 &nbsp;</a></td>
                                                          <td align="left"><a href="${ ext4nolazylink }">&nbsp; ext4-nolazy &nbsp;</a></td>
                                                          <td align="left"><a href="${ ext3link }">&nbsp; ext3 &nbsp;</a></td>
                                                          <td align="left"><a href="${ ext2link }">&nbsp; ext2 &nbsp;</a></td>
                                                          <td align="left"><a href="${ xfslink }">&nbsp; xfs &nbsp;</a></td>
                                                          <td align="left"><a href="${ btrfslink }">&nbsp; btrfs &nbsp;</a></td>
                                                        </tr>
                                                        % endfor
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
				    <!-- LTS ------------------------------------------------------------ -->
                                    <table width="100%" style="font-size: 0.9em"> <!-- inter-release results -->
                                      <tr>
                                        <td style="background: #e9e7e5;">LTS to LTS Comparisons</td>
                                      </tr>
                                        <tr>
                                            <td width="100%">
                                                <table id="" width="100%" border="0">
                                                    <tbody>
                                                        <tr>
                                                            <th width="100">Baseline</th>
                                                            <th align="left" width="100">&nbsp; Comparison &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; ext4 &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; ext4-nolazy &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; ext3 &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; ext2 &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; xfs &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; btrfs &nbsp;</th>
                                                        </tr>

                                                        % for lcomp in ltspairs:
                                                        <%
							   from os import path
							   baseline   = '%s (%s)' % (lcomp['first']['attributes']['distro-release-name'], lcomp['first']['attributes']['kernel'])
							   comparison = '%s (%s)' % (lcomp['second']['attributes']['distro-release-name'], lcomp['second']['attributes']['kernel'])

							   lbase =  ""
							   ext4link = path.join(lbase, path.basename(lcomp['path']), 'ext4/index.html')
							   ext4nolazylink = path.join(lbase, path.basename(lcomp['path']), 'ext4-nolazy/index.html')
							   ext3link = path.join(lbase, path.basename(lcomp['path']), 'ext3/index.html')
							   ext2link = path.join(lbase, path.basename(lcomp['path']), 'ext2/index.html')
							   xfslink = path.join(lbase, path.basename(lcomp['path']), 'xfs/index.html')
							   btrfslink = path.join(lbase, path.basename(lcomp['path']), 'btrfs/index.html')
                                                         %>
                                                        <tr>
                                                          <td align="left">${ baseline }</td>
                                                          <td align="left">${ comparison }</td>
                                                          <td align="left"><a href="${ ext4link }">&nbsp; ext4 &nbsp;</a></td>
                                                          <td align="left"><a href="${ ext4nolazylink }">&nbsp; ext4-nolazy &nbsp;</a></td>
                                                          <td align="left"><a href="${ ext3link }">&nbsp; ext3 &nbsp;</a></td>
                                                          <td align="left"><a href="${ ext2link }">&nbsp; ext2 &nbsp;</a></td>
                                                          <td align="left"><a href="${ xfslink }">&nbsp; xfs &nbsp;</a></td>
                                                          <td align="left"><a href="${ btrfslink }">&nbsp; btrfs &nbsp;</a></td>
                                                        </tr>
                                                        % endfor
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
				    <!-- VERSIONS ------------------------------------------------------------ -->
                                    <table width="100%" style="font-size: 0.9em"> <!-- inter-release results -->
                                      <tr>
                                        <td style="background: #e9e7e5;">Version to Version Comparisons</td>
                                      </tr>
                                        <tr>
                                            <td width="100%">
                                                <table id="" width="100%" border="0">
                                                    <tbody>
                                                        <tr>
                                                            <th width="100">Baseline</th>
                                                            <th align="left" width="100">&nbsp; Comparison &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; ext4 &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; ext4-nolazy &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; ext3 &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; ext2 &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; xfs &nbsp;</th>
                                                            <th align="left" width="40">&nbsp; btrfs &nbsp;</th>
                                                        </tr>

                                                        % for vcomp in versionpairs:
                                                        <%
							   from os import path
							   baseline   = '%s (%s)' % (vcomp['first']['attributes']['distro-release-name'], vcomp['first']['attributes']['kernel'])
							   comparison = '%s (%s)' % (vcomp['second']['attributes']['distro-release-name'], vcomp['second']['attributes']['kernel'])

							   lbase =  ""
							   ext4link = path.join(lbase, path.basename(vcomp['path']), 'ext4/index.html')
							   ext3link = path.join(lbase, path.basename(vcomp['path']), 'ext3/index.html')
							   ext2link = path.join(lbase, path.basename(vcomp['path']), 'ext2/index.html')
							   xfslink = path.join(lbase, path.basename(vcomp['path']), 'xfs/index.html')
							   btrfslink = path.join(lbase, path.basename(vcomp['path']), 'btrfs/index.html')
                                                         %>
                                                        <tr>
                                                          <td align="left">${ baseline }</td>
                                                          <td align="left">${ comparison }</td>
                                                          <td align="left"><a href="${ ext4link }">&nbsp; ext4 &nbsp;</a></td>
                                                          <td align="left"><a href="${ ext4nolazylink }">&nbsp; ext4-nolazy &nbsp;</a></td>
                                                          <td align="left"><a href="${ ext3link }">&nbsp; ext3 &nbsp;</a></td>
                                                          <td align="left"><a href="${ ext2link }">&nbsp; ext2 &nbsp;</a></td>
                                                          <td align="left"><a href="${ xfslink }">&nbsp; xfs &nbsp;</a></td>
                                                          <td align="left"><a href="${ btrfslink }">&nbsp; btrfs &nbsp;</a></td>
                                                        </tr>
                                                        % endfor
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
<!-- BOTTOM ------------------------------------------------------------ -->				      
                                </td>
                            </tr>
                        </table>
                    </div> <!-- dash-section -->

                    <div class="index-bottom-section">
                        <table width="100%"> <!-- The section is one big table -->
                            <tr>
                                <td align="left" valign="bottom" colspan="5">
                                  <span style="font-size: 10px; color: #aea79f !important">(c) 2014 Canonical Ltd. Ubuntu and Canonical are registered trademarks of Canonical Ltd.</span>
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

