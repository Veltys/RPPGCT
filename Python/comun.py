#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : comun.py
# Description   : Módulo de funciones comunes a varios sistemas
# Author        : Veltys
# Date          : 06-07-2017
# Version       : 0.1.3
# Usage         : import comun | from comun import <clase>
# Notes         : 


from abc import ABCMeta, abstractmethod                                         # Clases abstractas
from time import sleep                                                          # Para hacer pausas
import errno                                                                    # Códigos de error
import os                                                                       # Funcionalidades varias del sistema operativo
import pid                                                                      # Módulo propio de acceso a las funciones relativas al PID
import signal                                                                   # Manejo de señales
import sys                                                                      # Funcionalidades varias del sistema
import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO


class app(object):
    __metaclass__ = ABCMeta


    def __init__(self, config):
        self._modo_apagado = False
        self._config = config
        self.asignar_senyales()


    def apagado(self):
        self._modo_apagado = not(self._modo_apagado)

        for gpio, activacion in self._config.GPIOS:
            GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)


    def arranque(self, nombre):
        if pid.comprobar(nombre):
            if pid.bloquear(nombre):
                GPIO.setmode(GPIO.BCM)                                          # Establecemos el sistema de numeración BCM
                GPIO.setwarnings(False)                                         # De esta forma no alertará de los problemas
    
                for i in range(len(self._config.GPIOS)):
                    # Se configuran los pines GPIO como salida o entrada en función de lo leído en la configuración
                    if self._config.GPIOS[i][1]:
                        GPIO.setup(self._config.GPIOS[i][0], GPIO.OUT)
                    else:
                        GPIO.setup(self._config.GPIOS[i][0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

                    if not(self._config.GPIOS[i][1]):
                        # En el caso de tener un pin GPIO de entrada, se necesitará transformar en lista la tupla, ya que es posible que haga falta modificar su contenido
                        self._config.GPIOS[i] = list(self._config.GPIOS[i])
                        
    
                self.bucle()
    
            else:
                print('Error: No se puede bloquear ' + nombre, file=sys.stderr)
                sys.exit(errno.EACCES)
    
        else:
            print('Error: Ya se ha iniciado una instancia de ' + nombre, file=sys.stderr)
            sys.exit(errno.EEXIST)


    def asignar_senyales(self):
        for senyal, funcion in self._config.senyales.items():
            signal.signal(eval('signal.' + senyal), eval('self.' + funcion))

    @abstractmethod
    def bucle(self):
        pass


    def cerrar(self):
        GPIO.cleanup()                                                          # Devolvemos los pines a su estado inicial
        pid.desbloquear(os.path.basename(sys.argv[0]))
        sys.exit()


    def test(self):
        for gpio, activacion in self._config.GPIOS:
            GPIO.output(gpio, GPIO.HIGH if activacion else GPIO.LOW)


    def sig_apagado(self, signum, frame):
            self.apagado()


    def sig_cerrar(self, signum, frame):
        self.cerrar()


    def sig_test(self, signum, frame):
        self.test()
        sleep(self._config.PAUSA)

    def __del__(self):
        pass
