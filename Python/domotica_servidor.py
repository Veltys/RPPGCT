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


import errno                                                                    # Códigos de error
import sys                                                                      # Funcionalidades varias del sistema

try:
    from config import domotica_servidor_config as config                       # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file=sys.stderr)
    sys.exit(errno.ENOENT)

from time import sleep                                                          # Para hacer pausas
import comun                                                                    # Funciones comunes a varios sistemas
import multiprocessing                                                          # Multiprocesamiento
import os                                                                       # Funcionalidades varias del sistema operativo
import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO


class domotica_servidor(comun.app):
    def __init__(self, config, nombre):
        super().__init__(config, nombre)

    def bucle(self):
        try:
            if DEBUG:
                print('Padre #', os.getpid(), "\tMi configuración es: ", self._config.GPIOS, sep = '')
                print('Padre #', os.getpid(), "\tPienso iniciar ", int(len(self._config.GPIOS) / 2), ' hijos', sep = '')
 
            # Preparación de los parámetros que van a recibir los hijos
            parametros = []
            for i in range(int(len(self._config.GPIOS) / 2)):
                parametros.append([])

            for i in range(len(self._config.GPIOS)):
                if i % 2 == 0:
                    parametros[int(i / 2)].append(self._config.GPIOS[i])

                else:
                    parametros[int(i / 2)].append(self._config.GPIOS[i])

            # Creación de la piscina
            self._hijos = []
            for i in range(int(len(self._config.GPIOS) / 2)):
                if DEBUG:
                    print('Padre #', os.getpid(), "\tCreando hijo: ", i, sep = '')

                self._hijos.append(multiprocessing.Process(name = 'Hijo ' + str(i), target = domotica_servidor_hijos(parametros[i]).bucle))

            # Arrancamos los hijos
            if DEBUG:
                print('Padre #', os.getpid(), "\tArrancando hijos")

            for hijo in hijos:
                hijo.start()

            # Bucle para finalización y procesamiento
            while hijos:
                for hijo in hijos:
                    if not(hijo.is_alive()):
                        hijo.join()
                        hijos.remove(hijo)
                        del(hijo)
                
                if DEBUG:
                    print('Padre #', os.getpid(), "\tEsperando...")
                    
                sleep(self._config.PAUSA)
 
        except KeyboardInterrupt:
            sys.exit(0)

    def __del__(self):
        if DEBUG:
            print('Padre #', os.getpid(), "\tTerminando...")
                    
        for hijo in self._hijos:
            if hijo.is_alive():
                hijo.join()
                hijo.terminate()
                del(hijo)

        super().__del__()


class domotica_servidor_hijos(comun.app):
    def __init__(self, config_GPIOS, nombre = False):
        if DEBUG:
            print('Hijo #', os.getpid(), "\tMis parámetros son: ", config_GPIOS, sep = '')
            print('Hijo #', os.getpid(), "\tMi configuración de GPIOS heredada es: ", config.GPIOS, sep = '')

        config.GPIOS = config_GPIOS
        del(self._hijos)

        super().__init__(config, nombre)

        if DEBUG:
            print('Hijo #', os.getpid(), "\tLa he sustituido por: ", self._config.GPIOS, sep = '')


    def bucle(self):
        if DEBUG:
            print('Hijo #', os.getpid(), "\tTrabajando...", sep = '')

            while True:
                for i in range(0, int(len(self._config.GPIOS)), 2):
                    if GPIO.input(self._config.GPIOS[i][0]) and not(self._config.GPIOS[i][1]):
                        if(self._config.GPIOS[i][2]):
                            GPIO.output(self._config.GPIOS[i + 1][0], GPIO.LOW if self._config.GPIOS[i + 1][2] else GPIO.HIGH)
                        else:
                            GPIO.output(self._config.GPIOS[i + 1][0], GPIO.HIGH if self._config.GPIOS[i + 1][2] else GPIO.LOW)

                        self._config.GPIOS[i][2] = not(self._config.GPIOS[i][2])
                        self._config.GPIOS[i][1] = not(self._config.GPIOS[i][1])

                    elif not(GPIO.input(self._config.GPIOS[i][0])) and self._config.GPIOS[i][1]:
                        self._config.GPIOS[i][1] = not(self._config.GPIOS[i][1])

                    # else:

                sleep(self._config.PAUSA)

    def __del__(self):
        if DEBUG:
            print('Hijo #', os.getpid(), "\tRecibida orden de cierre. Terminando...")
                    
        super().__del__()



def main(argv = sys.argv):
     app = domotica_servidor(config, os.path.basename(sys.argv[0]))
     app.arranque()


if __name__ == '__main__':
    main(sys.argv)
