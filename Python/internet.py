#!/usr/bin/env python
# -*- coding: utf-8 -*-


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


# def main(argv = sys.argv):
#     quit(net_is_up())


# if __name__ == '__main__':
#     main(sys.argv)
