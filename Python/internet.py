#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Original title      : netisup.py
# Title               : internet.py
# Description         : Check if your Internet connection is alive
# Author              : linuxitux
# Adapted by          : Veltys
# Date                : 01-02-2016
# Usage               : ./internet.py
# Notes               : ICMP traffic must not be filtered


from subprocess import call
import sys
import time


hosts = ['***REMOVED***', '***REMOVED***', 'google.es']


def ping(host):
    ret = call(['ping', '-c', '3', '-W', '5', host], stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
    return ret == 0


def hay_internet():
    internet = 0

    for host in hosts:
        if ping(host):
            internet = 1
            break

    return internet


def main(argv = sys.argv):
    if hay_internet():
        print('Hay Internet')
    else:
        print('No hay Internet')


if __name__ == '__main__':
    main(sys.argv)
