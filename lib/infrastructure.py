#!/usr/bin/env python
#

Orchestra = {
    'arch' : {
        'amd64' : 'x86_64',
        'i386' : 'i386'
    },
    'series' : {
        'lucid' : {
            'preseed' : 'secondary',
            'server distro decoration' : '',
        },
        'natty' : {
            'preseed' : 'natty',
            'server distro decoration' : '',
        },
        'oneiric' : {
            'preseed' : 'primary',
            'server distro decoration' : '-server',
        },
        'precise' : {
            'preseed' : 'primary',
            'server distro decoration' : '-server',
        },
        'quantal' : {
            'preseed' : 'primary',
            'server distro decoration' : '-server',
        },
        'raring' : {
            'preseed' : 'primary',
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
        'natty' : {
            'series' : 'lucid',
            'package' : 'linux-image-generic-lts-backport-natty',
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
        },
}

# Information about the systems that the kernel team reprovisions and
# performs testing on.
#
LabHW = {
    "gonzo" : {
        "orchestra server" : "magners-orchestra",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "08:9e:01:3c:c9:60",
        "cdu" : [
            {
                "ip" : "10.97.0.12",
                "port" : "Gonzo"
            }
        ]
    },
    "fozzie" : {
        "orchestra server" : "magners-orchestra",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "90:b1:1c:10:6b:03",
        "cdu" : [
            {
                "ip" : "10.97.0.12",
                "port" : "Fozzie_PS2"
            }
        ]
    },
    "scooter" : {
        "orchestra server" : "magners-orchestra",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "d4:ae:52:a3:6a:22",
        "cdu" : [
            {
                "ip" : "10.97.0.12",
                "port" : "Scooter"
            }
        ]
    },
    "rizzo" : {
        "orchestra server" : "magners-orchestra",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "d4:ae:52:a3:6a:22",
        "cdu" : [
            {
                "ip" : "10.97.0.11",
                "port" : "Rizzo_PS1"
            }
        ]
    },
    "waldorf" : {
        "orchestra server" : "magners-orchestra",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "00:1e:67:34:b8:5c",
        "cdu" : [
            {
                "ip" : "10.97.0.11",
                "port" : "Waldorf"
            }
        ]
    },
    "statler" : {
        "orchestra server" : "magners-orchestra",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "60:eb:69:21:2c:6d",
        "cdu" : [
            {
                "ip" : "10.97.0.11",
                "port" : "Statler_PS1"
            },
            {
                "ip" : "10.97.0.12",
                "port" : "Statler_PS2"
            }
        ]
    }
}
# vi:set ts=4 sw=4 expandtab:
