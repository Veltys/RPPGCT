#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Original title	: netisup.py
# Title			: internet.py
# Description		: Módulo auxiliar para la comprobación de si hay o no Internet
# Original author	: linuxitux
# Author		: Veltys
# Date			: 29-06-2017
# Version		: 1.0.2
# Usage			: python internet.py
# Notes			: Se debe poder generar tráfico ICMP (ping), es decir, no debe ser bloqueado por un cortafuegos
#			  Este módulo está pensado para ser llamado desde otros módulos y no directamente, aunque si es llamado de esta forma, también hará su trabajo e informará al usuario de si hay conexión a Internet


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
