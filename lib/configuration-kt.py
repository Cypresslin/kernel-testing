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
        "creds"   : "NZn8yvnLAJEGD5bMmk:YfFPyvrspJDbf4cHsd:ZcfkrFk98FwRpwYyv5DVvDmAjRGWXGKn",
        "user"    : "jenkins",       # When ssh'ing to the maas server use this user
        "type"    : "maas",          # This _is_ a MAAS server (as opposed to a cobbler server)
        "sut_user": "ubuntu",        # The user on the test system after it's been provisioned
    },

    # Test systems section. This is a dictionary of all the test systems that are available
    # to me.
    #
    "systems" : {
        #  "nuc1" : {
        #      "arch" : ['amd64', 'i386'],
        #      "provisioner" : "maas",
        #      "jenkins server" : "jenkins",
        #      "mac address" : "ec:a8:6b:fa:91:64",
        #      "power" : [
        #          {
        #              "type"     : "amt",
        #              "address"  : "10.10.10.100", # "ec:a8:6b:fa:91:64"
        #              "user"     : "admin",
        #              "password" : "1Pa**word"
        #          }
        #      ],
        #      "role" : "testing",
        #      "locked" : False
        #  },
        #  "nuc2" : {
        #      "arch" : ['amd64', 'i386'],
        #      "provisioner" : "maas",
        #      "jenkins server" : "jenkins",
        #      "mac address" : "ec:a8:6b:fa:6f:be",
        #      "power" : [
        #          {
        #              "type"     : "amt",
        #              "address"  : "10.10.10.101", # "ec:a8:6b:fa:6f:be"
        #              "user"     : "admin",
        #              "password" : "1Pa**word"
        #          }
        #      ],
        #      "role" : "testing",
        #      "locked" : False
        #  },
        #  "oin" : {
        #      "arch" : ['amd64', 'i386'],
        #      "provisioner" : "maas",
        #      "jenkins server" : "jenkins",
        #      "mac address" : "74:27:ea:d5:8b:c9",
        #      "power" : [
        #          {
        #              "type"     : "dli", # Digital Loggers, Inc. PDU
        #              "address"  : "10.10.10.200",
        #              "user"     : "admin",
        #              "password" : "admin",
        #              "outlet"   : 1
        #          }
        #      ],
        #      "role" : "testing",
        #      "locked" : False
        #  },
        #  "gloin" : {
        #      "arch" : ['amd64', 'i386'],
        #      "provisioner" : "maas",
        #      "jenkins server" : "jenkins",
        #      "mac address" : "74:27:ea:d5:8b:63",
        #      "power" : [
        #          {
        #              "type"     : "dli", # Digital Loggers, Inc. PDU
        #              "address"  : "10.10.10.200",
        #              "user"     : "admin",
        #              "password" : "admin",
        #              "outlet"   : 0
        #          }
        #      ],
        #      "role" : "testing",
        #      "locked" : False
        #  },



        "gonzo" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "cobbler",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "08:9e:01:3c:c9:60",
            "power" : [
                {
                    "type"     : "cdu",
                    "address"  : "10.98.4.33",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                    "port"     : "gonzo"
                },
            ],
            "role" : "colin",
            "locked" : False,
        },
        "fozzie" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "cobbler",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "90:b1:1c:10:6b:03",
            "power" : [
                {
                    "type" : "cdu",
                    "address" : "10.98.4.32",
                    "port" : "fozzie_ps1",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                },
                {
                    "type" : "cdu",
                    "address" : "10.98.4.33",
                    "port" : "fozzie_ps2",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                }
            ],
            "role" : "testing",
            "locked" : False,
        },
        "rizzo" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "jenkins",
            "mac address" : "d4:ae:52:7c:c6:2a",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.210",
                    "username" : "maas",
                    "password" : "GY31V77wr"
                },
            ],
            "role" : "testing",
            "locked" : False,
        },
        "waldorf" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "cobbler",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "00:1e:67:34:b8:5c",
            "power" : [
                {
                    "type" : "cdu",
                    "address" : "10.98.4.30",
                    "port" : "waldorf_ps1",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                }
            ],
            "role" : "unknown",
            "locked" : False,
        },
        "statler" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "cobbler",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "60:eb:69:21:2c:6c",
            "power" : [
                {
                    "type" : "cdu",
                    "address" : "10.98.4.30",
                    "port" : "statler_ps1",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                },
                {
                    "type" : "cdu",
                    "address" : "10.98.4.31",
                    "port" : "statler_ps2",
                    "username"     : "kernel",
                    "password" : "K3rn3!",
                }
            ],
            "role" : "unknown",                 # This system has a raid controler that is a pita
            "locked" : False,
        },
        "gloin" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "a0:36:9f:21:d8:f8",
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
            "role" : "none",
            "locked" : True,                      # This is used as a kernel-team build system
        },
        "nori" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "00:1e:67:94:75:98",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.98.5.77",
                    "username" : "root",
                    "password" : "insecure"
                },
            ],
            "role" : "openstack",
            "locked" : False,
        },
        "kili" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "00:1e:67:94:77:43",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.98.5.86",
                    "username" : "root",
                    "password" : "insecure"
                },
            ],
            "role" : "openstack",
            "locked" : False,
        },
        "fili" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "00:1e:67:94:89:42",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.98.5.85",
                    "username" : "root",
                    "password" : "insecure"
                },
            ],
            "role" : "openstack",
            "locked" : False,
        },
        "dwalin" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "00:1e:67:94:70:ba",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.98.5.92",
                    "username" : "root",
                    "password" : "insecure"
                },
            ],
            "role" : "arges",
            "locked" : False,
        },

        "cavac" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "ac:16:2d:aa:6c:e8",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.98.5.83",
                    "username" : "Administrator",
                    "password" : "insecure"
                },
            ],
            "role" : "openstack",
            "locked" : False,
        },
        "etnyre" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "e4:11:5b:de:01:13",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.98.5.84",
                    "username" : "Administrator",
                    "password" : "insecure"
                },
            ],
            "role" : "smb",
            "locked" : False,
        },
        "bantam" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "80:c1:6e:62:22:30",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.98.5.89",
                    "username" : "Administrator",
                    "password" : "insecure"
                },
            ],
            "role" : "unknown",
            "locked" : False,
        },
        "larsen" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "ac:16:2d:b8:cb:f8",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.98.5.90",
                    "username" : "Administrator",
                    "password" : "insecure"
                },
            ],
            "role" : "smb",
            "locked" : False,
        },
        "rainier" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "ac:16:2d:b9:25:f8",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.98.5.91",
                    "username" : "Administrator",
                    "password" : "insecure"
                },
            ],
            "role" : "openstack",
            "locked" : False,
        },
        "fuller" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "6c:3b:e5:a9:8b:08",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.98.5.87",
                    "username" : "Administrator",
                    "password" : "insecure"
                },
            ],
            "role" : "openstack",
            "locked" : False,
        },
        "dagmar" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "10:60:4b:a9:e8:b8",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.98.5.88",
                    "username" : "Administrator",
                    "password" : "insecure"
                },
            ],
            "role" : "openstack",
            "locked" : True,                      # This system has the MAAS server running in a LXC
        },

        # -----------------------------------------------------------------------------------------
        # The following systems are either dead or not working reliably enough to make use of.
        #

        "bifur" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "00:1e:67:94:7d:9b",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.98.5.73",
                    "username" : "root",
                    "password" : "insecure"
                },
            ],
            "role" : "dead",
            "locked" : False,
        },
        "dori" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "00:1e:67:59:82:08",
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
            "role" : "dead",
            "locked" : False,
        },
        "bofur" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "00:1e:67:59:7f:e9",
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
            "role" : "busted",
            "locked" : False,
        },
        "gimli" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "a0:36:9f:24:44:f8",
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
            "role" : "none",
            "locked" : False,
        },
        "floyd" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "a0:36:9f:14:65:38",
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
            "role" : "down",
            "locked" : False,
        },
        "janice" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "a0:36:9f:14:65:70",
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
            "role" : "down",
            "locked" : False,
        },
        "pops" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "a0:36:9f:0f:1c:cc",
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
            "role" : "openstack",
            "locked" : False,
        },
        "zoot" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "mac address" : "a0:36:9f:0e:ed:08",
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
            "role" : "openstack",
            "locked" : False,
        },
    }

}

# vi:set ts=4 sw=4 expandtab syntax=python:
