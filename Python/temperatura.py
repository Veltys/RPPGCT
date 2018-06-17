#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : temperatura.py
# Description   : Sistema indicador led de la temperatura del procesador en tiempo real. Utiliza tantos leds como GPIOs se le indiquen, siendo el último el de "alarma".
# Author        : Veltys
# Date          : 30-11-2017
# Version       : 2.2.1
# Usage         : python3 temperatura.py
# Notes         : Mandándole la señal "SIGUSR1", el sistema pasa a "modo test", lo cual enciende todos los leds, para comprobar su funcionamiento
#                 Mandándole la señal "SIGUSR2", el sistema pasa a "modo apagado", lo cual simplemente apaga todos los leds hasta que esta misma señal sea recibida de nuevo


DEBUG = False
DEBUG_REMOTO = False


import errno                                                                    # Códigos de error
import sys                                                                      # Funcionalidades varias del sistema

try:
    from config import temperatura_config as config                            # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)

from time import sleep                                                          # Para hacer pausas
from shlex import split                                                         # Manejo de cadenas
from subprocess import check_output                                             # Llamadas a programas externos, recuperando su respuesta
import comun                                                                    # Funciones comunes a varios sistemas
import os                                                                       # Funcionalidades varias del sistema operativo

if DEBUG_REMOTO:
    import pydevd                                                               # Depuración remota

import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO

class temperatura(comun.app):
    def __init__(self, config, nombre):
        super().__init__(config, nombre)

    def bucle(self):
        try:
            leds = []

            for i in range(4):
                leds.append(GPIO.PWM(self._config.GPIOS[i][0], self._config.FRECUENCIA))
                leds[i].start(0)

            while True:
                if not(self._modo_apagado):
                    temperatura = check_output(split('/opt/vc/bin/vcgencmd measure_temp'))
                    temperatura = float(temperatura[5:-3])

                    if temperatura < self._config.TEMPERATURAS[0]:              # Temperatura por debajo del valor mínimo
                        for i in range(4):
                            leds[i].ChangeDutyCycle(self._config.COLORES[0][i] * 100)

                    elif temperatura < self._config.TEMPERATURAS[1]:            # Temperatura por debajo del valor medio
                        for i in range(4):
                            leds[i].ChangeDutyCycle(self._config.COLORES[1][i] * 100)

                    elif temperatura < self._config.TEMPERATURAS[2]:            # Temperatura por debajo del valor máximo
                        for i in range(4):
                            leds[i].ChangeDutyCycle(self._config.COLORES[2][i] * 100)

                    else:                                                       # Temperatura por encima del valor máximo
                        for i in range(4):
                            leds[i].ChangeDutyCycle(self._config.COLORES[3][i] * 100)

                sleep(self._config.PAUSA)

        except KeyboardInterrupt:
            self.cerrar()
            return

    def __del__(self):
        super().__del__()


def main(argv):
    if DEBUG_REMOTO:
        pydevd.settrace(config.IP_DEP_REMOTA)

    app = temperatura(config, os.path.basename(argv[0]))
    err = app.arranque()

    if err == 0:
        app.bucle()

    else:
        sys.exit(err)


if __name__ == '__main__':
    main(sys.argv)
