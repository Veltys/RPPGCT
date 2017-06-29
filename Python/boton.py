#!/usr/bin/env python
# -*- coding: utf-8 -*-


GPIO_BOTON = 22


# from shlex import split				        	                # Manejo de cadenas
# from subprocess import check_output		        	                # Llamadas a programas externos
import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO
import sys			                                                # Funcionalidades varias del sistema


def cerrar():
        GPIO.cleanup()                                                          # Devolvemos los pines a su estado inicial
        sys.exit()


def bucle():
        i = 1

        try:
                while True:
                        print 'Esperando un evento en el PIN GPIO' + str(GPIO_BOTON) + ' ID del evento: ' +str(i)
                        GPIO.wait_for_edge(GPIO_BOTON, GPIO.RISING)
                        print 'Se ha detectado un evento de activación en el PIN GPIO' + str(GPIO_BOTON) + ' ID del evento: ' +str(i)
                        GPIO.wait_for_edge(GPIO_BOTON, GPIO.FALLING)
                        print 'Se ha detectado un evento de desactivación en el PIN GPIO' + str(GPIO_BOTON) + ' ID del evento: ' +str(i)
                        i = i + 1

        except:
                cerrar()


def main(argv = sys.argv):
        GPIO.setmode(GPIO.BCM)				                        # Establecemos el sistema de numeración BCM
        GPIO.setwarnings(False)				                        # De esta forma no alertará de los problemas
        GPIO.setup(GPIO_BOTON, GPIO.IN)			                        # Gonfiguramos los pines GPIO como entrada

        bucle()



if __name__ == '__main__':
        main(sys.argv)
