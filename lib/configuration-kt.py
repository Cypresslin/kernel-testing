#!/usr/bin/env python
#

Configuration = {

    # The Jenkins server section. My Jenkins server is named 'jenkins'.
    #
    "jenkins" : {
        "server_url" : "http://10.245.80.50:8080"
    },

    # I only have one MAAS server and it's named 'maas'.
    #
    "maas" : {
        "server"  : "kernel-maas",   # Hostname of this maas server.
        "profile" : "jenkins",       # When talking to the maas server use this profile.
        "creds"   : "q6TPsE3AJBcVAvMqvB:uj8JPvENCh8hjdubmy:XcRLhdXxjdckFm6DQEpUKGQzMDe7VnXY",
        "user"    : "jenkins",       # When ssh'ing to the maas server use this user
        "type"    : "maas",          # This _is_ a MAAS server (as opposed to a cobbler server)
        "sut_user": "ubuntu",        # The user on the test system after it's been provisioned
    },

    # We have 2 McDivitt chartridges on the hyperscale MAAS server.
    #
    "hyper-maas" : {
        "server"  : "10.229.32.21",  # Hostname of this maas server.
        "profile" : "kernel",        # When talking to the maas server use this profile.
        "creds"   : "AVA8xetuqP8aYvGC7r:9AESbkWkA4f7YTZh6B:zDg39AsXkuamcQcazpCn8mDJsaL2Gnnk",
        "user"    : "kernel",        # When ssh'ing to the maas server use this user
        "type"    : "maas",          # This _is_ a MAAS server (as opposed to a cobbler server)
        "sut_user": "ubuntu",        # The user on the test system after it's been provisioned
    },

    # Test systems section. This is a dictionary of all the test systems that are available
    # to me.
    #
    "systems" : {
        "gonzo" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.227",
                    "username" : "admin",
                    "password" : "insecure"
                },
            ],
            "scratch drive" : "/dev/sdb",
            "role" : ["Filesystem Benchmarking"],
            "locked" : False,
        },
        "rizzo" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.210",
                    "username" : "admin",
                    "password" : "insecure"
                },
            ],
            "scratch drive" : "/dev/sdb",
            "role" : ["debug"],
            "locked" : False,
        },
        "pepe" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.213",
                    "username" : "admin",
                    "password" : "insecure"
                },
            ],
            "role" : ["Personal Testing"],
            "locked" : False,
        },
        "fozzie" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.211",
                    "username" : "admin",
                    "password" : "insecure"
                },
            ],
            "role" : ["sru"],
            "locked" : False,
        },
        "nori" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.212",
                    "username" : "maas",
                    "password" : "SeqjBEPS6FeZaW"
                },
            ],
            "role" : ["arges"],
            "locked" : False,
        },
        "kili" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.209",
                    "username" : "maas",
                    "password" : "kodw6gcl"
                },
            ],
            "role" : ["ubuntu_zfs", "ubuntu_zfs_stress"],
            "locked" : False,
            "scratch drive" : "/dev/sdb",
        },
        "tarf" : {
            "arch" : ['amd64', 'i386'],
            "scratch drive" : "/dev/sdb",
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.222",
                    "username" : "maas",
                    "password" : "mBZpvBcB8sQeo"
                },
            ],
            "role" : ["sru"],
            "locked" : False,
        },
        "alkaid" : {
            "arch" : ['amd64', 'i386'],
            "scratch drive" : "/dev/sdb",
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.219",
                    "username" : "admin",
                    "password" : "insecure"
                },
            ],
            "role" : ["Personal Testing"],
            "locked" : False,
        },
        "phact" : {
            "arch" : ['amd64', 'i386'],
            "scratch drive" : "/dev/sdb",
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.224",
                    "username" : "admin",
                    "password" : "insecure"
                },
            ],
            "role" : [],
            "locked" : False,
            "scratch drive" : "/dev/sdb",
        },
        "rukbah" : {
            "arch" : ['amd64', 'i386'],
            "scratch drive" : "/dev/sdb",
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.206",
                    "username" : "admin",
                    "password" : "insecure"
                },
            ],
            "role" : ['ubuntu_btrfs_kernel_fixes'],
            "locked" : False,
            "scratch drive" : "/dev/sdb",
        },
        "onza" : {
            "arch" : ['amd64', 'i386'],
            "scratch drive" : "/dev/sdb",
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.207",
                    "username" : "admin",
                    "password" : "insecure"
                },
            ],
            "role" : ["sru"],
            "locked" : False,
        },
        "onibi" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.205",
                    "username" : "admin",
                    "password" : "insecure"
                },
            ],
            "role" : ["sru"],
            "locked" : False,
        },
        "rainier" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "192.168.228.91",
                    "username" : "Administrator",
                    "password" : "insecure"
                },
            ],
            "role" : ["sru"],
            "locked" : False,
        },
        "fuller" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "192.168.228.87",
                    "username" : "Administrator",
                    "password" : "insecure"
                },
            ],
            "role" : ["sru"],
            "locked" : False,
        },
        "dagmar" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "192.168.228.88",
                    "username" : "Administrator",
                    "password" : "insecure"
                },
            ],
            "role" : [],
            "locked" : False,
        },
        "cavac" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "192.168.228.83",
                    "username" : "Administrator",
                    "password" : "insecure"
                },
            ],
            "role" : [],
            "locked" : False,
        },
        "bantam" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "192.168.228.89",
                    "username" : "Administrator",
                    "password" : "insecure"
                },
            ],
            "role" : ["sru"],
            "locked" : False,
        },
        "modoc" : {
            "arch" : ['ppc64el'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "192.168.228.20",
                    "username" : "",
                    "password" : "admin"
                },
            ],
            "role" : ["sru"],
            "locked" : False,
            'series-blacklist' : [
                'lucid', 'precise',
                ],
            "scratch drive" : "/dev/sdb",
        },
        "dwalin" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.225",
                    "username" : "maas",
                    "password" : "odkBlXo1HVRYsxS"
                },
            ],
            "role" : ["ubuntu_zfs_fstest", "ubuntu_zfs_xfs_generic"],
            "locked" : False,
            "scratch drive" : "/dev/sdb",
        },

        "etnyre" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "192.168.228.84",
                    "username" : "Administrator",
                    "password" : "insecure"
                },
            ],
            "role" : ["sru"],
            "locked" : False,
        },
        "statler" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.81.158",
                    "username" : "maas",
                    "password" : "j23x8zWbrPT"
                },
            ],
            "role" : [],
            "locked" : False,
            "scratch drive" : "",
        },
        "fili" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.98.5.226",
                    "username" : "maas",
                    "password" : "gEktYeGpC"
                },
            ],
            "role" : [],
            "locked" : False,
        },

        # ----------------

        "gloin" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "cdu",
                    "address" : "10.98.4.30",
                    "port" : "gloin_ps1",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                },
                {
                    "type" : "cdu",
                    "address" : "10.98.4.31",
                    "port" : "gloin_ps2",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                }
            ],
            "role" : [],
            "locked" : True,                      # This is used as a kernel-team build system
        },
        "haase" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.81.143",
                    "username" : "root",
                    "password" : "insecure"
                },
            ],
            "role" : [],
            "locked" : False,
        },
        "balboa" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.81.142",
                    "username" : "root",
                    "password" : "insecure"
                },
            ],
            "role" : [],
            "locked" : False,
        },
        "sayers" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.81.144",
                    "username" : "root",
                    "password" : "insecure"
                },
            ],
            "role" : [],
            "locked" : False,
        },
        "ms10-35-mcdivittB0" : {
            "arch" : ['arm64'],
            "sub-arch" : "xgene-uboot",
            "provisioner" : "hyper-maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.229.65.1",
                    "username" : "Administrator",
                    "password" : "password",
                    "node" : "c35n1"
                },
            ],
            "role" : ["sru"],
            'series-blacklist' : [
                'lucid', 'precise',
                ],
            "locked" : False,
        },
        "ms10-34-mcdivittB0" : {
            "arch" : ['arm64'],
            "sub-arch" : "xgene-uboot",
            "provisioner" : "hyper-maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.229.65.1",
                    "username" : "Administrator",
                    "password" : "password",
                    "node" : "c34n1"
                },
            ],
            #"role" : "SRU 2 Testing",
            'series-blacklist' : [
                'lucid', 'precise',
                ],
            "role" : [],
            "locked" : False,
        },
        # -----------------------------------------------------------------------------------------
        # The following systems are either dead or not working reliably enough to make use of.
        #

        "zuijin" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.223",
                    "username" : "admin",
                    "password" : "insecure"
                },
            ],
            "role" : [],
            "locked" : False,
        },
        "zmeu" : {
            "arch" : ['amd64', 'i386'],
            "scratch drive" : "/dev/sdb",
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.202",
                    "username" : "admin",
                    "password" : "insecure"
                },
            ],
            "role" : [],
            "locked" : False,
        },
        "larsen" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "192.168.228.90",
                    "username" : "Administrator",
                    "password" : "insecure"
                },
            ],
            "role" : [],
            "locked" : False,
        },
        "waldorf" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "cobbler",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "cdu",
                    "address" : "10.98.4.30",
                    "port" : "waldorf_ps1",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                }
            ],
            "role" : ["gone"],
            "locked" : True,
        },
        "bifur" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.98.5.73",
                    "username" : "root",
                    "password" : "insecure"
                },
            ],
            "role" : ["dead"],
            "locked" : False,
        },
        "dori" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "cdu",
                    "address" : "10.98.4.32",
                    "port" : "dori_ps1",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                },
                {
                    "type" : "cdu",
                    "address" : "10.98.4.33",
                    "port" : "dori_ps2",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                }
            ],
            "role" : ["dead"],
            "locked" : False,
        },
        "bofur" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "cdu",
                    "address" : "10.98.4.30",
                    "port" : "bofur_ps1",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                },
                {
                    "type" : "cdu",
                    "address" : "10.98.4.31",
                    "port" : "bofur_ps2",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                }
            ],
            "role" : ["busted"],
            "locked" : False,
        },
        "gimli" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "cdu",
                    "address" : "10.98.4.30",
                    "port" : "gimli_ps1",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                },
                {
                    "type" : "cdu",
                    "address" : "10.98.4.31",
                    "port" : "gimli_ps2",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                }
            ],
            "role" : [],
            "locked" : False,
        },
        "floyd" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "cdu",
                    "address" : "10.98.4.32",
                    "port" : "floyd_ps1",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                },
                {
                    "type" : "cdu",
                    "address" : "10.98.4.33",
                    "port" : "floyd_ps2",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                }
            ],
            "role" : ["down"],
            "locked" : False,
        },
        "janice" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "cdu",
                    "address" : "10.98.4.32",
                    "port" : "janice_ps1",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                },
                {
                    "type" : "cdu",
                    "address" : "10.98.4.33",
                    "port" : "janice_ps2",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                }
            ],
            "role" : ["down"],
            "locked" : False,
        },
        "pops" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "cdu",
                    "address" : "10.98.4.30",
                    "port" : "pops_ps1",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                },
                {
                    "type" : "cdu",
                    "address" : "10.98.4.31",
                    "port" : "pops_ps2",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                }
            ],
            "role" : ["openstack"],
            "locked" : False,
        },
        "zoot" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "cdu",
                    "address" : "10.98.4.30",
                    "port" : "zoot_ps1",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                },
                {
                    "type" : "cdu",
                    "address" : "10.98.4.31",
                    "port" : "zoot_ps2",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                }
            ],
            "role" : ["openstack"],
            "locked" : False,
        },
    }

}

# vi:set ts=4 sw=4 expandtab syntax=python:
