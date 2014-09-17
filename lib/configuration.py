#!/usr/bin/env python
#

Configuration = {

    # The Jenkins server section. My Jenkins server is named 'jenkins'.
    #
    "jenkins" : {
        "server_url" : "http://10.98.2.20:8080"
    },

    # I only have one MAAS server and it's named 'maas'.
    #
    "maas" : {
        "server"  : "maas",          # Hostname of this maas server.
        "profile" : "jenkins",       # When talking to the maas server use this profile.
        "creds"   : "VxFpPVkTJ8fkH6MqCq:GC9QjEr4GFaHe2dFcC:eWELKWXvVpTRa8Vzkb9CajVVH2vhXTv9",
        "user"    : "jenkins",       # When ssh'ing to the maas server use this user
        "type"    : "maas"           # This _is_ a MAAS server (as opposed to a cobbler server)
    },

    # I don't have a cobbler server so I could just leave this section
    # out. However, if I did have a cobbler server it would be named
    # 'cobbler'.
    #
    "cobbler" : {
        "server"  : "cobbler",
        "type"    : "cobbler"
    }
}

# vi:set ts=4 sw=4 expandtab syntax=python:
