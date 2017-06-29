#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : pid.py
# Description   : Módulo auxiliar para ciertas funciones de bloqueo y de PIDs
# Author        : Veltys
# Date          : 29-06-2017
# Version       : 0.1.5
# Usage         : python3 pid.py
# Notes         : TODO: Trabajar con PIDs, aún no es necesario y no está implementado


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
