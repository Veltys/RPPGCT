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


modo_apagado = False


import errno									# Códigos de error
import sys                                                                      # Funcionalidades varias del sistema

try:
  from config import cpu_config as config  	                                # Configuración

except ImportError:
  print('Error: Archivo de configuración no encontrado', file=sys.stderr)
  sys.exit(errno.ENOENT)

from time import sleep	                                                        # Para hacer pausas
from shlex import split				        	                # Manejo de cadenas
from subprocess import check_output		        	                # Llamadas a programas externos
import os									# Funcionalidades varias del sistema operativo
import pid                                                                      # Módulo propio de acceso a las funciones relativas al PID
import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO
import signal		        				                # Manejo de señales


def apagado():
    global modo_apagado

    modo_apagado = not(modo_apagado)

    for gpio in config.GPIOS:
        GPIO.output(gpio, GPIO.LOW)


def cerrar():
    GPIO.cleanup()                                                              # Devolvemos los pines a su estado inicial
    pid.desbloquear(os.path.basename(sys.argv[0]))
    sys.exit()


def test():
    for gpio in config.GPIOS:
        GPIO.output(gpio, GPIO.HIGH)


def sig_apagado(signum, frame):
    apagado()


def sig_cerrar(signum, frame):
    cerrar()


def sig_test(signum, frame):
    test()
    sleep(PAUSA)


def bucle():
    alarma = 0

    try:
        while True:
            if modo_apagado:
                for gpio in config.GPIOS:
                    GPIO.output(gpio, GPIO.LOW)

            else:
                cpu = check_output(split('cat /proc/loadavg'))
                cpu = float(cpu[0:4]) * 100

                for i in range(len(config.GPIOS)):
                    if i < len(config.GPIOS) - 1:
                        if cpu >= 100 / (len(config.GPIOS) - 1) * i:
                            GPIO.output(config.GPIOS[i], GPIO.HIGH)
                        else:
                            GPIO.output(config.GPIOS[i], GPIO.LOW)

                    elif cpu >= 95:
                        alarma = alarma + 1

                        if alarma >= 5:
                            GPIO.output(config.GPIOS[i], GPIO.HIGH)

                    else:
                        alarma = 0
                        GPIO.output(config.GPIOS[i], GPIO.LOW)

            sleep(config.PAUSA)

    except KeyboardInterrupt:
        cerrar()


def main(argv = sys.argv):
    signal.signal(signal.SIGTERM, sig_cerrar)
    signal.signal(signal.SIGUSR1, sig_test)
    signal.signal(signal.SIGUSR2, sig_apagado)

    if pid.comprobar(os.path.basename(argv[0])):
        if pid.bloquear(os.path.basename(argv[0])):
            GPIO.setmode(GPIO.BCM)				                # Establecemos el sistema de numeración BCM
            GPIO.setwarnings(False)				                # De esta forma no alertará de los problemas

            for gpio in config.GPIOS:
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
