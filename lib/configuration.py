#!/usr/bin/env python
#

Configuration = {

    # The Jenkins server section. My Jenkins server is named 'jenkins'.
    #
    "jenkins" : {
        "server_url" : "http://jenkins:8080"
    },

    # I only have one MAAS server and it's named 'maas'.
    #
    "maas" : {
        "server"  : "maas",          # Hostname of this maas server.
        "profile" : "jenkins",       # When talking to the maas server use this profile.
        "creds"   : "VxFpPVkTJ8fkH6MqCq:GC9QjEr4GFaHe2dFcC:eWELKWXvVpTRa8Vzkb9CajVVH2vhXTv9",
        "user"    : "jenkins",       # When ssh'ing to the maas server use this user
        "type"    : "maas",          # This _is_ a MAAS server (as opposed to a cobbler server)
        "sut-user": "ubuntu",        # The user on the test system after it's been provisioned
    },

    # I don't have a cobbler server so I could just leave this section
    # out. However, if I did have a cobbler server it would be named
    # 'cobbler'.
    #
    "cobbler" : {
        "server"  : "cobbler",
        "type"    : "cobbler",
        "sut-user": "jenkins",       # The user on the test system after it's been provisioned
    },

    # Test systems section. This is a dictionary of all the test systems that are available
    # to me.
    #
    "systems" : {
        "nuc1" : {
            "arch" : "x86",
            "provisioner" : "maas",
            "jenkins server" : "jenkins",
            "mac address" : "ec:a8:6b:fa:91:64",
            "power" : [
                {
                    "type"     : "amt",
                    "address"  : "10.10.10.100", # "ec:a8:6b:fa:91:64"
                    "user"     : "admin",
                    "password" : "1Pa**word"
                }
            ],
            "role" : "testing",
            "locked" : False
        },
        "nuc2" : {
            "arch" : "x86",
            "provisioner" : "maas",
            "jenkins server" : "jenkins",
            "mac address" : "ec:a8:6b:fa:6f:be",
            "power" : [
                {
                    "type"     : "amt",
                    "address"  : "10.10.10.101", # "ec:a8:6b:fa:6f:be"
                    "user"     : "admin",
                    "password" : "1Pa**word"
                }
            ],
            "role" : "testing",
            "locked" : False
        },
        "oin" : {
            "arch" : "x86",
            "provisioner" : "maas",
            "jenkins server" : "jenkins",
            "mac address" : "74:27:ea:d5:8b:c9",
            "power" : [
                {
                    "type"     : "dli", # Digital Loggers, Inc. PDU
                    "address"  : "10.10.10.200",
                    "user"     : "admin",
                    "password" : "admin",
                    "outlet"   : 1
                }
            ],
            "role" : "testing",
            "locked" : False
        },
        "gloin" : {
            "arch" : "x86",
            "provisioner" : "maas",
            "jenkins server" : "jenkins",
            "mac address" : "74:27:ea:d5:8b:63",
            "power" : [
                {
                    "type"     : "dli", # Digital Loggers, Inc. PDU
                    "address"  : "10.10.10.200",
                    "user"     : "admin",
                    "password" : "admin",
                    "outlet"   : 0
                }
            ],
            "role" : "testing",
            "locked" : False
        }
    }

}

# vi:set ts=4 sw=4 expandtab syntax=python:
