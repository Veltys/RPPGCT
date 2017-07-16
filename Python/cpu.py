#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : cpu.py
# Description   : Sistema indicador led de la carga de CPU en tiempo real. Utiliza tantos leds como GPIOs se le indiquen, siendo el último el de "alarma"
# Author        : Veltys
# Date          : 16-07-2017
# Version       : 2.1.5
# Usage         : python3 cpu.py
# Notes         : Mandándole la señal "SIGUSR1", el sistema pasa a "modo test", lo cual enciende todos los leds, para comprobar su funcionamiento
#                 Mandándole la señal "SIGUSR2", el sistema pasa a "modo apagado", lo cual simplemente apaga todos los leds hasta que esta misma señal sea recibida de nuevo


import errno                                                                    # Códigos de error
import sys                                                                      # Funcionalidades varias del sistema

try:
  from config import cpu_config as config                                       # Configuración

except ImportError:
  print('Error: Archivo de configuración no encontrado', file=sys.stderr)
  sys.exit(errno.ENOENT)

from psutil import cpu_percent                                                  # Obtención del porcentaje de uso de la CPU
from time import sleep	                                                        # Para hacer pausas
from shlex import split                                                         # Manejo de cadenas
import comun                                                                    # Funciones comunes a varios sistemas
import os                                                                       # Funcionalidades varias del sistema operativo
import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO


class cpu(comun.app):
    def __init__(self, config):
        super().__init__(config)

    def bucle(self):
        try:
            alarma = 0

            while True:
                if self._modo_apagado:
                    for gpio, modo, activacion in self._config.GPIOS:
                        GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)

                else:
                    cpu = cpu_percent()

                    i = 0
                    for gpio, modo, activacion in self._config.GPIOS:
                        if i < len(self._config.GPIOS) - 1:
                            if cpu >= 100 / (len(self._config.GPIOS) - 1) * i:
                                GPIO.output(gpio, GPIO.HIGH if activacion else GPIO.LOW)
                            else:
                                GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)

                        elif cpu >= 95:
                            alarma = alarma + 1

                            if alarma >= 5:
                                GPIO.output(gpio, GPIO.HIGH if activacion else GPIO.LOW)

                        else:
                            alarma = 0
                            GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)

                        i += 1

                sleep(self._config.PAUSA)

        except KeyboardInterrupt:
            sys.exit(0)

    def __del__(self):
        super().__del__()


def main(argv = sys.argv):
    app = cpu(config, os.path.basename(argv[0]))
    app.arranque()


if __name__ == '__main__':
    main(sys.argv)
