# A dictionary of specifics about each autotest test that the kernel team
# cares about.
#
# - The key is the autotest test name
#   - 'dependencies' is a sub-dictionary of lists of depended packages. The
#     key is either an ubuntu series name or 'common'. 'common' indicates
#     that those dependiencies apply to all ubuntu series.
#
#   - 'commands' is a list of commands that must be run prior to running the
#     associated test.
#
#   - 'atargs' is a dictionary of name/value pairs which are passed to the
#     autotest test via the autotest command line.
#
TestProfiles = {

    'connectathon' : {
    },
    'flail' : {
    },
    'synctest' : {
    },
    'signaltest' : {
    },
    'iosched_bugs' : {
    },
    'aiostress' : {
    },
    'aio_dio_bugs' : {
    },
    'ebizzy' : {
    },
    'libhugetlbfs' : {
    },
    'fsx' : {
    },
    'fsstress' : {
    },
    'rtc' : {
    },
    'hwclock' : {
    },
    'isic' : {
    },
    'scrashme' : {
    },

    'virt' : {
        'packages' : {
            'common' : [
                'p7zip-full', 'tcpdump', 'iproute2', 'libvirt-bin', 'virtinst', 'fakeroot', 'attr', 'git', 'iputils-arping',
                'gcc', 'python-support', 'python-dev', 'qemu-kvm', 'cpu-checker', 'policycoreutils', 'python-gst-1.0',
                'python-imaging', 'nfs-kernel-server', 'openvswitch-switch', 'genisoimage', 'python-all-dev', 'gnuplot-nox',
                'gdb', 'tgt', 'numactl', 'python-libguestfs', 'linux-tools-`uname -r`', 'valgrind',
                ],
            },
        'series-blacklist': [
            'lucid', 'precise', 'quantal', 'saucy',
            ],
        },

    'docker' : {
        'packages' : {
            'common' : [
                'docker.io', 'gdb'
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy',
            ],
        },

    'ubuntu_cve_kernel' : {
    },

    'ubuntu_seccomp' : {
        'series-blacklist' : [
            'precise'
        ],
        'arch-blacklist' : [
            'i386', 'i686', 'athlon', 'arm64', 'ppc64el',
        ],
    },

    'ubuntu_zfs' : {
        'series-blacklist' : [
            'lucid', 'precise', 'vivid', 'utopic',
        ],
    },

    'ubuntu_zfs_fstest' : {
        'series-blacklist' : [
            'lucid', 'precise', 'vivid', 'utopic',
        ],
    },

    'ubuntu_zfs_xfs_generic' : {
        'series-blacklist' : [
            'lucid', 'precise', 'vivid', 'utopic',
        ],
    },

    'ubuntu_zfs_stress' : {
        'series-blacklist' : [
            'lucid', 'precise', 'vivid', 'utopic',
        ],
    },

    'ubuntu_btrfs_kernel_fixes' : {
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy', 'trusty',
        ],
        'atargs' : {}, # this gets filled in later, it's a hack
    },

    'ubuntu_stress_btrfs' : {
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy',
        ],
        'scratch' : True,
        'atargs' : {}, # this gets filled in later, it's a hack
    },

    'ubuntu_stress_btrfs_cmd' : {
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy',
        ],
        'scratch' : True,
        'atargs' : {}, # this gets filled in later, it's a hack
    },

    'ubuntu_futex' : {
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy',
        ],
    },

    'ubuntu_unionmount_overlayfs_suite' : {
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy', 'trusty', 'utopic',
        ],
    },

    'ubuntu_kvm_unit_tests' : {
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy',
        ],
        'arch-blacklist' : [
            'ppc64le', 'aarch64',
        ],
    },

    'ubuntu_lxc' : {
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy',
        ],
    },

    'ubuntu_WiFi_SimpleConnection' : {
    },

    'network_WiFiCaps' : {
    },

    'ubuntu_qrt_kernel' : {
    },

    'ubuntu_qrt_kernel_aslr_collisions' : {
    },

    'ubuntu_qrt_kernel_hardening' : {
    },

    'ubuntu_qrt_kernel_panic' : {
    },

    'ubuntu_qrt_kernel_security' : {
    },

    'ubuntu_qrt_apparmor' : {
    },

    'ubuntu_ecryptfs' : {
    },

    'ubuntu_leap_seconds' : {
    },

    'ubuntu_32_on_64' : {
        'arch-blacklist' : [
            'i386', 'i686', 'athlon', 'ppc64el', 'arm64', 'ppc64le', 'aarch64',
        ],
    },

    'xfstests' : {
        'series-blacklist': [
            'lucid', 'precise', 'quantal', 'saucy', 'trusty',
        ],
        'command' : 'sudo mkdir -p /media/xfsmount ; sudo adduser --quiet --disabled-password -gecos "XFS test user,,," fsgqa || true',
        'atargs' : {}, # this gets filled in later, it's a hack
        'scratch' : True,
    },

    'ubuntu_fs_fio_perf' : {
        'packages' : {
            'common' : [
                 'build-essential', 'git-core', 'fio', 'libaio-dev', 'xfsdump', 'xfsprogs', 'btrfs-tools', 'gdb',
                ],
            },
        'env' : {('BENCHMARKS', 'true')},
        'atargs' : {}, # this gets filled in later, it's a hack
        'scratch' : True,
        },

    'iozone' : {
        'packages' : {
            'common' : [
                'gnuplot', 'xfsdump', 'xfsprogs', 'btrfs-tools', 'gdb',
                ],
            },
        'command' : 'sudo mkdir -p /media/iozonemount',
        'atargs' : {}, # this gets filled in later, it's a hack
        'scratch' : True,
        },

    'iozone-fsync' : {
        'packages' : {
            'common' : [
                'gnuplot', 'xfsdump', 'xfsprogs', 'btrfs-tools', 'gdb',
                ],
            },
        'command' : 'sudo mkdir -p /media/iozonemount',
        'atargs' : {}, # this gets filled in later, it's a hack
        'scratch' : True,
        },

    'iozone-nolazy' : {
        'packages' : {
            'common' : [
                'gnuplot', 'xfsdump', 'xfsprogs', 'btrfs-tools', 'gdb',
                ],
            },
        'command' : 'sudo mkdir -p /media/iozonemount',
        'atargs' : {}, # this gets filled in later, it's a hack
        'scratch' : True,
        },

    'iozone-ioscheduler-xfs' : {
        'packages' : {
            'common' : [
                'gnuplot', 'xfsdump', 'xfsprogs', 'gdb',
                ],
            },
        'command' : 'sudo mkdir -p /media/iozonemount',
        'atargs' : {}, # this gets filled in later, it's a hack
        'scratch' : True,
        },

    'tiobench' : {
        'packages' : {
            'common' : [
                'gnuplot', 'xfsdump', 'xfsprogs', 'btrfs-tools', 'gdb',
                ],
            },
        'command' : 'sudo mkdir -p /media/testmount',
        'atargs' : {}, # this gets filled in later, it's a hack
        'scratch' : True,
        },

    'iperf' : {
        'packages' : {
            'common' : ['sysstat', 'gdb'],
            },
        },

    'ltp' : {
    },

    'stress' : {
    },

    'dbench' : {
    },

    'power_consumption' : {
        'atargs' : {'METER_ADDR': '10.97.4.49', 'METER_PORT': '3490', 'METER_TAGPORT': '9999'},
    },

    'wakeup_events' : {
    },

    'ubuntu_cts_kernel' : {
        'series-blacklist': [
            'lucid', 'precise', 'quantal', 'saucy',
        ],
    },

    'ubuntu_kernel_selftests' : {
        'series-blacklist': [
            'lucid', 'precise', 'quantal', 'saucy', 'trusty', 'xenial',
        ],
        'arch-blacklist' : [
            'armv7l',
        ],
    },

    'ubuntu_stress_smoke_test' : {
        'series-blacklist' : [
            'lucid', 'precise', 'trusty', 'utopic', 'vivid', 'wily',
        ],
    },

    'ubuntu_aufs_smoke_test' : {
        'series-blacklist' : [
            'lucid', 'precise', 'trusty', 'utopic', 'vivid', 'wily',
        ],
    },

    'ubuntu_fan_smoke_test' : {
        'series-blacklist' : [
            'lucid', 'precise', 'trusty', 'utopic', 'vivid', 'wily',
        ],
    },

    'ubuntu_zfs_smoke_test' : {
        'series-blacklist' : [
            'lucid', 'precise', 'trusty', 'utopic', 'vivid', 'wily',
        ],
    },

    'ubuntu_squashfs_smoke_test' : {
        'series-blacklist' : [
            'lucid', 'precise', 'trusty', 'utopic', 'vivid', 'wily',
        ],
    },

    'ubuntu_load_livepatch_modules' : {
    },
}

# Test Collections may be defined, and will run the list of autotest tests in them
#
TestCollections = {
    # Live Kernel Patching
    #
    'lkp' : [
            'ubuntu_cve_kernel',
        ],

    'lkp-1' : [
        'qrt',
        'ubuntu_lxc',
        'ubuntu_seccomp',
        'ubuntu_kvm_unit_tests',
        'ubuntu_leap_seconds',
        'ubuntu_32_on_64',
    ],

    'lkp-2' : [
        'smoke',
        'ubuntu_cve_kernel',
        'ubuntu_cts_kernel',
        'ubuntu_kernel_selftests',
        'ubuntu_unionmount_overlayfs_suite',
    ],

    'lkp-3' : [
        'connectathon',
        'synctest',
        'signaltest',
        'iosched_bugs',
        'aiostress',
        'aio_dio_bugs',
        'ebizzy',
        'libhugetlbfs',
        'fsx',
        'fsstress',
        'rtc',
        'hwclock',
        'isic',
        'scrashme',
    ],

    'lkp-apparmor' : [
            'ubuntu_qrt_apparmor'
        ],

    'lkp-ecryptfs' : [
             'ubuntu_ecryptfs',
        ],

    'lkp-xfstests' : [
             'xfstests',
        ],


    # CPC
    #
    'cpc' : [
            'ubuntu_qrt_kernel_hardening',
            'ubuntu_qrt_kernel_panic',
            'ubuntu_qrt_kernel_security',
            'ubuntu_qrt_kernel_aslr_collisions',
            'ubuntu_lxc',
            'ubuntu_kernel_selftests',
        ],

    # zsystem specific tests
    #
    'ibm' : [
            'ubuntu_qrt_kernel_hardening',
            'ubuntu_qrt_kernel_panic',
            'ubuntu_qrt_kernel_security',
            'ubuntu_qrt_kernel_aslr_collisions',
            'ubuntu_lxc',
            'ubuntu_qrt_apparmor',
            'ubuntu_kernel_selftests',
            'smoke',
        ],

    # These are the tests that get run as DEP8 tests
    #
    'dep8' : [
            'ubuntu_qrt_kernel_hardening',
            'ubuntu_qrt_kernel_panic',
            'ubuntu_qrt_kernel_security',
            'ubuntu_qrt_kernel_aslr_collisions',
            'ubuntu_qrt_apparmor',
            'ubuntu_kernel_selftests'
        ],

    # The set of tests that Ubuntu Engineering QA run.
    #
    'qrt' : [
            'ubuntu_qrt_kernel_hardening',
            'ubuntu_qrt_kernel_panic',
            'ubuntu_qrt_kernel_security',
            'ubuntu_qrt_kernel_aslr_collisions',
            'ubuntu_qrt_apparmor',
        ],

    'smoke' : [
            'ubuntu_aufs_smoke_test',
            'ubuntu_stress_smoke_test',
            'ubuntu_zfs_smoke_test',
            'ubuntu_fan_smoke_test',
            'ubuntu_squashfs_smoke_test',
        ],

    # This is the set of tests that will run if no KERNEL_TEST_LIST variable is set.
    # (QA runs this set)
    #
    'default' : ['qa'],

    # This is the set of tests that the kernel team runs. This should
    # be a superset of the 'default' tests that QA runs.
    #
    'kernel' : ['qa', 'iperf', 'ubuntu_leap_seconds', 'stress', 'ltp', 'ubuntu_cts_kernel', 'virt', 'ubuntu_kvm_unit_tests'],

    # The set of tests that mainline kernels run
    #
    'mainline' : ['stress'],

    # The set of tests that SRU kernels run
    #
    'sru' : [
        'sru-1',
        'sru-2',
        'sru-3',
    ],

    'sru-1' : [
        'qrt',
        'ubuntu_lxc',
        'ubuntu_seccomp',
        'ubuntu_kvm_unit_tests',
        'ubuntu_leap_seconds',
        'ubuntu_32_on_64',
    ],

    'sru-2' : [
        'smoke',
        'xfstests',
        'ubuntu_cts_kernel',
        'ubuntu_kernel_selftests',
        'ubuntu_unionmount_overlayfs_suite',
    ],

    'sru-3' : [
        'connectathon',
        'synctest',
        'signaltest',
        'iosched_bugs',
        'aiostress',
        'aio_dio_bugs',
        'ebizzy',
        'libhugetlbfs',
        'fsx',
        'fsstress',
        'rtc',
        'hwclock',
        'isic',
        'scrashme',
    ],

}

# A list of the tests that is used to create test jobs when the mail handler
# is processing SRU email.
#
SRU_TestsList = [
    'sru-1',
    'sru-2',
    'sru-3',
    'ubuntu_ecryptfs',
    'ubuntu_btrfs_kernel_fixes',
    'ubuntu_zfs_fstest',
    'ubuntu_zfs_xfs_generic',
    'ubuntu_zfs_stress',
]

LKP_TestsList = [
    'lkp-1',
    'lkp-2',
    'lkp-3',
    'lkp-ecryptfs',
    'lkp-xfstests',
    'ubuntu_load_livepatch_modules',
]

# vi:set ts=4 sw=4 expandtab syntax=python:
