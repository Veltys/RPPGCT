#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : domotica.py
# Description   : Sistema gestor de domótica
# Author        : Veltys
# Date          : 04-07-2017
# Version       : 1.0.0
# Usage         : python3 domotica.py
# Notes         : Sistema en el que se gestionarán pares de puertos GPIO
#                 Las entradas impares en la variable de configuración asociada GPIOS corresponderán a los relés que se gestionarán
#                 Las pares, a los pulsadores que irán asociados a dichos relés, para su conmutación
#                 Se está estudiando, para futuras versiones, la integración con servicios IoT, especuialmente con el "AWS IoT Button" --> http://amzn.eu/dsgsHvv


import errno                                                                    # Códigos de error
import sys                                                                      # Funcionalidades varias del sistema

try:
  from config import temperaturas_config as config                              # Configuración

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

    def bucle():
        try:
            i = 1

            while True:
                print('Esperando un evento en el PIN GPIO', GPIO_BOTON, "\r\nID del evento: ", i, sep='')
                GPIO.wait_for_edge(GPIO_BOTON, GPIO.RISING)
                print('Se ha detectado un evento de activación en el PIN GPIO', GPIO_BOTON, "\r\nID del evento: ", i, sep = '')
                GPIO.wait_for_edge(GPIO_BOTON, GPIO.FALLING)
                print('Se ha detectado un evento de desactivación en el PIN GPIO', GPIO_BOTON, "\r\nID del evento: ", i, sep='')
                i = i + 1

        except KeyboardInterrupt:
            self.cerrar()


def main(argv = sys.argv):
    app = temperaturas(config)
    app.arranque(os.path.basename(argv[0]))


if __name__ == '__main__':
    main(sys.argv)
