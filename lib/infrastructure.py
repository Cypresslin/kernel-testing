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
        }
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
}

# Information about the systems that the kernel team reprovisions and
# performs testing on.
#
LabHW = {
    "gonzo" : {
        "orchestra server" : "jiufeng",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "08:9e:01:3c:c9:60",
        "cdu" : [
            {
                "ip" : "10.98.0.41",
                "port" : "Gonzo"
            }
        ]
    },
    "fozzie" : {
        "orchestra server" : "jiufeng",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "90:b1:1c:10:6b:03",
        "cdu" : [
            {
                "ip" : "10.98.0.43",
                "port" : "Fozzie_PS2"
            }
        ]
    },
    "scooter" : {
        "orchestra server" : "jiufeng",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "d4:ae:52:a3:6a:22",
        "cdu" : [
            {
                "ip" : "10.98.0.41",
                "port" : "Scooter"
            }
        ]
    },
    "rizzo" : {
        "orchestra server" : "jiufeng",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "d4:ae:52:7c:c6:2a",
        "cdu" : [
            {
                "ip" : "10.98.0.41",
                "port" : "Rizzo_PS1"
            },
            {
                "ip" : "10.98.0.43",
                "port" : "Rizzo_PS1"
            }
        ]
    },
    "waldorf" : {
        "orchestra server" : "jiufeng",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "00:1e:67:34:b8:5c",
        "cdu" : [
            {
                "ip" : "10.98.0.43",
                "port" : "Waldorf"
            }
        ]
    },
    "statler" : {
        "orchestra server" : "jiufeng",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "60:eb:69:21:2c:6d",
        "cdu" : [
            {
                "ip" : "10.98.0.41",
                "port" : "Statler_PS1"
            }
        ]
    },
    "zoot" : {
        "orchestra server" : "jiufeng",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "a0:36:9f:0e:ed:08",
        "cdu" : [
            {
                "ip" : "10.98.0.43",
                "port" : "Zoot_PS2"
            }
        ]
    },
    "floyd" : {
        "orchestra server" : "jiufeng",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "a0:36:9f:14:65:38",
        "cdu" : [
            {
                "ip" : "10.98.0.43",
                "port" : "Floyd_PS2"
            }
        ]
    },
    "janice" : {
        "orchestra server" : "jiufeng",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "a0:36:9f:14:65:70",
        "cdu" : [
            {
                "ip" : "10.98.0.30",
                "port" : "Janice_PS1"
            }
        ]
    },
    "pops" : {
        "orchestra server" : "jiufeng",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "a0:36:9f:0f:1c:cc",
        "cdu" : [
            {
                "ip" : "10.98.0.43",
                "port" : "Pops_PS2"
            }
        ]
    },
    "beaker" : {
        "orchestra server" : "jiufeng",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "00:00:1a:1a:c4:97",
        "cdu" : [
            {
                "ip" : "10.98.0.43",
                "port" : "Beaker_PS2"
            }
        ]
    }
}
# vi:set ts=4 sw=4 expandtab:
