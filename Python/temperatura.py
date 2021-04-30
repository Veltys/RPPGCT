#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : temperatura.py
# Description   : Sistema indicador led de la temperatura del procesador en tiempo real. Utiliza tantos leds como GPIOs se le indiquen, siendo el último el de "alarma".
# Author        : Veltys
# Date          : 2021-04-30
# Version       : 3.0.3
# Usage         : python3 temperatura.py
# Notes         : Mandándole la señal "SIGUSR1", el sistema pasa a "modo test", lo cual enciende todos los leds, para comprobar su funcionamiento
#                 Mandándole la señal "SIGUSR2", el sistema pasa a "modo apagado", lo cual apaga todos los leds hasta que esta misma señal sea recibida de nuevo


CMD_COMANDO     = '/usr/bin/vcgencmd'
CMD_PARAMETROS  = 'measure_temp'
DEBUG           = False
DEBUG_REMOTO    = False

import errno                                                                                            # Códigos de error
import os                                                                                               # Funcionalidades varias del sistema operativo
from subprocess import check_output                                                                     # Llamadas a programas externos, recuperando su respuesta
import sys                                                                                              # Funcionalidades varias del sistema
from time import sleep                                                                                  # Para hacer pausas

import RPi.GPIO as GPIO                                                                                 # Acceso a los pines GPIO
import comun                                                                                            # Funciones comunes a varios sistemas

if DEBUG_REMOTO:
    import pydevd                                                                                       # Depuración remota
    from pydevd_file_utils import setup_client_server_paths                                             # Configuración de las rutas Eclipse ➡

try:
    from config import temperatura_config as config                                                     # Configuración

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
            while True:                                                                                 # Se ejecutará siempre, ya que las condiciones de parada son externas
                if not(self._modo_apagado):                                                             #     Si no se ha activado el "modo apagado"
                    temperatura = check_output([CMD_COMANDO, CMD_PARAMETROS])                           #         Se lee la temperatura de la CPU
                    temperatura = float(temperatura[5:-3])                                              #         Se convierte a un valor numérico

                    if temperatura < self._config.TEMPERATURAS[0]:                                      #         Se comprueba si está por debajo del valor mínimo
                        j = 0                                                                           #             Se asigna la coordenada corespondiente para el posterior acceso a la lista de colores de los leds

                    elif temperatura < self._config.TEMPERATURAS[1]:                                    #         Se comprueba si está por debajo del valor medio
                        j = 1                                                                           #             Se asigna la coordenada corespondiente para el posterior acceso a la lista de colores de los leds

                    elif temperatura < self._config.TEMPERATURAS[2]:                                    #         Se comprueba si está por debajo del valor máximo
                        j = 2                                                                           #             Se asigna la coordenada corespondiente para el posterior acceso a la lista de colores de los leds

                    else:                                                                               #         Está igual o por encima del valor máximo
                        j = 3                                                                           #             Se asigna la coordenada corespondiente para el posterior acceso a la lista de colores de los leds

                    igual = mayor = menor = False                                                       #         Inicialización de variables

                    for i, velocidades in enumerate(self._config.VELOCIDADES):                          #         Se recorre la tupla de temperaturas y velocidades
                        if velocidades[0] < temperatura:                                                #             Cáculo del elemento menor
                            menor = i

                        elif velocidades[0] == temperatura:                                             #             Cáculo del elemento igual
                            igual = i

                            break

                        elif velocidades[0] > temperatura:                                              #             Cáculo del elemento mayor, si no hay igual
                            mayor = i

                            break

                    if igual is False:                                                                  #         Si no existe un elemento igual, puede que haya que interpolar
                        if mayor is False:                                                              #         Si valor mayor no se ha modificado e igual tampoco, se está ante un valor mayor que el máximo
                            velocidad = self._config.VELOCIDADES[len(self._config.VELOCIDADES) - 1][1]  #             Se establece la velocidad al final de los puntos

                        elif menor is False:                                                            #         Si valor menor no se ha modificado e igual tampoco, se está ante un valor menor que el mínimo
                            velocidad = self._config.VELOCIDADES[0][1]                                  #             Se establece la velocidad al inicial de los puntos

                        else:                                                                           #         En cualquier otro caso, se habrá de interpolar
                            velocidad = ((temperatura - self._config.VELOCIDADES[menor][0]) / (self._config.VELOCIDADES[mayor][0] - self._config.VELOCIDADES[menor][0])) * (self._config.VELOCIDADES[mayor][1] - self._config.VELOCIDADES[menor][1]) + self._config.VELOCIDADES[menor][1]
                            velocidad = round(velocidad, 2)

                        if velocidad > 0 and velocidad < self._config.VELOCIDAD_MINIMA:                 #         Ya calculada la velocidad, si ésta es menor que el mínimo que el ventilador requiere para su funcionamiento
                            velocidad = self._config.VELOCIDAD_MINIMA                                   #             Se pondrá al mínimo de éste

                    else:                                                                               #         Si sí
                        velocidad = self._config.VELOCIDADES[igual][1]                                  #             Se almacena su valor para posterior uso

                    i = 0                                                                               #         Contador de ciclos del bucle

                    for puertos in self._config.GPIOS:                                                  #         Se recorre la lista de leds
                        for gpio, tipo, acceso, activacion, _ in puertos:
                            if tipo == config.LED:                                                      #             Si se está ante un led
                                if j >= 3:                                                              #                 Si hay que activarlo
                                    GPIO.output(gpio, GPIO.HIGH if activacion else GPIO.LOW)            #                     Se activa

                                else:                                                                   #                 Si no
                                    GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)            #                     Se desactiva

                            elif tipo == config.LED_PWM:                                                #             Si se está ante un led PWM
                                acceso.ChangeDutyCycle(self._config.COLORES[j][i] * 100)                #                 Se cambia el ciclo de ejecución en función de la cordenada anteriormente asignada

                            elif tipo == config.VENTILADOR_PWM:                                         #             Si se está ante un ventilador PWM
                                acceso.ChangeDutyCycle(velocidad * 100)                                 #                 Se cambia el ciclo de ejecución en función de la cordenada anteriormente asignada

                            else:                                                                       #             Si se está ante cualquier otro
                                pass                                                                    #                 No se hace nada, ya que esto sería un caso que no debería de darse

                            i += 1                                                                      #         Aumento del contador

                sleep(self._config.PAUSA)                                                               #     Pausa hasta la nueva comprobación

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
        setup_client_server_paths(config.PYDEV_REMOTE_PATHS)

        pydevd.settrace(config.IP_DEP_REMOTA)

    app = temperatura(config, os.path.basename(argv[0]))

    err = app.arranque()

    if err == 0:
        app.bucle()

    else:
        sys.exit(err)


if __name__ == '__main__':
    main(sys.argv)
