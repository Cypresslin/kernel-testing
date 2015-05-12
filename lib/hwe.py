#!/usr/bin/env python
#

# The relationships of a hardware enablement (hwe) kernel for a
# series to the LTS series it 'enables'.
#
HWE = {
        'lucid' : {
            'series' : None,
        },
        'precise' : {
            'series' : None,
        },
        'quantal' : {
            'series' : 'precise',
            'package' : 'linux-generic-lts-quantal',
        },
        'saucy' : {
            'series' : 'precise',
            'package' : 'linux-generic-lts-saucy',
        },
        'trusty' : {
            'series' : 'precise',
            'package' : 'linux-generic-lts-trusty',
        },
        'utopic' : {
            'series' : 'trusty',
            'package' : 'linux-generic-lts-utopic',
        },
        'vivid' : {
            'series' : 'trusty',
            'package' : 'linux-generic-lts-utopic',
            'ppa' : True
        },
        'wily' : {
            'series' : 'trusty',
            'package' : 'linux-generic-lts-wily',
            'ppa' : True
        },
}

# vi:set ts=4 sw=4 expandtab:
