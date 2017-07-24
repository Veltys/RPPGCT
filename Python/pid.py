#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : pid.py
# Description   : Módulo auxiliar para ciertas funciones de bloqueo y de PIDs
# Author        : Veltys
# Date          : 23-07-2017
# Version       : 0.2.1
# Usage         : import pid | from pid import <clase>
# Notes         : TODO: Trabajar con PIDs, aún no es necesario y no está implementado


import os                                                                       # Funciones del sistema operativo

if os.name == 'nt':
    from tempfile import gettempdir                                             # Obtención del directorio temporal

class bloqueo(object):
    def __init__(self,nombre):
        self._bloqueado = False
        self._nombre = nombre


    def bloquear(self):
        try:
            if os.name == 'posix':
                archivo = open('/var/lock/' + self._nombre[0:-3] + '.lock', 'w+')

            elif os.name == 'nt':
                archivo = open(gettempdir() + '/' + self._nombre[0:-3] + '.lock', 'w+')

            else:
                return False

            archivo.close()
            self._bloqueado = True
            return True

        except IOError:
            return False


    def comprobar(self):
        if os.name == 'posix':
            return not(os.path.isfile('/var/lock/' + self._nombre[0:-3] + '.lock'))
    
        elif os.name == 'nt':
            return not(os.path.isfile(gettempdir() + '\\' + self._nombre[0:-3] + '.lock'))
    
        else:
            return False


    def desbloquear(self):
        if self._bloqueado:
            if os.name == 'posix':
                os.remove('/var/lock/' + self._nombre[0:-3] + '.lock')

            elif os.name == 'nt':
                os.remove(gettempdir() + '\\' + self._nombre[0:-3] + '.lock')

            else:
                pass

            self._bloqueado = False


    def nombre(self, nombre = False):
        if nombre == False:
            return self._nombre
        else:
            self._nombre = nombre
