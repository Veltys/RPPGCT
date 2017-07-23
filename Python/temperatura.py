#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : temperaturas.py
# Description   : Sistema indicador led de la temperatura del procesador en tiempo real. Utiliza tantos leds como GPIOs se le indiquen, siendo el último el de "alarma".
# Author        : Veltys
# Date          : 10-07-2017
# Version       : 2.1.4
# Usage         : python3 temperaturas.py
# Notes         : Mandándole la señal "SIGUSR1", el sistema pasa a "modo test", lo cual enciende todos los leds, para comprobar su funcionamiento
#                 Mandándole la señal "SIGUSR2", el sistema pasa a "modo apagado", lo cual simplemente apaga todos los leds hasta que esta misma señal sea recibida de nuevo


import errno                                                                    # Códigos de error
import sys                                                                      # Funcionalidades varias del sistema

try:
  from config import temperaturas_config as config                              # Configuración

except ImportError:
  print('Error: Archivo de configuración no encontrado', file = sys.stderr)
  sys.exit(errno.ENOENT)

from time import sleep                                                          # Para hacer pausas
from shlex import split                                                         # Manejo de cadenas
from subprocess import check_output                                             # Llamadas a programas externos, recuperando su respuesta
import comun                                                                    # Funciones comunes a varios sistemas
import os                                                                       # Funcionalidades varias del sistema operativo
import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO

class temperaturas(comun.app):
    def __init__(self, config, nombre):
        super().__init__(config, nombre)

    def bucle(self):
        try:
            while True:
                if not(self._modo_apagado):
                    temperatura = check_output(split('/opt/vc/bin/vcgencmd measure_temp'))
                    temperatura = float(temperatura[5:-3])
                    
                    for gpio, modo, activacion in self._config.GPIOS:
                        GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)

                    if temperatura < self._config.TEMPERATURAS[0]:
                        GPIO.output(self._config.GPIOS[0][0], GPIO.HIGH if self._config.GPIOS[0][2] else GPIO.LOW)
                    elif temperatura < self._config.TEMPERATURAS[1]:
                        GPIO.output(self._config.GPIOS[1][0], GPIO.HIGH if self._config.GPIOS[1][2] else GPIO.LOW)
                    elif temperatura < self._config.TEMPERATURAS[2]:
                        GPIO.output(self._config.GPIOS[2][0], GPIO.HIGH if self._config.GPIOS[2][2] else GPIO.LOW)
                    else:
                        GPIO.output(self._config.GPIOS[3][0], GPIO.HIGH if self._config.GPIOS[3][2] else GPIO.LOW)

                sleep(self._config.PAUSA)

        except KeyboardInterrupt:
            self.cerrar()
            return

    def __del__(self):
        super().__del__()


def main(argv = sys.argv):
    app = temperaturas(config, os.path.basename(argv[0]))
    app.arranque()


if __name__ == '__main__':
    main(sys.argv)
