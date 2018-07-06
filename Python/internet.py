#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Original title    : netisup.py
# Title             : internet.py
# Description       : Módulo auxiliar para la comprobación de si hay o no Internet
# Original author   : linuxitux
# Author            : Veltys
# Date              : 04-07-2018
# Version           : 2.0.5
# Usage             : python3 internet.py o from internet import hay_internet
# Notes             : Se debe poder generar tráfico ICMP (ping), es decir, no debe ser bloqueado por un cortafuegos
#                     Este módulo está pensado para ser llamado desde otros módulos y no directamente, aunque si es llamado de esta forma, también hará su trabajo e informará al usuario de si hay conexión a Internet


import errno                                                                    # Códigos de error
import os                                                                       # Funciones del sistema operativo
import sys                                                                      # Funcionalidades varias del sistema

from subprocess import call                                                     # Llamadas a programas externos

try:
    from config import internet_config as config                                # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)


def ping(host):
    ''' Realiza un ping a un host dado
    '''

    if sys.platform.startswith('win'):                                          # Si la plataforma en la que nos hallamos es Windows
        ret = call(['ping', '-n', '3', '-w', '5000', host], stdout = open(os.devnull, 'w'), stderr = open(os.devnull, 'w'))
    else:                                                                       # En caso contrario, se asume UNIX (o POSIX)
        ret = call(['ping', '-c', '3', '-W', '5', host], stdout = open(os.devnull, 'w'), stderr = open(os.devnull, 'w'))

    return ret == 0                                                             # Se evalúa si el resultado es el esperado y se devuelve éste


def hay_internet():
    ''' Comprueba si hay o no acceso a Internet
    '''

    res = False                                                                 # Precarga del resultado en caso de fallo

    for host in config.HOSTS:                                                   # Se recorre la lista de hosts
        if ping(host):                                                          #     Se hace ping a cada uno, si la respuesta es positiva
            res = True                                                          #         Se establece el resultado como positivo

            break                                                               #         Se detiene la ejecución

    return res                                                                  # Se devuelve el resultado


def main(argv):
    if hay_internet():
        print('¡Hay Internet! =D')
    else:
        print('¡No hay Internet! D=')


if __name__ == '__main__':
    main(sys.argv)
