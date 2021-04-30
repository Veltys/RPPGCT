#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Original title    : netisup.py
# Title             : internet.py
# Description       : Módulo auxiliar para la comprobación de si hay o no Internet
# Original author   : linuxitux
# Author            : Veltys
# Date              : 2021-04-30
# Version           : 2.1.0
# Usage             : python3 internet.py o from internet import hay_internet
# Notes             : Se debe poder generar tráfico ICMP (ping), es decir, no debe ser bloqueado por un cortafuegos
#                     Este módulo está pensado para ser llamado desde otros módulos y no directamente, aunque si es llamado de esta forma, también hará su trabajo e informará al usuario de si hay conexión a Internet


import errno                                                                    # Códigos de error
import os                                                                       # Funciones del sistema operativo
from subprocess import run                                                      # Llamadas a programas externos
import sys                                                                      # Funcionalidades varias del sistema


try:
    from config import internet_config as config                                # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)


def ping(host):
    ''' Realiza un ping a un host dado
    '''

    if sys.platform.startswith('win'):                                          # Si la plataforma en la que nos hallamos es Windows
        ret = run(['C:\Windows\System32\PING.EXE', '-n', '3', '-w', '5000', host], stdout = open(os.devnull, 'w'), stderr = open(os.devnull, 'w'))
    else:                                                                       # En caso contrario, se asume UNIX (o POSIX)
        ret = run(['/bin/ping', '-c', '3', '-W', '5', host], stdout = open(os.devnull, 'w'), stderr = open(os.devnull, 'w'))

    return ret.returncode == 0                                                  # Se evalúa si el resultado es el esperado y se devuelve éste


def hay_internet(h = None):
    ''' Comprueba si hay o no acceso a Internet
    '''

    res = False                                                                 # Precarga del resultado en caso de fallo

    if h == None:                                                               # Si no se han cargado hosts por defecto
        hosts = []                                                              #     Se inicializa la lista de hosts vacía
    else:                                                                       # Si sí
        hosts = h                                                               #     Se inicializa la lista de hosts con los que han entrado

    hosts.extend(config.HOSTS)                                                  # Se añaden a la lista de hosts los preconfigurados

    for host in hosts:                                                          # Se recorre la lista de hosts
        if ping(host):                                                          #     Se hace ping a cada uno, si la respuesta es positiva
            res = True                                                          #         Se establece el resultado como positivo

            break                                                               #         Se detiene la ejecución

    return res                                                                  # Se devuelve el resultado


def main(argv):
    if hay_internet(argv[1:]):
        print('¡Hay Internet! =D')
    else:
        print('¡No hay Internet! D=')


if __name__ == '__main__':
    main(sys.argv)
