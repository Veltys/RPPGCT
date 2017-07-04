#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : cpu.py
# Description   : Sistema indicador led de la carga de CPU en tiempo real. Utiliza tantos leds como GPIOs se le indiquen, siendo el último el de "alarma"
# Author        : Veltys
# Date          : 01-07-2017
# Version       : 2.0.1
# Usage         : python3 cpu.py
# Notes         : Mandándole la señal "SIGUSR1", el sistema pasa a "modo test", lo cual enciende todos los leds, para comprobar su funcionamiento
#		  Mandándole la señal "SIGUSR2", el sistema pasa a "modo apagado", lo cual simplemente apaga todos los leds hasta que esta misma señal sea recibida de nuevo


import errno                                                                    # Códigos de error
import sys                                                                      # Funcionalidades varias del sistema

try:
  from config import cpu_config as config  	                                    # Configuración

except ImportError:
  print('Error: Archivo de configuración no encontrado', file=sys.stderr)
  sys.exit(errno.ENOENT)

from time import sleep	                                                        # Para hacer pausas
from shlex import split				        	                                # Manejo de cadenas
from subprocess import check_output                                             # Llamadas a programas externos
import comun                                                                    # Funciones comunes a varios sistemas
import os                                                                       # Funcionalidades varias del sistema operativo
import pid                                                                      # Módulo propio de acceso a las funciones relativas al PID
import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO


class cpu(comun.app):
    def __init__(self, config):
        super().__init__(config)

    def bucle(self):
        alarma = 0

        try:
            while True:
                if self._modo_apagado:
                    for gpio, activacion in self._config.GPIOS.items():
                        GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)

                else:
                    cpu = check_output(split('cat /proc/loadavg'))
                    cpu = float(cpu[0:4]) * 100

                    i = 0
                    for gpio, activacion in self._config.GPIOS.items():
                        if i < len(config.GPIOS) - 1:
                            if cpu >= 100 / (len(config.GPIOS) - 1) * i:
                                GPIO.output(gpio, GPIO.HIGH if activacion else GPIO.LOW)
                            else:
                                GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)

                        elif cpu >= 95:
                            alarma = alarma + 1

                            if alarma >= 5:
                                GPIO.output(gpio, GPIO.HIGH if activacion else GPIO.LOW)

                        else:
                            alarma = 0
                            GGPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)

                i += 1

                sleep(self._config.PAUSA)

        except KeyboardInterrupt:
            cerrar()


def main(argv = sys.argv):
    app = cpu(config)
    app.arranque(os.path.basename(argv[0]))


if __name__ == '__main__':
    main(sys.argv)
