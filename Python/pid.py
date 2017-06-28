#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os                                                                       # Funciones del sistema operativo


def bloquear(nombre):
    try:
        archivo = open('/var/lock/' + nombre[0:-3] + '.lock', 'w+')
        archivo.close()
        return True

    except IOError:
        return False


def comprobar(nombre):
    return not(os.path.isfile('/var/lock/' + nombre[0:-3] + '.lock'))

def desbloquear(nombre):
    os.remove('/var/lock/' + nombre[0:-3] + '.lock')
