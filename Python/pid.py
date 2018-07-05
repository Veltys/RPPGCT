#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : pid.py
# Description   : Módulo auxiliar para ciertas funciones de bloqueo y de PIDs
# Author        : Veltys
# Date          : 04-07-2018
# Version       : 0.2.3
# Usage         : import pid | from pid import <clase>
# Notes         : TODO: Trabajar con PIDs, aún no es necesario y no está implementado


import os                                                                                   # Funciones del sistema operativo

if os.name == 'nt':
    from tempfile import gettempdir                                                         # Obtención del directorio temporal


class bloqueo(object):
    ''' Clase que contiene todos los métodos necesarios para llevar a cabo un (des)bloqueo
    '''

    def __init__(self, nombre):
        ''' Constructor de la clase:
            - Inicializa las variables
        '''

        self._bloqueado = False
        self._nombre    = nombre


    def bloquear(self):
        ''' Lleva a cabo un "bloqueo" para impedir la ejecución de otra instacia de la app que lo solicite
        '''

        archivo = False                                                                     # Precarga de la variable archivo para evitar un posterior fallo

        try:                                                                                # Bloque try
            if os.name == 'posix':                                                          #     Si se trata de un sistema POSIX
                archivo = open('/var/lock/' + self._nombre[0:-3] + '.lock', 'w+')           #         Se abre un archivo de bloqueo en el directorio /var/lock

            elif os.name == 'nt':                                                           #     Si se trata de un sistema con nucleo NT
                archivo = open(gettempdir() + '/' + self._nombre[0:-3] + '.lock', 'w+')     #         Se abre un archivo de bloqueo en el directorio temporal

            else:                                                                           #     En cualquier otro caso y ante la duda, no es posible realizar un bloqueo
                res = False                                                                 #         Por lo cual se genera el resultado del error

        except IOError:                                                                     # Si no hay permiso de escritura u otro error de entrada / salida
            res = False                                                                     #     Se genera el resultado de error

        else:                                                                               # Si no ha habido fallos
            if archivo:                                                                     #     Si se ha podido realizar la apertura
                archivo.close()                                                             #         Se cierra el archivo (sólo interesa su creación, con eso es bastante)

                self._bloqueado = True                                                      #         Se actualiza la variable interna de información de bloqueo

                res = True                                                                  #         Se genera el resultado de éxito

        return res                                                                          # Se devuelve el resultado previamente generado


    def comprobar(self):
        ''' Comprueba si hay ya un "bloqueo" previo
        '''

        if os.name == 'posix':                                                              # Si se trata de un sistema POSIX
            return not(os.path.isfile('/var/lock/' + self._nombre[0:-3] + '.lock'))         #     Se retorna la comprobación correspondiente a dicho sistema

        elif os.name == 'nt':                                                               # Si se trata de un sistema con nucleo NT
            return not(os.path.isfile(gettempdir() + '\\' + self._nombre[0:-3] + '.lock'))  #     Se retorna la comprobación correspondiente a dicho sistema

        else:                                                                               # En cualquier otro caso y ante la duda, no es posible realizar un bloqueo
            return False                                                                    #     Se retorna directamente False, porque no está contemplado el bloqueo en este caso


    def desbloquear(self):
        ''' Deshace un "bloqueo" en caso de que lo haya
        '''

        if self._bloqueado:                                                                 # Si el hipotético bloqueo se ha realizado por este sistema
            if self.comprobar():                                                            #     Si efectivamente se comprueba que el bloqueo se ha llevado a cabo
                if os.name == 'posix':                                                      #         Si se trata de un sistema POSIX
                    os.remove('/var/lock/' + self._nombre[0:-3] + '.lock')                  #             Se elimina el archivo de bloqueo

                elif os.name == 'nt':                                                       #         Si se trata de un sistema con nucleo NT
                    os.remove(gettempdir() + '\\' + self._nombre[0:-3] + '.lock')           #             Se elimina el archivo de bloqueo

            self._bloqueado = False                                                         #     Sea como fuere, se actualiza la variable interna de información de bloqueo


    def nombre(self, nombre = False):
        ''' Función "sobrecargada" gracias al parámetro "nombre"
            - Para "nombre" == "False"
                - Actúa como observador de la variable "_nombre" de la clase
            - Para "nombre" != "False"
                - Actúa como modificador de la variable "_nombre" de la clase
        '''

        if nombre == False:
            return self._nombre

        else:
            self._nombre = nombre
