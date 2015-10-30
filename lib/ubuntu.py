#!/usr/bin/env python
#

import re

#
# Warning - using the following dictionary to get the series name from the kernel version works for the linux package,
# but not for some others (some ARM packages are known to be wrong). This is because the ARM kernels used for some
# series are not the same as the main kernels
#

# UbuntuError
#
class UbuntuError(Exception):
    # __init__
    #
    def __init__(self, error):
        self.msg = error

# Ubuntu
#
class Ubuntu:

    # db: dictionary of Ubuntu releases, with its kernel package, version
    # and miscelaneous information used by scripts throughout the tree
    #
    # Format:
    # db = {
    #   <release number string> : {
    #      'field 1' : <value 1>,
    #      'field 2' : <value 2>,
    #      ...
    #      'field n' : <value n>
    #   }
    # }
    #
    # release number string is the number of the release, '10.10', '12.04', etc.
    # For each release, we have a dictionary assigned to it which consists of a
    # set of fields with values assigned, relevant to that release. The possible
    # fields are:
    # * development (bool) - indicates if this release
    #   represents the current Ubuntu development release
    # * series_verson (string) - same as release number string. XXX: remove this?
    # * kernel (string) - the main kernel version used in this release (from
    #   linux package), eg. '3.2.0'
    # * name (string) - first name of this release, eg. 'precise'
    # * supported (bool) - indicates if this is an stable supported
    #   release (not a development release, and not EOL - end of life)
    # * packages (list) - list of source package names supported in this
    #   release.
    # * dependent-packages (dictionary) - dictionary mapping a package
    #   to its dependent packages. Format:
    #   'dependent-packages' : {
    #     <source package name> : {
    #       'task name 1' : <source package name 1 linked to this task>,
    #       'task name 2' : <source package name 2 linked to this task>,
    #       ...
    #       'task name n' : <source package name n linked to this task>
    #     }
    #   }
    #   - source package name is the name of the source package uploaded.
    #   - task name can be one of the following: 'meta', 'lbm', 'lrm',
    #     'lum', 'ports-meta', 'signed'
    #   The information on this dictionary is solely used as an way to
    #   process and create tracking bugs. Using this information the
    #   scripts can know which packages needs extra 'prepare-package-*'
    #   tasks in tracking bugs, and which package name relates to its
    #   respective 'prepare-package-*' task:
    #   - For 'meta', 'lbm', 'lrm', 'lum', 'ports-meta' and 'signed',
    #     they are used when opening a tracking bug to know if that
    #     tracking bug needs respectively the tasks
    #     'prepare-package-meta', 'prepare-package-lbm', etc.
    #   - For 'meta', 'lbm', 'lrm', 'lum' and 'ports-meta', shank bot
    #     (stable/sru-workflow-manager) uses the dictionary to know
    #     what's the package name for that task, to check if the package
    #     is built on the ppa with the needed ABI. For 'signed', it uses
    #     the dictionary to know what's the package name for the
    #     prepare-package-signed task, and to check if the package with
    #     same ABI-VERSION is built on the ppa.
    # * derivative-packages (dictionary) - dictionary solely used by
    #   shank bot to know which tracking bugs it needs to open for
    #   rebasable branches, when the master linux packages are built on
    #   the ppa. Format:
    #   'derivative-packages' : {
    #     <source package name A> : [
    #          <source package name 1>,
    #          <source package name 2>,
    #          ...
    #          <source package name n>
    #       ],
    #     <source package name B> : [ ... ],
    #     ...
    #     <source package name n> : [ ... ]
    #   }
    #   Example:
    #   'derivative-packages' : {
    #     'linux' : [ 'linux-ti-omap4', 'linux-armadaxp' ]
    #   }
    #   This example means for shank bot that when 'linux' package is
    #   built on the c-k-t PPA, open automatically tracking bugs for
    #   'linux-ti-omap4' and 'linux-armadaxp' packages so they can be
    #   rebased on top of linux master branch and worked on.
    # * backport-packages (dictionary) - if the release is an LTS
    #   (Long Term Support), this will provide a mapping of available
    #   backport packages on it, so shank bot can properly open new
    #   tracking bugs for them. It's different from derivative-packages
    #   field, because the tracking bug is opened when a linux master
    #   branch is built on another release, so this field serves as a
    #   reverse map. But the purpose is the same, and also is solely
    #   used to open new tracking bugs for backport packages.
    #   Format:
    #   'backport-packages' : {
    #     <backport source package name 1> : [
    #       <original source package name of backported package>,
    #       <release number from where it's being backported>
    #     ],
    #     ...
    #     <backport source package name N> : [ ... ]
    #   }
    #   Consider this backports-package entry for '10.04' (Lucid) for
    #   example:
    #   'backport-packages' : {
    #     'linux-lts-backport-oneiric' : [ 'linux', '11.10' ],
    #     'linux-lts-backport-natty' : [ 'linux', '11.04' ],
    #     'linux-lts-backport-maverick' : [ 'linux', '10.10' ],
    #    }
    #   Above we have listed the three backports it can have. Taking
    #   oneiric backport, the list means, we are backporting from
    #   'linux' package present on '11.10'.
    # * sha1 XXX: doesn't seem to be used anymore
    # * md5 XXX: doesn't seem to be used anymore
    db = {
        '16.04' :
        {
            'development' : True,        # This is the version that is currently under development
            'series_version' : '16.04',
            'kernel'    : '4.3.0',
            'name'      : 'xenial',
            'supported' : False,
            # adjust packages when this goes live
            'packages'  :
            [
                'linux',
                'linux-meta',
                'linux-raspi2',
                'linux-meta-raspi2',
            ],
            'dependent-packages' :
            {
                'linux' : {
                    'meta'   : 'linux-meta',
                    'signed' : 'linux-signed'
                },
                'linux-raspi2' : { 'meta' : 'linux-meta-raspi2' },
            },
            'derivative-packages' :
            {
                'linux' : [ 'linux-raspi2' ]
            },
            'sha1' : '',
            'md5' : ''
        },
        '15.10' :
        {
            'development' : False,        # This is the version that is currently under development
            'series_version' : '15.10',
            'kernel'    : '4.2.0',
            'name'      : 'wily',
            'supported' : True,
            # adjust packages when this goes live
            'packages'  :
            [
                'linux',
                'linux-meta',
                'linux-raspi2',
                'linux-meta-raspi2',
            ],
            'dependent-packages' :
            {
                'linux' : {
                    'meta'   : 'linux-meta',
                    'signed' : 'linux-signed'
                },
                'linux-raspi2' : { 'meta' : 'linux-meta-raspi2' },
            },
            'derivative-packages' :
            {
                'linux' : [ 'linux-raspi2' ]
            },
            'sha1' : '',
            'md5' : ''
        },
        '15.04' :
        {
            'development' : False,        # This is the version that is currently under development
            'series_version' : '15.04',
            'kernel'    : '3.19.0',
            'name'      : 'vivid',
            'supported' : True,
            # adjust packages when this goes live
            'packages'  :
            [
                'linux',
                'linux-meta',
            ],
            'dependent-packages' :
            {
                'linux' : {
                    'meta'   : 'linux-meta',
                    'signed' : 'linux-signed'
                },
            },
            'derivative-packages' :
            {
                'linux' : []
            },
            'sha1' : '',
            'md5' : ''
        },
        '14.10' :
        {
            'development' : False,        # This is the version that is currently under development
            'series_version' : '14.10',
            'kernel'    : '3.16.0',
            'name'      : 'utopic',
            'supported' : False,
            # adjust packages when this goes live
            'packages'  :
            [
                'linux',
                'linux-meta',
            ],
            'dependent-packages' :
            {
                'linux' : {
                    'meta'   : 'linux-meta',
                    'signed' : 'linux-signed'
                },
            },
            'derivative-packages' :
            {
                'linux' : []
            },
            'sha1' : '',
            'md5' : ''
        },
        '14.04' :
        {
            'development' : False,        # This is the version that is currently under development
            'series_version' : '14.04',
            'kernel'    : '3.13.0',
            'name'      : 'trusty',
            'supported' : True,
            # adjust packages when this goes live
            'packages'  :
            [
                'linux',
                'linux-meta',
                'linux-exynos5',
                'linux-keystone',
                'linux-meta-keystone',
                'linux-lts-utopic',
                'linux-meta-lts-utopic',
                'linux-signed-lts-utopic',
                'linux-lts-vivid',
                'linux-meta-lts-vivid',
                'linux-signed-lts-vivid',
            ],
            'dependent-packages' :
            {
                'linux' : {
                    'meta'   : 'linux-meta',
                    'signed' : 'linux-signed'
                },
                'linux-lts-utopic' : {
                    'meta' : 'linux-meta-lts-utopic',
                    'signed' : 'linux-signed-lts-utopic'
                },
                'linux-lts-vivid' : {
                    'meta' : 'linux-meta-lts-vivid',
                    'signed' : 'linux-signed-lts-vivid'
                },
                'linux-keystone' : { 'meta' : 'linux-meta-keystone' },
            },
            'derivative-packages' :
            {
                'linux' : ['linux-keystone']
            },
            'backport-packages' :
            {
                'linux-lts-utopic' : [ 'linux', '14.10' ],
                'linux-lts-vivid' : [ 'linux', '15.04' ],
                'linux-lts-wily' : [ 'linux', '15.10' ],
            },
            'sha1' : '',
            'md5' : ''
        },
        '13.10' :
        {
            'development' : False,
            'series_version' : '13.10',
            'kernel'    : '3.11.0',
            'name'      : 'saucy',
            'supported' : False,
            # adjust packages when this goes live
            'packages'  :
            [
                'linux',
                'linux-meta',
                'linux-exynos5',
            ],
            'dependent-packages' :
            {
                'linux' : {
                    'meta'   : 'linux-meta',
                    'signed' : 'linux-signed'
                },
                'linux-lowlatency' : { 'meta' : 'linux-meta-lowlatency' },
                'linux-ppc' : { 'meta' : 'linux-meta-ppc' }
            },
            'derivative-packages' :
            {
                'linux' : [ 'linux-lowlatency', 'linux-ppc' ]
            },
            'sha1' : '',
            'md5' : ''
        },
        '13.04' :
        {
            'development' : False,
            'series_version' : '13.04',
            'kernel'    : '3.8.0',
            'name'      : 'raring',
            'supported' : False,
            # adjust packages when this goes live
            'packages'  :
            [
                'linux',
                'linux-meta',
                'linux-meta-ti-omap4',
            ],
            'dependent-packages' :
            {
                'linux' : {
                    'meta'   : 'linux-meta',
                    'signed' : 'linux-signed'
                },
                'linux-lowlatency' : { 'meta' : 'linux-meta-lowlatency' },
                'linux-ppc' : { 'meta' : 'linux-meta-ppc' }
            },
            'derivative-packages' :
            {
                'linux' : [ 'linux-lowlatency', 'linux-ppc' ]
            },
            'sha1' : '',
            'md5' : ''
        },
        '12.10' :
        {
            'series_version' : '12.10',
            'kernel'    : '3.5.0',
            'name'      : 'quantal',
            'supported' : False,
            # adjust packages when this goes live
            'packages'  :
            [
                'linux',
                'linux-meta',
                'linux-ti-omap4',
                'linux-meta-ti-omap4',
                'linux-armadaxp',
                'linux-meta-armadaxp'
            ],
            'dependent-packages' :
            {
                'linux' : { 
                    'meta'   : 'linux-meta',
                    'lbm'    : 'linux-backports-modules-3.5.0',
                    'signed' : 'linux-signed'
                },
                'linux-ti-omap4' : { 'meta' : 'linux-meta-ti-omap4' },
                'linux-armadaxp' : { 'meta' : 'linux-meta-armadaxp' },
                'linux-lowlatency' : { 'meta' : 'linux-meta-lowlatency' }
            },
            'derivative-packages' :
            {
                'linux' : [ 'linux-ti-omap4', 'linux-armadaxp', 'linux-lowlatency' ]
            },
            'sha1' : '',
            'md5' : ''
        },
        '12.04' :
        {
            'series_version' : '12.04',
            'kernel'    : '3.2.0',
            'name'      : 'precise',
            'supported' : True,
            # adjust packages when this goes live
            'packages'  :
            [
                'linux',
                'linux-meta',
                'linux-lts-quantal',
                'linux-meta-lts-quantal',
                'linux-signed-lts-quantal',
                'linux-lts-raring',
                'linux-meta-lts-raring',
                'linux-signed-lts-raring',
                'linux-lts-saucy',
                'linux-meta-lts-saucy',
                'linux-signed-lts-saucy',
                'linux-ti-omap4',
                'linux-meta-ti-omap4',
                'linux-armadaxp',
                'linux-lts-trusty',
                'linux-meta-lts-trusty',
                'linux-signed-lts-trusty',
                'linux-meta-armadaxp'
            ],
            'dependent-packages' :
            {
                'linux' : {
                    'meta' : 'linux-meta',
                    'lbm'  : 'linux-backports-modules-3.2.0'
                },
                'linux-lts-quantal' : {
                    'meta' : 'linux-meta-lts-quantal',
                    'signed' : 'linux-signed-lts-quantal'
                },
                'linux-lts-raring' : {
                    'meta' : 'linux-meta-lts-raring',
                    'signed' : 'linux-signed-lts-raring'
                },
                'linux-lts-saucy' : {
                    'meta' : 'linux-meta-lts-saucy',
                    'signed' : 'linux-signed-lts-saucy'
                },
                'linux-lts-trusty' : {
                    'meta' : 'linux-meta-lts-trusty',
                    'signed' : 'linux-signed-lts-trusty'
                },
                'linux-ti-omap4' : { 'meta' : 'linux-meta-ti-omap4' },
                'linux-armadaxp' : { 'meta' : 'linux-meta-armadaxp' }
                #'linux-lowlatency' : { 'meta' : 'linux-meta-lowlatency' }
            },
            'derivative-packages' :
            {
                'linux' : [ 'linux-ti-omap4', 'linux-armadaxp' ] # 'linux-lowlatency'
            },
            'backport-packages' :
            {
                #'linux-lts-quantal' : [ 'linux', '12.10' ],
                #'linux-lts-raring' : [ 'linux', '13.04' ],
                #'linux-lts-saucy' : [ 'linux', '13.10' ],
                'linux-lts-trusty' : [ 'linux', '14.04' ],
            },
            'sha1' : '',
            'md5' : ''
        },
        '11.10' :
        {
            'series_version' : '11.10',
            'kernel'    : '3.0.0',
            'name'      : 'oneiric',
            'supported' : False,
            # adjust packages when this goes live
            'packages'  :
            [
                'linux',
                'linux-meta',
                'linux-ti-omap4',
                'linux-meta-ti-omap4'
            ],
            'dependent-packages' :
            {
                'linux' : { 
                    'meta' : 'linux-meta',
                    'lbm'  : 'linux-backports-modules-3.0.0'
                },
                'linux-ti-omap4' : { 'meta' : 'linux-meta-ti-omap4' }
            },
            'derivative-packages' :
            {
                'linux' : [ 'linux-ti-omap4' ]
            },
            'sha1' : '',
            'md5' : ''
        },
        '11.04' :
        {
            'series_version' : '11.04',
            'kernel'    : '2.6.38',
            'name'      : 'natty',
            'supported' : False,
            'packages'  :
            [
                'linux',
                'linux-meta',
                'linux-ti-omap4',
                'linux-meta-ti-omap4',
                'linux-backports-modules-2.6.38'
            ],
            'dependent-packages' :
            {
                'linux' : {
                    'meta' : 'linux-meta',
                    'lbm'  : 'linux-backports-modules-2.6.38'
                },
                'linux-ti-omap4' : { 'meta' : 'linux-meta-ti-omap4' }
            },
            'derivative-packages' :
            {
                'linux' : [ 'linux-ti-omap4' ]
            },
            'sha1' : '0770b9d2483eaeee4b80aec1fd448586b882003e',
            'md5' : 'cf0b587742611328f095da4b329e9fc7'
        },
        '10.10' :
        {
            'series_version' : '10.10',
            'kernel' : '2.6.35',
            'name' : 'maverick',
            'supported' : False,
            'packages' :
            [
                'linux',
                'linux-ti-omap4',
                'linux-mvl-dove',
                'linux-meta',
                'linux-ports-meta',
                'linux-meta-mvl-dove',
                'linux-meta-ti-omap4',
                'linux-backports-modules-2.6.35'
            ],
            'dependent-packages' :
            {
                'linux' : {
                    'meta' : 'linux-meta',
                    'ports-meta' : 'linux-ports-meta',
                    'lbm': 'linux-backports-modules-2.6.35'
                },
                'linux-ti-omap4' : { 'meta' : 'linux-meta-ti-omap4' },
                'linux-mvl-dove' : { 'meta' :  'linux-meta-mvl-dove' }
            },
            'derivative-packages' :
            {
                'linux' : [ 'linux-ti-omap4', 'linux-mvl-dove' ]
            },
            'sha1' : 'a2422f9281766ffe2f615903712819b9b0d9dd52',
            'md5' : '62001687bd94d1c0dd9a3654c64257d6'
        },
        '10.04' :
        {
            'series_version' : '10.04',
            'kernel' : '2.6.32',
            'name' : 'lucid',
            'supported' : False,
            'packages' :
            [
                'linux',
                'linux-ec2',
                'linux-meta',
                'linux-ports-meta',
                'linux-meta-ec2',
                'linux-backports-modules-2.6.32',
            ],
            'dependent-packages' :
            {
                'linux' : {
                    'meta' : 'linux-meta',
                    'ports-meta' : 'linux-ports-meta',
                    'lbm' : 'linux-backports-modules-2.6.32'
                },
                'linux-ec2' : { 'meta' : 'linux-meta-ec2' },
            },
            'derivative-packages' :
            {
                'linux' : [ 'linux-ec2' ]
            },
            'sha1' : '298cbfdb55fc64d1135f06b3bed3c8748123c183',
            'md5' : '4b1f6f6fac43a23e783079db589fc7e2'
        },
        '9.10' :
        {
            'series_version' : '9.10',
            'kernel' : '2.6.31',
            'name' : 'karmic',
            'supported' : False,
            'packages' :
            [
                'linux',
                'linux-fsl-imx51',
                'linux-mvl-dove',
                'linux-ec2',
                'linux-meta',
                'linux-ports-meta',
                'linux-meta-ec2',
                'linux-meta-mvl-dove',
                'linux-meta-fsl-imx51',
                'linux-backports-modules-2.6.31'
            ],
            'sha1' : '6b19c2987b0e2d74dcdca2aadebd5081bc143b72',
            'md5' : '16c0355d3612806ef87addf7c9f8c9f9'
        },
        '9.04' :
        {
            'series_version' : '9.04',
            'kernel' : '2.6.28',
            'name' : 'jaunty',
            'supported' : False,
            'packages' : [],
            'sha1' : '92d6a293200566646fbb9215e0633b4b9312ad38',
            'md5' : '062c29b626a55f09a65532538a6184d4'
        },
        '8.10' :
        {
            'series_version' : '8.10',
            'kernel' : '2.6.27',
            'name' : 'intrepid',
            'supported' : False,
            'packages' : []
        },
        '8.04' :
        {
            'series_version' : '8.04',
            'kernel' : '2.6.24',
            'name' : 'hardy',
            'supported' : False,
            'packages' :
            [
                'linux',
                'linux-meta',
                'linux-backports-modules-2.6.24',
                'linux-ubuntu-modules-2.6.24',
                'linux-restricted-modules-2.6.24'
            ],
            'dependent-packages' :
            {
                'linux' : {
                    'meta' : 'linux-meta',
                    'lbm' : 'linux-backports-modules-2.6.24',
                    'lrm' : 'linux-restricted-modules-2.6.24',
                    'lum' : 'linux-ubuntu-modules-2.6.24'
                }
            },
            'sha1' : 'ccccdc4759fd780a028000a1b7b15dbd9c60363b',
            'md5' : 'e4aad2f8c445505cbbfa92864f5941ab'
        },
        '7.10' :
        {
            'series_version' : '7.10',
            'kernel' : '2.6.22',
            'name' : 'gutsy',
            'supported' : False,
            'packages' : []
        },
        '7.04' :
        {
            'series_version' : '7.04',
            'kernel' : '2.6.20',
            'name' : 'feisty',
            'supported' : False,
            'packages' : []
        },
        '6.06' :
        {
            'series_version' : '6.06',
            'kernel' : '2.6.15',
            'name' : 'dapper',
            'supported' : False,
            'packages' :
            [
                'linux-source-2.6.15',
                'linux-backports-modules-2.6.15',
                'linux-restricted-modules-2.6.15'
            ]
        },
    }

    index_by_kernel_version = {
        '4.3.0'    : db['16.04'],
        '4.2.0'    : db['15.10'],
        '4.0.0'    : db['15.10'],
        '3.19.0'   : db['15.04'],
        '3.16.0'   : db['14.10'],
        '3.13.0'   : db['14.04'],
        '3.11.0'   : db['13.10'],
        '3.8.0'    : db['13.04'],
        '3.5.0'    : db['12.10'],
        '3.2.0'    : db['12.04'],
        '3.0.0'    : db['11.10'],
        '2.6.38'   : db['11.04'],
        '2.6.35'   : db['10.10'],
        '2.6.32'   : db['10.04'],
        '2.6.31'   : db['9.10'],
        '2.6.28'   : db['9.04'],
        '2.6.27'   : db['8.10'],
        '2.6.24'   : db['8.04'],
        '2.6.22'   : db['7.10'],
        '2.6.20'   : db['7.04'],
        '2.6.15'   : db['6.06'],
    }

    index_by_series_name = {
        'xenial'   : db['16.04'],
        'wily'     : db['15.10'],
        'vivid'    : db['15.04'],
        'utopic'   : db['14.10'],
        'trusty'   : db['14.04'],
        'saucy'    : db['13.10'],
        'raring'   : db['13.04'],
        'quantal'  : db['12.10'],
        'precise'  : db['12.04'],
        'oneiric'  : db['11.10'],
        'natty'    : db['11.04'],
        'maverick' : db['10.10'],
        'lucid'    : db['10.04'],
        'karmic'   : db['9.10'],
        'jaunty'   : db['9.04'],
        'intrepid' : db['8.10'],
        'hardy'    : db['8.04'],
        'gutsy'    : db['7.10'],
        'feisty'   : db['7.04'],
        'dapper'   : db['6.06'],
    }

    kernel_source_packages = [
        'linux',
        'linux-raspi2',
        'linux-meta-raspi2',
        'linux-ti-omap4', # maverick, natty
        'linux-armadaxp', # precise, quantal
        'linux-exynos5',
        'linux-keystone',
        'linux-ec2',
        'linux-meta',
        'linux-meta-ec2',
        'linux-meta-ti-omap4', # maverick, natty
        'linux-meta-armadaxp', # precise, quantal
        'linux-ports-meta',
        'linux-source-2.6.15',

        'linux-backports-modules-2.6.15',
        'linux-backports-modules-2.6.24',
        'linux-backports-modules-2.6.31',
        'linux-backports-modules-2.6.32',
        'linux-backports-modules-2.6.35',
        'linux-backports-modules-2.6.38',
        'linux-backports-modules-3.0.0',
        'linux-backports-modules-3.2.0',

        'linux-restricted-modules-2.6.15',
        'linux-restricted-modules-2.6.24',

        'linux-ubuntu-modules-2.6.24',

        #'linux-lts-backport-maverick',
        #'linux-lts-backport-natty',
        #'linux-lts-backport-oneiric',
        #'linux-lts-quantal',
        #'linux-meta-lts-backport-maverick',
        #'linux-meta-lts-backport-natty',
        #'linux-meta-lts-backport-oneiric',
        #'linux-meta-lts-quantal',
    ]

    # lookup
    #
    def lookup(self, key):
        """
        Using the given key, find the matching record in the db and return that record.
        Note, the key argument can be a series-name, series-version or a kernel-version.
        """
        if key in Ubuntu.db:
            record = Ubuntu.db[key]
        elif key in Ubuntu.index_by_kernel_version:
            record = Ubuntu.index_by_kernel_version[key]
        elif key in Ubuntu.index_by_series_name:
            record = Ubuntu.index_by_series_name[key]
        else:
            raise KeyError(key)

        return record

    # is_development_series
    #
    def is_development_series(self, series):
        '''
        Returns True if the series passed in is the current series under development.
        '''
        try:
            retval = self.index_by_series_name[series]['development']
        except KeyError:
            retval = False
        return retval

    # is_supported_series
    #
    def is_supported_series(self, series):
        """
        Lookup the given series and return whether it is still supported or not. Note, since
        this uses the 'lookup' method, the series argument can be a series-name, series-version
        or a kernel-version.
        """
        retval = False

        rec = self.lookup(series)
        retval = rec['supported']

        return retval

    # development_series
    #
    @property
    def development_series(self):
        """
        Assume there is one, and only one, development series.
        """
        retval = None
        for series in self.db:
            try:
                if self.db[series]['development']:
                    retval = self.db[series]['name']
                    break
            except KeyError:
                    pass

        return retval

    # supported_series
    #
    @property
    def supported_series(self):
        """
        A list of all the currently supported series names.
        """
        retval = []
        for series in self.db:
            if self.db[series]['supported']:
                retval.append(self.db[series]['name'])

        return retval

    # active_packages
    #
    @property
    def active_packages(self):
        """
        A list of all the packages for all the supported series.
        """
        retval = []
        for series in self.db:
            if self.db[series]['supported']:
                for pkg in self.db[series]['packages']:
                    if pkg not in retval:
                        retval.append(pkg)

        return retval

    # series where that package-version is found
    #
    def series_name(self, package, version):
        """
        Return the series name where that package-version is found
        """
        Dbg.enter('series_name')
        retval = None

        if package.startswith('linux-lts-'):
            Dbg.verbose('package condition 2\n')
            for entry in self.db.itervalues():
                # starting with trusty, the lts packages now include the series
                # version instead of the series name, e.g: 3.16.0-23.31~14.04.2
                # instead of 3.16.0-23.31~trusty1
                expected = '.*~(%s\.\d+|%s\d+)' % (entry['series_version'], entry['name'])
                if re.match(expected, version):
                    retval = entry['name']
        else:
            Dbg.verbose('package condition 1\n')
            for entry in self.db.itervalues():
                if version.startswith(entry['kernel']):
                    retval = entry['name']

        Dbg.leave('series_name (%s)' % retval)
        return retval

if __name__ == '__main__':
    ubuntu = Ubuntu()
    db = ubuntu.db

    #for record in db:
    #    print db[record]

    print(ubuntu.lookup('2.6.32'))
    print(ubuntu.lookup('lucid'))
    print(ubuntu.lookup('10.04'))

# vi:set ts=4 sw=4 expandtab:
