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
            'server distro decoration' : '',
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
                "ip" : "10.97.0.11",
                "port" : "Fozzie_PS1"
            },
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
            },
            {
                "ip" : "10.97.0.12",
                "port" : "Rizzo_PS2"
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
    },
    "animal" : {
        "orchestra server" : "magners-orchestra",
        "jenkins server" : "kernel-jenkins",
        "mac address" : "00:1e:67:65:89:f9",
        "cdu" : [
            {
                "ip" : "10.97.0.20",
                "port" : "animal"
            }
        ]
    },
    #"zoot" : {
    #    "orchestra server" : "magners-orchestra",
    #    "jenkins server" : "kernel-jenkins",
    #    "mac address" : "00:1e:67:65:89:f9",
    #    "cdu" : [
    #        {
    #            "ip" : "10.97.0.20",
    #            "port" : "zoot"
    #        }
    #    ]
    #},
    #"pops" : {
    #    "orchestra server" : "magners-orchestra",
    #    "jenkins server" : "kernel-jenkins",
    #    "mac address" : "00:1e:67:65:86:aa",
    #    "cdu" : [
    #        {
    #            "ip" : "10.97.0.20",
    #            "port" : "pops"
    #        }
    #    ]
    #}
}
# vi:set ts=4 sw=4 expandtab:
