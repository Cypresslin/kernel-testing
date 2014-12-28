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
}

# vi:set ts=4 sw=4 expandtab:
