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
                'build-essential', 'libcap2-bin', 'gcc-multilib', 'gdb', 'gawk', 'execstack', 'exim4', 'libcap-dev', 'gdb',
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
                'ruby1.8', 'attr', 'apport', 'libpam-apparmor', 'libgtk2.0-dev', 'pyflakes', 'apparmor-profiles', 'quilt',
                ],
            'raring' : [
                'python3-libapparmor', 'python-libapparmor', 'python3', 'python3-all-dev',
                ],
            'quantal' : [
                'python3-libapparmor', 'python-libapparmor', 'python3', 'python3-all-dev',
                ],
            'precise' : [
                'python-libapparmor', 'python3', 'python3-all-dev',
                ],
            'oneiric' : [
                'python-libapparmor', 'python3', 'python3-all-dev',
                ],
            },
        },

    'ubuntu_ecryptfs' : {
        'packages' : {
            'common' : [
                'libglib2.0-dev', 'intltool', 'keyutils', 'libkeyutils-dev', 'libpam0g-dev', 'libnss3-dev', 'libtool', 'acl', 'xfsprogs', 'btrfs-tools', 'gdb',
                ],
            },
        },

    'ubuntu_leap_seconds' : {
        'packages' : {
            'common' : [],
            },
        },

    'xfstests' : {
        'packages' : {
            'common' : [
                'uuid-dev', 'xfslibs-dev', 'xfsdump', 'autoconf', 'kpartx', 'libtool', 'python-xattr', 'libacl1-dev', 'libaio-dev', 'quota', 'bc', 'libdm0-dev', 'btrfs-tools', 'attr', 'gdb',
                ],
            },
        'command' : 'sudo mkdir -p /media/xfsmount ; sudo adduser --quiet --disabled-password -gecos "XFS test user,,," fsgqa || true',
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
            'common' : ['flex'],
            },
        },

    'stress' : {
        'packages' : {
            'common' : [],
            },
        },

    'power_consumption' : {
        'packages' : {
           'common' : ['stress'],
            },
        'atargs' : {'METER_ADDR':'10.97.8.2', 'METER_PORT':'3490', 'METER_TAGPORT':'9999'},
        },

    'wakeup_events' : {
        'packages' : {
            'common' : [],
            },
        },

}

# Test Collections may be defined, and will run the list of autotest tests in them
#
TestCollections = {
    'benchmarks' : ['dbench', 'compilebench', 'bonnie'],

    # This is the set of tests that will run if no KERNEL_TEST_LIST variable is set.
    # (QA runs this set)
    #
    'default' : ['ubuntu_ecryptfs', 'ubuntu_qrt_kernel_hardening', 'ubuntu_qrt_kernel_panic', 'ubuntu_qrt_kernel_security', 'ubuntu_qrt_kernel_aslr_collisions', 'ubuntu_qrt_apparmor'],

    # This is the set of tests that the kernel team runs. This should
    # be a superset of the 'default' tests that QA runs.
    #
    'kernel' : ['iperf', 'ubuntu_leap_seconds', 'stress', 'ltp', 'xfstests'],

    # This is the set of tests for measuring power consumption.
    'power' : ['power_consumption'],

    # This is the set of tests for measuring power consumption.
    'wakeup_events' : ['wakeup_events'],

}

# vi:set ts=4 sw=4 expandtab syntax=python:
