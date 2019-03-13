#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script creates vpn tunnels for fortios firewall devices
"""

__author__      = "Mesut Bayrak"
__copyright__ = "Copyright 2016, Planet Earth"


import argparse

parser = argparse.ArgumentParser(description='Creates vpn tunnels')


parser.add_argument('-C','--create',
                    metavar='creator',
                    nargs='+',
                    required=False,
                    help='vpn tunnel creator requires 6 parameters')

parser.add_argument('-D','--delete',
                    metavar='deleter',
                    help='tunnel delete requires 1 paramaeter')

parser.add_argument('-L','--list',
                    metavar='lister',
                    help='lists vpn tunnels requires no parameter --detail shows tunnel status')

args = parser.parse_args()

if args.create:
    print("test")
elif args.delete:
    print("delete")
elif args.list:
    print('list')







    """
Mikronet (phase1-interface) # show
config vpn ipsec phase1-interface
    edit "Datacenter"
        set interface "wan1"
        set ike-version 2
        set dhgrp 2
        set proposal 3des-md5
        set remote-gw 185.141.110.220
        set psksecret ENC 24l+Ll/2UUxhMVZKebtODmW3etuRWxiZ0xR4ZMNyXFmPPRv9jDblOnDP3Inb6HnAA7jbzeQQaxosCLEp7BVYnhZn/TF/Eu+p2rLHDn0oK+h0dBBK
    next
end

    """