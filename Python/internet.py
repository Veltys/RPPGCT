#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Original title    : netisup.py
# Title             : internet.py
# Description       : Módulo auxiliar para la comprobación de si hay o no Internet
# Original author   : linuxitux
# Author            : Veltys
# Date              : 02-07-2017
# Version           : 2.0.3
# Usage             : python3 internet.py
# Notes             : Se debe poder generar tráfico ICMP (ping), es decir, no debe ser bloqueado por un cortafuegos
#                     Este módulo está pensado para ser llamado desde otros módulos y no directamente, aunque si es llamado de esta forma, también hará su trabajo e informará al usuario de si hay conexión a Internet


import errno                                                                    # Códigos de error
import sys                                                                      # Funcionalidades varias del sistema

try:
    from config import internet_config as config                                # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)

import os                                                                       # Funciones del sistema operativo

from subprocess import call                                                     # Llamadas a programas externos


def ping(host):
    if sys.platform.startswith('win'):
        ret = call(['ping', '-n', '3', '-w', '5000', host], stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
    else:
        ret = call(['ping', '-c', '3', '-W', '5', host], stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))

    return ret == 0


def hay_internet():
    internet = 0

    for host in config.HOSTS:
        if ping(host):
            internet = 1
            break

    return internet


def main(argv = sys.argv):
    if hay_internet():
        print('¡Hay Internet! =D')
    else:
        print('¡No hay Internet! D=')


if __name__ == '__main__':
    main(sys.argv)
