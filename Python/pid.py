#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : pid.py
# Description   : Módulo auxiliar para ciertas funciones de bloqueo y de PIDs
# Author        : Veltys
# Date          : 19-04-2019
# Version       : 1.1.0
# Usage         : import pid | from pid import <clase>
# Notes         : ...


import os                                                                                   # Funciones del sistema operativo

if os.name == 'nt':
    from tempfile import gettempdir                                                         # Obtención del directorio temporal


class _comun_pid(object):
    ''' Clase que contiene todos los métodos comunes de este sistema
    '''

    def __init__(self, nombre):
        ''' Constructor de la clase:
            - Inicializa las variables
        '''

        self._nombre = nombre


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


class bloqueo(_comun_pid):
    ''' Clase que contiene todos los métodos necesarios para llevar a cabo un (des)bloqueo
    '''

    def __init__(self, nombre):
        ''' Constructor de la clase:
            - Llama al constructor de la clase padre
            - Inicializa las variables
        '''

        super().__init__(nombre)

        self._bloqueado = False


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
            return os.path.isfile('/var/lock/' + self._nombre[0:-3] + '.lock')              #     Se retorna la comprobación correspondiente a dicho sistema

        elif os.name == 'nt':                                                               # Si se trata de un sistema con nucleo NT
            return os.path.isfile(gettempdir() + '\\' + self._nombre[0:-3] + '.lock')       #     Se retorna la comprobación correspondiente a dicho sistema

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


class pid(_comun_pid):
    ''' Clase que contiene todos los métodos necesarios para (des)activar el acceso externo sencillo por pid
    '''

    def __init__(self, nombre):
        ''' Constructor de la clase:
            - Llama al constructor de la clase padre
            - Inicializa las variables
        '''

        super().__init__(nombre)

        self._activado  = False
        self._pid       = os.getpid()


    def activar(self):
        ''' Activa el acceso externo sencillo por pid
        '''

        try:                                                                                # Bloque try
            if os.name == 'posix':                                                          #     Si se trata de un sistema POSIX
                archivo = open('/var/run/' + self._nombre[0:-3] + '.pid', 'w+')             #         Se abre un archivo de pid en el directorio /var/run

            elif os.name == 'nt':                                                           #     Si se trata de un sistema con nucleo NT
                archivo = open('./' + self._nombre[0:-3] + '.pid', 'w+')                    #         Se abre un archivo de pid en el directorio ./

            else:                                                                           #     En cualquier otro caso y ante la duda, no es posible realizar un bloqueo
                res = False                                                                 #         Por lo cual se genera el resultado del error

                archivo = False                                                             #         Precarga de la variable archivo para evitar un posterior fallo

        except IOError:                                                                     # Si no hay permiso de escritura u otro error de entrada / salida
            res = False                                                                     #     Se genera el resultado de error

        else:                                                                               # Si no ha habido fallos
            if archivo:                                                                     #     Si se ha podido realizar la apertura
                archivo.write(str(self._pid))                                               #         Se escribe el pid en el archivo

                archivo.close()                                                             #         Se cierra el archivo (sólo interesa su creación, con eso es bastante)

                self._activado = True                                                       #         Se actualiza la variable interna de información de activación

                res = True                                                                  #         Se genera el resultado de éxito

            else:                                                                           #     Si no se ha podido
                res = False                                                                 #         Se genera el resultado de error

        finally:                                                                            # En cualquier caso
            return res                                                                      #     Se devuelve el resultado previamente generado


    def comprobar(self):
        ''' Comprueba si hay ya un archivo pid previo
        '''

        if os.name == 'posix':                                                              # Si se trata de un sistema POSIX
            return os.path.isfile('/var/run/' + self._nombre[0:-3] + '.pid')                #     Se retorna la comprobación correspondiente a dicho sistema

        elif os.name == 'nt':                                                               #         Si se trata de un sistema con nucleo NT
            return os.path.isfile('./' + self._nombre[0:-3] + '.pid')                       #     Se retorna la comprobación correspondiente a dicho sistema

        else:                                                                               # En cualquier otro caso y ante la duda, no es posible realizar un bloqueo
            return False                                                                    #     Se retorna directamente False, porque no está contemplado el bloqueo en este caso


    def desactivar(self):
        ''' Desactiva el acceso externo sencillo por pid en el caso de que esté activado
        '''

        if self._activado:                                                                  # Si el hipotético acceso externo sencillo se ha activado en este sistema
            if self.comprobar():                                                            #     Si efectivamente se comprueba que el acceso externo sencillo se ha llevado a cabo
                if os.name == 'posix':                                                      #         Si se trata de un sistema POSIX
                    os.remove('/var/run/' + self._nombre[0:-3] + '.pid')                    #             Se elimina el archivo de bloqueo

                elif os.name == 'nt':                                                       #         Si se trata de un sistema con nucleo NT
                    os.remove('./' + self._nombre[0:-3] + '.pid')                           #             Se elimina el archivo de bloqueo

            self._activado = False                                                          #     Sea como fuere, se actualiza la variable interna de información de activación


    def pid(self):
        ''' Observador de la variable "_pid" de la clase
        '''

        return self._pid
