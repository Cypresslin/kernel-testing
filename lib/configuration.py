#!/usr/bin/env python
#
import sys
from os                             import path
import yaml

# This is a hack. The configuration was previously defined as a python dictionary named
# 'Configuration'. So that I didn't have to go around and modify a bunch of things at
# once and get them all right I've done what you see below. This enables the existing
# code to continue to work while I switch over to a yaml file based config definition.
#
def _load():
    cfg = None
    p = path.dirname(sys.argv[0])
    with open(path.join(p, 'lib', 'config.yaml'), 'r') as stream:
        cfg = yaml.safe_load(stream)
    return cfg

Configuration = _load()
