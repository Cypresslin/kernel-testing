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

    'ubuntu_boot' : {
    },
    'xmtest' : {
    },
    'ipv6connect' : {
    },
    'wb_kupdate' : {
    },
    'monotonic_time' : {
    },
    'perfmon' : {
    },
    'posixtest' : {
    },
    'regression' : {
    },
    'rmaptest' : {
    },
    'fs_mark' : {
    },
    'dma_memtest' : {
    },
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
    },

    'docker' : {
    },

    'ubuntu_cve_kernel' : {
    },

    'ubuntu_seccomp' : {
    },

    'ubuntu_zfs' : {
    },

    'ubuntu_zfs_fstest' : {
    },

    'ubuntu_zfs_xfs_generic' : {
    },

    'ubuntu_zfs_stress' : {
    },

    'ubuntu_btrfs_kernel_fixes' : {
        'atargs' : {}, # this gets filled in later, it's a hack
    },

    'ubuntu_stress_btrfs' : {
        'scratch' : True,
        'atargs' : {}, # this gets filled in later, it's a hack
    },

    'ubuntu_stress_btrfs_cmd' : {
        'scratch' : True,
        'atargs' : {}, # this gets filled in later, it's a hack
    },

    'ubuntu_futex' : {
    },

    'ubuntu_unionmount_overlayfs_suite' : {
    },

    'ubuntu_kvm_unit_tests' : {
    },

    'ubuntu_lxc' : {
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
    },

    'xfstests' : {
        'command' : 'sudo mkdir -p /media/xfsmount ; sudo adduser --quiet --disabled-password -gecos "XFS test user,,," fsgqa || true',
        'atargs' : {}, # this gets filled in later, it's a hack
        'scratch' : True,
    },

    'ubuntu_fs_fio_perf' : {
        'env' : {('BENCHMARKS', 'true')},
        'atargs' : {}, # this gets filled in later, it's a hack
        'scratch' : True,
    },

    'iozone' : {
        'command' : 'sudo mkdir -p /media/iozonemount',
        'atargs' : {}, # this gets filled in later, it's a hack
        'scratch' : True,
    },

    'iozone-fsync' : {
        'command' : 'sudo mkdir -p /media/iozonemount',
        'atargs' : {}, # this gets filled in later, it's a hack
        'scratch' : True,
    },

    'iozone-nolazy' : {
        'command' : 'sudo mkdir -p /media/iozonemount',
        'atargs' : {}, # this gets filled in later, it's a hack
        'scratch' : True,
    },

    'iozone-ioscheduler-xfs' : {
        'command' : 'sudo mkdir -p /media/iozonemount',
        'atargs' : {}, # this gets filled in later, it's a hack
        'scratch' : True,
    },

    'tiobench' : {
        'command' : 'sudo mkdir -p /media/testmount',
        'atargs' : {}, # this gets filled in later, it's a hack
        'scratch' : True,
    },

    'iperf' : {
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
    },

    'ubuntu_kernel_selftests' : {
    },

    'ubuntu_stress_smoke_test' : {
    },

    'ubuntu_aufs_smoke_test' : {
    },

    'ubuntu_fan_smoke_test' : {
    },

    'ubuntu_zfs_smoke_test' : {
    },

    'ubuntu_squashfs_smoke_test' : {
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
        'qrt',
        'ubuntu_lxc',
        'ubuntu_kernel_selftests',
        'ubuntu_leap_seconds',
        'smoke',
        'ubuntu_cts_kernel',
        'ubuntu_kernel_selftests',
        'ubuntu_unionmount_overlayfs_suite',
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

    # These are the tests that get run as DEP8 tests
    #
    'dep8' : [
        'ubuntu_qrt_kernel_hardening',
        'ubuntu_qrt_kernel_panic',
        'ubuntu_qrt_kernel_security',
        'ubuntu_qrt_kernel_aslr_collisions',
        'ubuntu_qrt_apparmor',
        'ubuntu_kernel_selftests',
        'ubuntu_aufs_smoke_test',
        'ubuntu_stress_smoke_test',
        'ubuntu_zfs_smoke_test',
        'ubuntu_fan_smoke_test',
        'ubuntu_squashfs_smoke_test',
        'ubuntu_cve_kernel',
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

    'boot' : [
        'ubuntu_boot',
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
        'qrt',
        'sru-1',
        'sru-2',
        'sru-3',
    ],

    'sru-1' : [
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
        'aiostress',
        # 'dma_memtest',
        'ebizzy',
        'fs_mark',
        'fsx',
        'hwclock',
        'iosched_bugs',
        'iperf',
        'ipv6connect',
        'isic',
        'libhugetlbfs',
        'monotonic_time',
        # 'perfmon',
        'posixtest',
        # 'regression',
        'rmaptest',
        'rtc',
        'scrashme',
        'signaltest',
        'synctest',
        'wb_kupdate',
        # 'xmtest',
        'aio_dio_bugs',
    ],

}

# A list of the tests that is used to create test jobs when the mail handler
# is processing SRU email.
#
SRU_TestsList = [
    'qrt',
    'sru-1',
    'sru-2',
    'sru-3',
    'ubuntu_ecryptfs',
    'ubuntu_btrfs_kernel_fixes',
    'ubuntu_zfs_fstest',
    'ubuntu_zfs_xfs_generic',
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
