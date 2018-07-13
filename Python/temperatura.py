#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : temperatura.py
# Description   : Sistema indicador led de la temperatura del procesador en tiempo real. Utiliza tantos leds como GPIOs se le indiquen, siendo el último el de "alarma".
# Author        : Veltys
# Date          : 13-07-2018
# Version       : 2.2.4
# Usage         : python3 temperatura.py
# Notes         : Mandándole la señal "SIGUSR1", el sistema pasa a "modo test", lo cual enciende todos los leds, para comprobar su funcionamiento
#                 Mandándole la señal "SIGUSR2", el sistema pasa a "modo apagado", lo cual apaga todos los leds hasta que esta misma señal sea recibida de nuevo


CMD_COMANDO     = '/opt/vc/bin/vcgencmd'
CMD_PARAMETROS  = 'measure_temp'
DEBUG           = False
DEBUG_REMOTO    = False

import errno                                                                                        # Códigos de error
import os                                                                                           # Funcionalidades varias del sistema operativo
import sys                                                                                          # Funcionalidades varias del sistema

if DEBUG_REMOTO:
    import pydevd                                                                                   # Depuración remota

import RPi.GPIO as GPIO                                                                             # Acceso a los pines GPIO

import comun                                                                                        # Funciones comunes a varios sistemas

from time import sleep                                                                              # Para hacer pausas
from subprocess import check_output                                                                 # Llamadas a programas externos, recuperando su respuesta

try:
    from config import temperatura_config as config                                                 # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)


class temperatura(comun.app):
    ''' Clase del servidor del sistema indicador led de la temperatura del procesador en tiempo real
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
            for _, _, acceso, _, _ in self._config.GPIOS:                                           # Se recorre la lista de puertos GPIO
                acceso.start(0)                                                                     #     Se inicializa el led a 0 (porcentaje de su ciclo de trabajo que estará encendido)

            while True:                                                                             # Se ejecutará siempre, ya que las condiciones de parada son externas
                if not(self._modo_apagado):                                                         #     Si no se ha activado el "modo apagado"
                    temperatura = check_output([CMD_COMANDO, CMD_PARAMETROS])                       #         Se lee la temperatura de la CPU
                    temperatura = float(temperatura[5:-3])                                          #         Se convierte a un valor numérico

                    if temperatura < self._config.TEMPERATURAS[0]:                                  #         Se comprueba si está por debajo del valor mínimo
                        j = 0                                                                       #             Se asigna la coordenada corespondiente para el posterior acceso a la lista de colores de los leds

                    elif temperatura < self._config.TEMPERATURAS[1]:                                #         Se comprueba si está por debajo del valor medio
                        j = 1                                                                       #             Se asigna la coordenada corespondiente para el posterior acceso a la lista de colores de los leds

                    elif temperatura < self._config.TEMPERATURAS[2]:                                #         Se comprueba si está por debajo del valor máximo
                        j = 2                                                                       #             Se asigna la coordenada corespondiente para el posterior acceso a la lista de colores de los leds

                    else:                                                                           #         Está igual o por encima del valor máximo
                        j = 3                                                                       #             Se asigna la coordenada corespondiente para el posterior acceso a la lista de colores de los leds

                    # TODO: Optimizar
                    for i in range(len(self._config.GPIOS)):                                        #         Se recorre la lista de leds
                        self._config.GPIOS[i][2].ChangeDutyCycle(self._config.COLORES[j][i] * 100)  #             Se cambia el ciclo de ejecución en función de la cordenada anteriormente asignada

                sleep(self._config.PAUSA)                                                           #     Pausa hasta la nueva comprobación

        except KeyboardInterrupt:
            self.cerrar()
            return


    def __del__(self):
        ''' Destructor de la clase:
            - Llama al Destructor de la clase padre
        '''

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
