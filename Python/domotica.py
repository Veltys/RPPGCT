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
# import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO
import RPIO as GPIO


class domotica(comun.app):
    def __init__(self, config):
        super().__init__(config)

    def bucle(self):
        try:
            for i in range(0, int(len(self._config.GPIOS)), 2):
                # GPIO interrupt callbacks
                RPIO.add_interrupt_callback(config.GPIOS[i][0], gpio_callback)

            while True:
                GPIO.wait_for_interrupts()
        except KeyboardInterrupt:
            self.cerrar()


def gpio_callback(gpio_id, val):
    print("gpio %s: %s" % (gpio_id, val))


def main(argv = sys.argv):
     app = domotica(config)
     app.arranque(os.path.basename(argv[0]))


if __name__ == '__main__':
    main(sys.argv)
