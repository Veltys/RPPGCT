#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : reiniciar_router.py
# Description   : Sistema que comprueba si hay acceso a Internet. Si no, manda una señal en un puerto GPIO determinado
# Author        : Veltys
# Date          : 29-06-2017
# Version       : 1.2.1
# Usage         : python3 reiniciar_router.py
# Notes         : La idea es conectar un relé a este GPIO y al mismo la alimentación del sistema de acceso a Internet
#		  Mandándole la señal "SIGUSR1", el sistema pasa a "modo test", lo cual enciende todos los leds, para comprobar su funcionamiento
#                 Mandándole la señal "SIGUSR2", el sistema pasa a "modo apagado", lo cual simplemente apaga todos los leds hasta que esta misma señal sea recibida de nuevo


GPIOS = [4]                                                                 	# Pines GPIO que serán utilizados
PAUSAS = [15, 60, 180, 900]                                                     # Vector de segundos de pausas en orden de menor a mayor


from internet import hay_internet                                               # Módulo propio de comprobación de Internet
from time import sleep	                                                        # Gestión de pausas
import errno                                                                    # Códigos de error
import os									# Funcionalidades varias del sistema operativo
import pid                                                                      # Módulo propio de acceso a las funciones relativas al PID
import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO
import signal		        				                # Manejo de señales
import sys			                                                # Funcionalidades varias del sistema


def cerrar():                                                                   # Tareas necesarias al invocar el cierre
    GPIO.cleanup()                                                              # Devolvemos los pines a su estado inicial
    pid.desbloquear(os.path.basename(sys.argv[0]))
    sys.exit()


def test():                                                                     # Función de testeo del sistema
    for gpio in GPIOS:
        GPIO.output(gpio, GPIO.HIGH)


def sig_cerrar(signum, frame):
    cerrar()


def sig_test(signum, frame):
    test()
    sleep(PAUSAS[0])


def bucle():
    try:
        for gpio in GPIOS:
            GPIO.output(gpio, GPIO.LOW)

        sleep(PAUSAS[1])                                                        # Es necesario una pausa adicional, ya que al arrancar es posible que este script se ejecute antes de que haya red y no queremos que se reinicie el router "porque sí"

        while True:
            if hay_internet():                                                  # Si hay Internet, simplemente se esperará para hacer la próxima comprobación
                for gpio in GPIOS:
                    GPIO.output(gpio, GPIO.LOW)

                sleep(PAUSAS[3])

            else:                                                               # En caso contrario, se mandará la orden de apagado durante el tiempo mínimo establecido y después se restablecerá
                for gpio in GPIOS:
                    GPIO.output(gpio, GPIO.HIGH)

                sleep(PAUSAS[0])

                for gpio in GPIOS:
                    GPIO.output(gpio, GPIO.LOW)

                sleep(PAUSAS[2])                                                # Al acabar, se esperará a que se haya levantado la conexión y se volverá a comprobar


    except KeyboardInterrupt:
        cerrar()


def main(argv = sys.argv):
    signal.signal(signal.SIGTERM, sig_cerrar)
    signal.signal(signal.SIGUSR1, sig_test)

    if pid.comprobar(os.path.basename(argv[0])):
        if pid.bloquear(os.path.basename(argv[0])):
            GPIO.setmode(GPIO.BCM)				                # Establecemos el sistema de numeración BCM
            GPIO.setwarnings(False)				                # De esta forma no alertará de los problemas

            for gpio in GPIOS:
                GPIO.setup(gpio, GPIO.OUT)                                      # Configuramos los pines GPIO como salida

            bucle()

        else:
            print('Error: No se puede bloquear ' + os.path.basename(argv[0]), file=sys.stderr)
            sys.exit(errno.EACCES)

    else:
        print('Error: Ya se ha iniciado una instancia de ' + os.path.basename(argv[0]), file=sys.stderr)
        sys.exit(errno.EEXIST)


if __name__ == '__main__':
    main(sys.argv)
