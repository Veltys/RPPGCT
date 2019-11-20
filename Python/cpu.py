#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : cpu.py
# Description   : Sistema indicador led de la carga de CPU en tiempo real. Utiliza tantos leds como GPIOs se le indiquen, siendo el último el de "alarma"
# Author        : Veltys
# Date          : 13-07-2018
# Version       : 2.1.10
# Usage         : python3 cpu.py
# Notes         : Mandándole la señal "SIGUSR1", el sistema pasa a "modo test", lo cual enciende todos los leds, para comprobar su funcionamiento
#                 Mandándole la señal "SIGUSR2", el sistema pasa a "modo apagado", lo cual apaga todos los leds hasta que esta misma señal sea recibida de nuevo


DEBUG           = False
DEBUG_REMOTO    = False


import errno                                                                                            # Códigos de error
import os                                                                                               # Funcionalidades varias del sistema operativo
import sys                                                                                              # Funcionalidades varias del sistema

if DEBUG_REMOTO:
    import pydevd                                                                                       # Depuración remota

import RPi.GPIO as GPIO                                                                                 # Acceso a los pines GPIO

import comun                                                                                            # Funciones comunes a varios sistemas

from time import sleep                                                                                  # Para hacer pausas

if DEBUG_REMOTO:
    from pydevd_file_utils import setup_client_server_paths                                             # Configuración de las rutas Eclipse ➡

try:
    from psutil import cpu_percent                                                                      # Obtención del porcentaje de uso de la CPU

except ImportError:
    print('Error: Paquete "psutil" no encontrado' + os.linesep + 'Puede instalarlo con la orden "[sudo] pip3 install psutil"', file = sys.stderr)
    sys.exit(errno.ENOENT)

try:
    from config import cpu_config as config                                                             # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)


class cpu(comun.app):
    ''' Clase del sistema indicador led de la carga de CPU en tiempo real
    '''

    def __init__(self, config, nombre):
        ''' Constructor de la clase:
            - Llama al constructor de la clase padre
        '''

        super().__init__(config, nombre)

    def bucle(self):
        ''' Realiza en bucle las tareas asignadas a este sistema
        '''

        try:
            alarma = 0

            cantidad_puertos = len(self._config.GPIOS)                                                  # Precálculo de la cantidad de puertos

            while True:                                                                                 # Se ejecutará siempre, ya que las condiciones de parada son externas
                if not(self._modo_apagado):                                                             #     Si no se ha activado el "modo apagado"
                    cpu = cpu_percent()                                                                 #         Se mide el porcentaje de uso de la CPU

                    i = 0

                    for puertos in self._config.GPIOS:                                                  #         Se recorre la lista de puertos GPIO
                        for gpio, tipo, _, activacion, _ in puertos:
                            if tipo == self._config.LED:                                                #             Comprobación de seguridad para no manipular leds de otro tipo
                                if i < len(self._config.GPIOS) - 1:                                     #                 Puertos asociados a leds normales
                                    if cpu >= 100 / (cantidad_puertos - 1) * i:                         #                     Si el porcentaje de CPU es mayor o igual al umbral de encendido
                                        GPIO.output(gpio, GPIO.HIGH if activacion else GPIO.LOW)        #                         Se enciende el led

                                    else:                                                               #                     Si no
                                        GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)        #                         Se apaga el led

                                else:                                                                   #                 Puerto asociados a led de alarma
                                    if cpu >= 95:                                                       #                     Si la CPU está por encima del 94%
                                        alarma += 1                                                     #                         Se añade una entrada a la alarma

                                        if alarma >= 5:                                                 #                         Si ya ha sucedido cinco o más veces
                                            GPIO.output(gpio, GPIO.HIGH if activacion else GPIO.LOW)    #                             Se enciende el led de alarma

                                    else:                                                               #                     Si no
                                        alarma = 0                                                      #                         Se reinicia la alarma

                                        GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)        #                         Se apaga el led de alarma

                            i = i + 1

                sleep(self._config.PAUSA)                                                               #     Pausa hasta la nueva comprobación

        except KeyboardInterrupt:                                                                       # Condición de parada: interrupción de teclado
            self.cerrar()                                                                               #     Se invoca al método de cierre

            return                                                                                      #     Se sale

    def __del__(self):
        ''' Destructor de la clase:
            - Llama al Destructor de la clase padre
        '''

        super().__del__()


def main(argv):
    if DEBUG_REMOTO:
        setup_client_server_paths(config.PYDEV_REMOTE_PATHS)

        pydevd.settrace(config.IP_DEP_REMOTA)

    app = cpu(config, os.path.basename(argv[0]))

    err = app.arranque()

    if err == 0:
        app.bucle()

    else:
        sys.exit(err)


if __name__ == '__main__':
    main(sys.argv)
