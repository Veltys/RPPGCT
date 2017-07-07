#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : domotica.py
# Description   : Sistema gestor de domótica
# Author        : Veltys
# Date          : 07-07-2017
# Version       : 1.0.0
# Usage         : python3 domotica.py
# Notes         : Sistema en el que se gestionarán pares de puertos GPIO
#                 Las entradas impares en la variable de configuración asociada GPIOS corresponderán a los relés que se gestionarán
#                 Las pares, a los pulsadores que irán asociados a dichos relés, para su conmutación
#                 Se está estudiando, para futuras versiones, la integración con servicios IoT, especuialmente con el "AWS IoT Button" --> http://amzn.eu/dsgsHvv


debug = True


import errno                                                                    # Códigos de error
import sys                                                                      # Funcionalidades varias del sistema

try:
  from config import domotica_config as config                                  # Configuración

except ImportError:
  print('Error: Archivo de configuración no encontrado', file=sys.stderr)
  sys.exit(errno.ENOENT)

from time import sleep                                                          # Para hacer pausas
import comun                                                                    # Funciones comunes a varios sistemas
import os                                                                       # Funcionalidades varias del sistema operativo
import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO


class domotica(comun.app):
    def __init__(self, config):
        super().__init__(config)

    def bucle(self):
        try:
            while True:
                for i in range(0, int(len(self._config.GPIOS)), 2):
                    if GPIO.input(self._config.GPIOS[i][0]) and not(self._config.GPIOS[i][1]):
                        if debug:
                            print('El pin GPIO', self._config.GPIOS[i][0], ' se ha levantado. ', 'apagando' if self._config.GPIOS[i][2] else 'encendiendo' ,' el LED asociado al ping GPIO', self._config.GPIOS[i + 1][0], '.', sep = '')

                        if(self._config.GPIOS[i][2]):
                            GPIO.output(self._config.GPIOS[i + 1][0], GPIO.LOW if self._config.GPIOS[i + 1][2] else GPIO.HIGH)
                        else:
                            GPIO.output(self._config.GPIOS[i + 1][0], GPIO.HIGH if self._config.GPIOS[i + 1][2] else GPIO.LOW)

                        self._config.GPIOS[i][2] = not(self._config.GPIOS[i][2])
                        self._config.GPIOS[i][0] = not(self._config.GPIOS[i][0])

                    elif not(GPIO.input(self._config.GPIOS[i][0])) and self._config.GPIOS[i][1]:
                        if debug:
                            print('El pin GPIO', self._config.GPIOS[i][0], ' se ha bajado. ', sep = '')

                        self._config.GPIOS[i][0] = not(self._config.GPIOS[i][0])

                    else:
                        if debug:
                            print('Estoy esperando a que el pin GPIO', self._config.GPIOS[i][0], ' se baje', sep = '')
            
                sleep(self._config.PAUSA)

        except KeyboardInterrupt:
            self.cerrar()


def main(argv = sys.argv):
     app = domotica(config)
     app.arranque(os.path.basename(argv[0]))


if __name__ == '__main__':
    main(sys.argv)
