#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : comun.py
# Description   : Módulo de funciones comunes a varios sistemas
# Author        : Veltys
# Date          : 15-07-2017
# Version       : 0.2.2
# Usage         : import comun | from comun import <clase>
# Notes         : 


from abc import ABCMeta, abstractmethod                                         # Clases abstractas
from pid import bloqueo                                                         # Módulo propio para bloquear la ejecución de más de una instancia
from time import sleep                                                          # Para hacer pausas
import errno                                                                    # Códigos de error
import os                                                                       # Funcionalidades varias del sistema operativo
import signal                                                                   # Manejo de señales
import sys                                                                      # Funcionalidades varias del sistema
import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO


class app(object):
    # Clase abstracta que contiene todos los métodos comunes para una app de este sistema
 
    __metaclass__ = ABCMeta


    def __init__(self, config, nombre):
        ''' Constructor de la clase:
            - Inicializa variables
            - Carga la configuración
            - Asigna señales a sus correspondientes funciones
        '''

        self._config = config
        self._bloqueo = bloqueo(nombre)
        self._modo_apagado = False
        self.asignar_senyales()


    def apagado(self):
        ''' Activador / desactivador del "modo apagado":
            - Conmuta el "modo apagado"
            - "Apaga" todos los puertos GPIO 
        '''

        self._modo_apagado = not(self._modo_apagado)

        for gpio, modo, activacion in self._config.GPIOS:
            GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)


    def arranque(self):
        ''' Lleva a cabo las tareas necesarias para el "arranque" de la app:
            - Comprueba si hay otra instancia en ejecución
                - Si no, establece un bloqueo para evitar otras ejecuciones
                - Si sí, sale
            - Configura los puertos GPIO
            - Llama a la función self.bucle()
        '''

        if self._bloqueo.comprobar():
            if self._bloqueo.bloquear():
                try:
                    self._config.GPIOS

                except AttributeError:
                    pass

                else:
                    GPIO.setmode(GPIO.BCM)                                      # Establecemos el sistema de numeración BCM
                    GPIO.setwarnings(False)                                     # De esta forma no alertará de los problemas

                    for i in range(len(self._config.GPIOS)):                    # Se configuran los pines GPIO como salida o entrada en función de lo leído en la configuración
                        if self._config.GPIOS[i][1]:
                            GPIO.setup(self._config.GPIOS[i][0], GPIO.OUT)
                        else:
                            GPIO.setup(self._config.GPIOS[i][0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

                        if not(self._config.GPIOS[i][1]):                       # En el caso de tener un pin GPIO de entrada, se necesitará transformar en lista la tupla, ya que es posible que
                            self._config.GPIOS[i] = list(self._config.GPIOS[i]) # haga falta modificar su contenido

                self.bucle()
    
            else:
                print('Error: No se puede bloquear ' + nombre, file=sys.stderr)
                sys.exit(errno.EACCES)
    
        else:
            print('Error: Ya se ha iniciado una instancia de ' + nombre, file=sys.stderr)
            sys.exit(errno.EEXIST)


    def asignar_senyales(self):
        ''' Asigna señales a sus correspondientes funciones:
                - Comprueba si existe la variable correspondiente
                    - Si no, no hace nada
                    - Si sí, asigna la señal especificada con la función correspondiente
        '''

        try:
            self._config.senyales

        except AttributeError:
            pass

        else:
            for senyal, funcion in self._config.senyales.items():
                signal.signal(eval('signal.' + senyal), eval('self.' + funcion))

    @abstractmethod
    def bucle(self):
        ''' Función abstracta que será especificada en el sistema que la incluya.
        '''

        pass


    def test(self):
        ''' Ejecuta el modo de pruebas.
        '''

        try:
            self._config.GPIOS

        except AttributeError:
            pass

        else:
            for gpio, modo, activacion in self._config.GPIOS:
                GPIO.output(gpio, GPIO.HIGH if activacion else GPIO.LOW)

            sleep(self._config.PAUSA)


    def sig_apagado(self, signum, frame):
        ''' Funcion "wrapper" para el procesamiento de la señal de apagado
        '''

        self.apagado()


    def sig_test(self, signum, frame):
        ''' Funcion "wrapper" para el procesamiento de la señal de pruebas
        '''

        self.test()


    def __del__(self):
        ''' Destructor de la clase: Realiza las operaciones necesarias para el cierre del sistema:
            - "Limpia" los puertos GPIO que hayan podido usarse
            - Desbloquea la posible ejecución de otra futura instancia del mismo sistema
        '''

        GPIO.cleanup()                                                          # Devolvemos los pines a su estado inicial
        self._bloqueo.desbloquear()
