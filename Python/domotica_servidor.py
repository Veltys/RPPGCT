#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : domotica_servidor.py
# Description   : Parte servidor del sistema gestor de domótica
# Author        : Veltys
# Date          : 15-07-2017
# Version       : 0.2.0
# Usage         : python3 domotica_servidor.py
# Notes         : Parte servidor del sistema en el que se gestionarán pares de puertos GPIO
#                 Las entradas impares en la variable de configuración asociada GPIOS corresponderán a los relés que se gestionarán
#                 Las pares, a los pulsadores que irán asociados a dichos relés, para su conmutación
#                 Pendiente (TODO): Por ahora solamente responde a un pulsador local, queda pendiente la implementación remota (sockets)
#                 Se está estudiando, para futuras versiones, la integración con servicios IoT, especuialmente con el "AWS IoT Button" --> http://amzn.eu/dsgsHvv


DEBUG = True
salir = False

import errno                                                                    # Códigos de error
import sys                                                                      # Funcionalidades varias del sistema
import os                                                                       # Funcionalidades varias del sistema operativo

try:
    from config import domotica_servidor_config as config                       # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file=sys.stderr)
    sys.exit(errno.ENOENT)

from copy import deepcopy                                                       # Copia "segura" de objetos
from threading import Thread                                                    # Capacidades multihilo
from time import sleep                                                          # Para hacer pausas
import comun                                                                    # Funciones comunes a varios sistemas
import socket                                                                   # Tratamiento de sockets
#Windows import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO


class domotica_servidor(comun.app):
    def __init__(self, config, nombre):
        super().__init__(config, nombre)

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(('', self._config.puerto))
        self._socket.listen(1)

    def bucle(self):
        try:
#Windows             if DEBUG:
#Windows                 print('Padre #', os.getpid(), "\tMi configuración es: ", self._config.GPIOS, sep = '')
#Windows                 print('Padre #', os.getpid(), "\tPienso iniciar ", int(len(self._config.GPIOS) / 2), ' hijos', sep = '')

#Windows             self._hijos = list()
#Windows             for i in range(int(len(self._config.GPIOS) / 2)):
#Windows                 if DEBUG:
#Windows                     print('Padre #', os.getpid(), "\tPreparando hijo ", i, sep = '')

#Windows                 self._hijos.append(Thread(target = main_hijos, args = (i,)))

#Windows                 if DEBUG:
#Windows                     print('Padre #', os.getpid(), "\tArrancando hijo ", i, sep = '')

#Windows                 self._hijos[i].start()

            sc, dir = self._socket.accept()
            comando = sc.recv(1024)

            if DEBUG:
                print('Padre #', os.getpid(), "\tHe recibido el comando: ", comando, sep = '')

            comando = comando.decode('utf_8')

            if DEBUG:
                print('Padre #', os.getpid(), "\tHe recibido el comando: ", comando, sep = '')

            comando = comando.lower()

            if DEBUG:
                print('Padre #', os.getpid(), "\tHe recibido el comando: ", comando, sep = '')

            while comando[0:5] != 'salir':
                sleep(self._config.PAUSA)
                comando = sc.recv(1024)

                if DEBUG:
                    print('Padre #', os.getpid(), "\tHe recibido el comando: ", comando, sep = '')

        except KeyboardInterrupt:
            self.cerrar()
            return


    def cerrar(self):
        global salir

        salir = True

        if DEBUG:
            print('Padre #', os.getpid(), "\tDisparado el evento de cierre", sep = '')

        super().cerrar()


    def __del__(self):
        super().__del__()


class domotica_servidor_hijos(comun.app):
    def __init__(self, id_hijo, config):
        ''' Constructor de la clase:
            - Inicializa variables
            - Carga la configuración
        '''

        # super().__init__()                                                                        # La llamada al constructor de la clase padre está comentada a propósito

        self._bloqueo = False
        self._config = config
        self._modo_apagado = False

        self._id_hijo = id_hijo

        self._GPIOS = list()
        self._GPIOS.append(self._config.GPIOS[self._id_hijo * 2])
        self._GPIOS.append(self._config.GPIOS[self._id_hijo * 2 + 1])
        
        if DEBUG:
            print('Hijo  #', self._id_hijo, "\tMi configuración es ", self._GPIOS, sep = '')
            print('Hijo  #', self._id_hijo, "\tDeberé escuchar en el puerto GPIO", self._GPIOS[0][0] , ' y conmutar el puerto GPIO', self._GPIOS[1][0], sep = '')



    def bucle(self):
        try:
            while not(salir):
                for i in range(0, int(len(self._GPIOS)), 2):                                            # Se recorre la configuración propia (no la general), tomandos un paso de 2, ya que los puertos se trabajan por pares
                    if DEBUG:
                        print('Hijo  #', self._id_hijo, "\tRecorriendo puertos GPIO. Voy por el puerto GPIO", self._GPIOS[i][0], sep = '')

                    if GPIO.input(self._GPIOS[i][0]) and not(self._GPIOS[i][2]):                        # Se comprueba el puerto que ha sido activado y que no sea recurrente (dejar el botón pulsado)
                        if DEBUG:
                            print('Hijo  #', self._id_hijo, "\tOrden de conmutación recibida en el puerto GPIO", self._GPIOS[i][0], sep = '')
                            print('Hijo  #', self._id_hijo, "\tComutando el puerto GPIO", self._GPIOS[i + 1][0], sep = '')

                        GPIO.output(self._GPIOS[i + 1][0], not(GPIO.input(self._GPIOS[i + 1][0])))      # Se conmuta la salida del puerto GPIO

                        self._GPIOS[i][2] = not(self._GPIOS[i][2])                                      # Se indica que el puerto que ha sido activado

                    elif not(GPIO.input(self._GPIOS[i][0])) and self._GPIOS[i][2]:                      # Se comprueba el puerto que ha sido desactivado y que antes había sido activado
                        if DEBUG:
                            print('Hijo  #', self._id_hijo, "\tEl puerto GPIO", self._GPIOS[i][0], ' ha sido levantado', sep = '')

                        self._GPIOS[i][2] = not(self._GPIOS[i][2])                                      # Se indica que el el puerto que ha sido desactivado

                    # else:

                sleep(self._config.PAUSA)

        except KeyboardInterrupt:
            self.cerrar()
            return


    def cerrar(self):
        if DEBUG:
            print('Hijo #', self._id_hijo, "\tDisparado el evento de cierre", sep = '')

        # super().cerrar()


    def __del__(self):
        # super().__del__()                                                                         # La llamada al constructor de la clase padre está comentada a propósito
        pass


def main(argv = sys.argv):
    app = domotica_servidor(config, os.path.basename(sys.argv[0]))
    app.arranque()


def main_hijos(argv):
    app = domotica_servidor_hijos(argv, config)
    app.arranque()


if __name__ == '__main__':
    main(sys.argv)
