#!/usr/bin/env python
#

Orchestra = {
    'arch' : {
        'amd64' : 'x86_64',
        'i386' : 'i386'
    },
    'series' : {
        'lucid' : {
            'preseed' : 'secondary-no-slave',
            'server distro decoration' : '',
        },
        'oneiric' : {
            'preseed' : 'primary-no-slave',
            'server distro decoration' : '-server',
        },
        'precise' : {
            'preseed' : 'primary-no-slave',
            'server distro decoration' : '-server',
        },
        'quantal' : {
            'preseed' : 'primary-no-slave',
            'server distro decoration' : '-server',
        },
        'raring' : {
            'preseed' : 'primary-no-slave',
            'server distro decoration' : '-server',
        },
        'saucy' : {
            'preseed' : 'primary-no-slave',
            'server distro decoration' : '-server',
        },
        'trusty' : {
            'preseed' : 'primary-no-slave',
            'server distro decoration' : '-server',
        },
    }
}

# The relationships of a hardware enablement (hwe) kernel for a
# series to the LTS series it 'enables'.
#
HWE = {
        'lucid' : {
            'series' : None,
        },
        'oneiric' : {
            'series' : 'lucid',
            'package' : 'linux-image-generic-lts-backport-oneiric',
        },
        'precise' : {
            'series' : None,
        },
        'quantal' : {
            'series' : 'precise',
            'package' : 'linux-generic-lts-quantal',
        },
        'raring' : {
            'series' : 'precise',
            'package' : 'linux-generic-lts-raring',
            'ppa' : True,
        },
        'saucy' : {
            'series' : 'precise',
            'package' : 'linux-generic-lts-saucy',
            'ppa' : True,
        },
}

# Information about the systems that the kernel team reprovisions and
# performs testing on.
#
LabHW = {
    "gonzo" : {
        "orchestra server" : "cobbler",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "08:9e:01:3c:c9:60",
        "cdu" : [
            {
                "ip" : "10.98.4.33",
                "port" : "gonzo"
            }
        ]
    },
    "fozzie" : {
        "orchestra server" : "cobbler",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "90:b1:1c:10:6b:03",
        "cdu" : [
            {
                "ip" : "10.98.4.32",
                "port" : "fozzie-ps1"
            },
            {
                "ip" : "10.98.4.33",
                "port" : "fozzie-ps2"
            }
        ]
    },
    "rizzo" : {
        "orchestra server" : "cobbler",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "d4:ae:52:7c:c6:2a",
        "cdu" : [
            {
                "ip" : "10.98.4.32",
                "port" : "rizzo-ps1"
            },
            {
                "ip" : "10.98.4.33",
                "port" : "rizzo-ps2"
            }
        ]
    },
    "waldorf" : {
        "orchestra server" : "cobbler",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "00:1e:67:34:b8:5c",
        "cdu" : [
            {
                "ip" : "10.98.4.30",
                "port" : "waldorf"
            }
        ]
    },
    "statler" : {
        "orchestra server" : "cobbler",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "60:eb:69:21:2c:6d",
        "cdu" : [
            {
                "ip" : "10.98.4.30",
                "port" : "statler-ps1"
            },
            {
                "ip" : "10.98.4.31",
                "port" : "statler-ps2"
            }
        ]
    },
    "zoot" : {
        "orchestra server" : "cobbler",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "a0:36:9f:0e:ed:08",
        "cdu" : [
            {
                "ip" : "10.98.4.30",
                "port" : "zoot-ps1"
            },
            {
                "ip" : "10.98.4.31",
                "port" : "zoot-ps2"
            }
        ]
    },
    "floyd" : {
        "orchestra server" : "cobbler",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "a0:36:9f:14:65:38",
        "cdu" : [
            {
                "ip" : "10.98.4.32",
                "port" : "floyd-ps1"
            },
            {
                "ip" : "10.98.4.33",
                "port" : "floyd-ps2"
            }
        ]
    },
    "janice" : {
        "orchestra server" : "cobbler",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "a0:36:9f:14:65:70",
        "cdu" : [
            {
                "ip" : "10.98.4.32",
                "port" : "janice-ps1"
            },
            {
                "ip" : "10.98.4.33",
                "port" : "janice-ps2"
            }
        ]
    },
    "pops" : {
        "orchestra server" : "cobbler",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "a0:36:9f:0f:1c:cc",
        "cdu" : [
            {
                "ip" : "10.98.4.30",
                "port" : "pops-ps1"
            },
            {
                "ip" : "10.98.4.31",
                "port" : "pops-ps2"
            }
        ]
    },
    "beaker" : {
        "orchestra server" : "cobbler",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "00:00:1a:1a:c4:98",
        "cdu" : [
            {
                "ip" : "10.98.4.30",
                "port" : "beaker"
            }
        ]
    }
}
# vi:set ts=4 sw=4 expandtab:
