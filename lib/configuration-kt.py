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
        "gonzo" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "cobbler",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.227",
                    "username" : "maas",
                    "password" : "3tHOR7kJvXP"
                },
            ],
            "role" : "colin",
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
                    "username" : "maas",
                    "password" : "GY31V77wr"
                },
            ],
            "role" : "testing",
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
                    "password" : "lZ6ZpxRKMJGd7E"
                },
            ],
            "role" : "openstack",
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
                    "password" : "145M3gj5sm8NMX"
                },
            ],
            "role" : "none",
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
                    "username" : "maas",
                    "password" : "jwolLJyecdWB"
                },
            ],
            "role" : "openstack",
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
                    "username" : "maas",
                    "password" : "wi7hthvxPpNH3"
                },
            ],
            "role" : "smb",
            "locked" : False,
        },
        "tarf" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.222",
                    "username" : "maas",
                    "password" : "PcnHDCZbb0aIvi"
                },
            ],
            "role" : "none",
            "locked" : False,
        },
        "alkaid" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.219",
                    "username" : "maas",
                    "password" : "XN40Btk6aji"
                },
            ],
            "role" : "none",
            "locked" : False,
        },
        "phact" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.224",
                    "username" : "maas",
                    "password" : "66W9ZESwzWdza"
                },
            ],
            "role" : "none",
            "locked" : False,
        },
        "rukbah" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.206",
                    "username" : "maas",
                    "password" : "08JqQ3y4IpuN"
                },
            ],
            "role" : "none",
            "locked" : False,
        },
        "zmeu" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.202",
                    "username" : "maas",
                    "password" : "BE7Orv9A"
                },
            ],
            "role" : "none",
            "locked" : False,
        },
        "zuijin" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.223",
                    "username" : "maas",
                    "password" : "XT9Jlikfw226AKp"
                },
            ],
            "role" : "none",
            "locked" : False,
        },
        "onza" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
            "power" : [
                {
                    "type" : "ipmi",
                    "address" : "10.245.80.207",
                    "username" : "maas",
                    "password" : "gkMEkXdhy5"
                },
            ],
            "role" : "none",
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
                    "username" : "maas",
                    "password" : "DJ6DA9qA"
                },
            ],
            "role" : "none",
            "locked" : False,
        },

        # ----------------

        "fozzie" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "cobbler",
            "jenkins server" : "kernel-jenkins",
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
            "role" : "unknown",
            "locked" : False,
        },
        "statler" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "cobbler",
            "jenkins server" : "kernel-jenkins",
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
        "fili" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
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

        "etnyre" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
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
        "rainier" : {
            "arch" : ['amd64', 'i386'],
            "provisioner" : "maas",
            "jenkins server" : "kernel-jenkins",
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
