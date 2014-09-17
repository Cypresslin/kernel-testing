#!/usr/bin/env python
#

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
        'trusty' : {
            'series' : 'precise',
            'package' : 'linux-generic-lts-trusty',
            'ppa' : True,
        },
        'utopic' : {
            'series' : 'trusty',
            'package' : 'linux-generic-lts-utopic',
            'ppa' : True,
        },
}

# vi:set ts=4 sw=4 expandtab:
