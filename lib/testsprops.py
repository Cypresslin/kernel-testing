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
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'git', 'libkeyutils-dev',
                ],
            },
        'series-blacklist' : [
            ],
        'arch-blacklist' : [
            ],
        },

    'ubuntu_seccomp' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'git'
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy',
            ],
        'arch-blacklist' : [
            'i386', 'i686', 'athlon', 'arm64', 'ppc64el',
            ],
        },

    'ubuntu_stress_ng' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'git', 'libattr1-dev', 'libkeyutils-dev',
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy',
            ],
        },

    'ubuntu_zfs' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'xfsprogs', 'git', 'acl', 'libattr1-dev',
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'vivid', 'utopic',
            ],
        },

    'ubuntu_zfs_fstest' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'xfsprogs', 'git', 'acl', 'libattr1-dev',
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'vivid', 'utopic',
            ],
        },

    'ubuntu_zfs_xfs_generic' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'xfsprogs', 'git', 'acl', 'libattr1-dev',
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'vivid', 'utopic',
            ],
        },

    'ubuntu_zfs_stress' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'xfsprogs', 'git', 'acl', 'libattr1-dev', 'libkeyutils-dev',
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'vivid', 'utopic',
            ],
        },

    'ubuntu_btrfs_kernel_fixes' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'xfsprogs', 'btrfs-tools', 'git', 'acl', 'libattr1-dev',
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy', 'trusty',
            ],
        'atargs' : {}, # this gets filled in later, it's a hack
        },

    'ubuntu_stress_btrfs' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'xfsprogs', 'btrfs-tools', 'git', 'acl', 'libattr1-dev', 'libkeyutils-dev',
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy',
            ],
        'scratch' : True,
        'atargs' : {}, # this gets filled in later, it's a hack
        },

    'ubuntu_stress_btrfs_cmd' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'xfsprogs', 'btrfs-tools', 'git', 'acl', 'libattr1-dev',
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy',
            ],
        'scratch' : True,
        'atargs' : {}, # this gets filled in later, it's a hack
        },

    'ubuntu_futex' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'git'
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy',
            ],
        },

    'ubuntu_unionmount_overlayfs_suite' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'git'
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy', 'trusty', 'utopic',
            ],
        },

    'ubuntu_kvm_unit_tests' : {
        'packages' : {
            'common' : [
                'qemu-kvm', 'gdb',
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy',
            ],
        'arch-blacklist' : [
            'ppc64le', 'aarch64',
            ],
        },

    'ubuntu_lxc' : {
        'packages' : {
            'common' : [
                'lxc-tests', 'gdb',
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'quantal', 'saucy',
            ],
        },

    'ubuntu_WiFi_SimpleConnection' : {
        'packages' : {
            'common' : [
                ],
            },
        },

    'network_WiFiCaps' : {
        'packages' : {
            'common' : [
                'iw', 'pkg-config', 'libnl-dev', 'gdb',
                ],
            },
        },

    'ubuntu_qrt_kernel' : {
        'packages' : {
            'common' : [
                'build-essential', 'libcap2-bin', 'gcc-multilib', 'gdb', 'gawk', 'execstack', 'exim4', 'libcap-dev', 'gdb',
                ],
            },
        },

    'ubuntu_qrt_kernel_aslr_collisions' : {
        'packages' : {
            'common' : [
                'build-essential', 'libcap2-bin', 'gcc-multilib', 'gdb', 'gawk', 'execstack', 'exim4', 'libcap-dev', 'gdb',
                ],
            },
        },

    'ubuntu_qrt_kernel_hardening' : {
        'packages' : {
            'common' : [
                'build-essential', 'libcap2-bin', 'gcc-multilib', 'gdb', 'gawk', 'execstack', 'exim4', 'libcap-dev', 'gdb',
                ],
            },
        },

    'ubuntu_qrt_kernel_panic' : {
        'packages' : {
            'common' : [
                'build-essential', 'libcap2-bin', 'gcc-multilib', 'gdb', 'gawk', 'execstack', 'exim4', 'libcap-dev', 'gdb', 'libkeyutils-dev',
                ],
            },
        },

    'ubuntu_qrt_kernel_security' : {
        'packages' : {
            'common' : [
                'build-essential', 'libcap2-bin', 'gcc-multilib', 'gdb', 'gawk', 'execstack', 'exim4', 'libcap-dev', 'gdb',
                ],
            },
        },

    'ubuntu_qrt_apparmor' : {
        'packages' : {
            'common' : [
                'build-essential', 'libcap2-bin', 'gcc-multilib', 'gdb', 'gawk', 'execstack', 'exim4', 'libcap-dev', 'gdb',
                'python-pexpect', 'apparmor', 'apparmor-utils', 'netcat', 'sudo', 'build-essential', 'libapparmor-dev',
                'attr', 'apport', 'libpam-apparmor', 'libgtk2.0-dev', 'pyflakes', 'apparmor-profiles', 'quilt', 'libdbus-1-dev'
                ],
            'xenial' : [
                'python3-libapparmor', 'python-libapparmor', 'python3', 'python3-all-dev', 'ruby', 'apparmor-easyprof',
                ],
            'wily' : [
                'python3-libapparmor', 'python-libapparmor', 'python3', 'python3-all-dev', 'ruby', 'apparmor-easyprof',
                ],
            'vivid' : [
                'python3-libapparmor', 'python-libapparmor', 'python3', 'python3-all-dev', 'ruby', 'apparmor-easyprof',
                ],
            'utopic' : [
                'python3-libapparmor', 'python-libapparmor', 'python3', 'python3-all-dev', 'ruby', 'apparmor-easyprof',
                ],
            'trusty' : [
                'python3-libapparmor', 'python-libapparmor', 'python3', 'python3-all-dev', 'ruby', 'apparmor-easyprof',
                ],
            'saucy' : [
                'python3-libapparmor', 'python-libapparmor', 'python3', 'python3-all-dev', 'ruby1.8', 'apparmor-easyprof',
                ],
            'raring' : [
                'python3-libapparmor', 'python-libapparmor', 'python3', 'python3-all-dev', 'ruby1.8', 'apparmor-easyprof',
                ],
            'quantal' : [
                'python3-libapparmor', 'python-libapparmor', 'python3', 'python3-all-dev', 'ruby1.8',
                ],
            'precise' : [
                'python-libapparmor', 'python3', 'python3-all-dev', 'ruby1.8',
                ],
            },
        },

    'ubuntu_ecryptfs' : {
        'packages' : {
            'common' : [
                'libglib2.0-dev', 'intltool', 'keyutils', 'libkeyutils-dev', 'libpam0g-dev', 'libnss3-dev', 'libtool', 'acl', 'xfsprogs', 'btrfs-tools', 'gdb', 'libattr1-dev'
                ],
            },
        },

    'ubuntu_leap_seconds' : {
        'packages' : {
            'common' : ['gdb',],
            },
        },

    'ubuntu_32_on_64' : {
        'packages' : {
            'common' : ['gdb', 'gcc-multilib'],
            },
        'arch-blacklist' : [
            'i386', 'i686', 'athlon', 'ppc64el', 'arm64', 'ppc64le', 'aarch64',
            ],
        },

    'xfstests' : {
        'packages' : {
            'common' : [
                'build-essential', 'uuid-dev', 'xfslibs-dev', 'xfsdump', 'autoconf', 'kpartx', 'libtool', 'python-xattr', 'libacl1-dev', 'libaio-dev', 'quota', 'bc', 'btrfs-tools', 'attr', 'gdb',
                ],
            'xenial' : [
                'libtool-bin'
                ],
            'wily' : [
                'libtool-bin', 'libdm0-dev',
                ],
            'vivid' : [
                'libtool-bin', 'libdm0-dev',
                ],
            },
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
        'packages' : {
            'common' : [
                'gdb', 'flex', 'build-essential', 'gcc-multilib', 'git', 'automake'
                ],
            },
        },

    'stress' : {
        'packages' : {
            'common' : ['gdb'],
            },
        },

    'dbench' : {
        'packages' : {
            'common' : [],
            },
        },

    'power_consumption' : {
        'packages' : {
           'common' : ['gdb', 'stress'],
            },
        'atargs' : {'METER_ADDR':'10.97.4.49', 'METER_PORT':'3490', 'METER_TAGPORT':'9999'},
        },

    'wakeup_events' : {
        'packages' : {
            'common' : [],
            },
        },

    'ubuntu_cts_kernel' : {
        'packages' : {
            'common' : ['gdb', 'coreutils', 'apparmor', 'linux-tools-`uname -r`', 'iproute2', 'openvswitch-switch'],
            },
        'series-blacklist': [
            'lucid', 'precise', 'quantal', 'saucy',
            ],
        },

    'ubuntu_kernel_selftests' : {
        'packages' : {
            'common' : ['build-essential', 'gcc-multilib', 'gdb', 'git']
            },
        'series-blacklist': [
            'lucid', 'precise', 'quantal', 'saucy', 'trusty', 'xenial',
            ],
        'arch-blacklist' : [
            'armv7l',
            ],
        },

    'ubuntu_stress_smoke_test' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'git', 'libattr1-dev', 'libkeyutils-dev',
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'trusty', 'utopic', 'vivid', 'wily',
            ],
        },

    'ubuntu_aufs_smoke_test' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'git', 'libattr1-dev', 'libkeyutils-dev',
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'trusty', 'utopic', 'vivid', 'wily',
            ],
        },

    'ubuntu_fan_smoke_test' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'git',
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'trusty', 'utopic', 'vivid', 'wily',
            ],
        },

    'ubuntu_zfs_smoke_test' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'xfsprogs', 'git', 'acl', 'libattr1-dev',
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'trusty', 'utopic', 'vivid', 'wily',
            ],
        },

    'ubuntu_squashfs_smoke_test' : {
        'packages' : {
            'common' : [
                'build-essential', 'gcc-multilib', 'gdb', 'xfsprogs', 'git', 'acl', 'libattr1-dev',
                ],
            },
        'series-blacklist' : [
            'lucid', 'precise', 'trusty', 'utopic', 'vivid', 'wily',
            ],
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
             'xfstests',
             'ubuntu_cts_kernel',
             'ubuntu_kernel_selftests',
             'ubuntu_unionmount_overlayfs_suite',
        ],

    'lkp-3' : [
             'ubuntu_ecryptfs',
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

}

# A list of the tests that is used to create test jobs when the mail handler
# is processing SRU email.
#
SRU_TestsList = [
    'sru-1',
    'sru-2',
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
]

# vi:set ts=4 sw=4 expandtab syntax=python:
